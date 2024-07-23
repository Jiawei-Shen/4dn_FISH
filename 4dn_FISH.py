import FISH_utils
import struct
import zlib
import os
from decimal import Decimal, getcontext
import time
import numpy as np

MAX_UNCOMPRESSED_BLOCK_SIZE = 65536
UNIT_LENGTH = 8
SHORT_NAMES = short_names = ["core", "rna", "quality", "bio", "demultiplexing", "trace", "cell", "subcell", "extracell", "mapping"]
_fish_magic = b'FISH'
_fish_magic_page = b'FISHP'
_version = Decimal(110.5739636611)
_zlib_compressed_level = 6

# todo: EOF is still lacking
# todo: think about what function should be inner.
class FISH_4dn:
    def __init__(self, filename):
        if not filename.endswith('.fish'):
            raise ValueError("Filename must end with '.fish'")
        self.filename = filename
        self.data = []
        self.metadata = {}
        self.clevel = _zlib_compressed_level
        self.__page_start_offset_list = []
        self.__page_start_offset_pos = 0
        self.__buffer = b''
        self.__chunk_offsets_buffer = []
        self.__vir_offsets_buffer = b""
        self.__vir_offsets_offset = 0

    def read(self, head=200):
        """
        Read data from the binary file.
        """
        try:
            with open(self.filename, 'rb') as file:
                self.data = file.read()
                print(f"Data read from {self.filename}")
                print(self.data[:head])
                # print(self.data)
        except FileNotFoundError:
            print(f"File {self.filename} not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    def read_metadata(self):
        """
        Read data from the binary file.
        """
        metadata = {}
        # try:
        with open(self.filename, 'rb') as file:
            buffer = file.read(26)
            metadata_length = struct.unpack("<I", buffer[22:26])[0]

            file.seek(0)
            metadata_bin = file.read(metadata_length)
            pointer = [0]
            metadata["magic"] = FISH_utils.parse_binary(pointer, metadata_bin, f"<{len(_fish_magic)}s")
            metadata["version"] = FISH_utils.parse_binary(pointer, metadata_bin, "<f")
            metadata["total_size"] = FISH_utils.parse_binary(pointer, metadata_bin, "<Q")
            metadata["n_tables"] = FISH_utils.parse_binary(pointer, metadata_bin, "<I")
            metadata["tables"] = FISH_utils.parse_binary(pointer, metadata_bin, "<H")
            metadata["page_start_offset"] = FISH_utils.parse_binary(pointer, metadata_bin,
                                                                    f"<{metadata['n_tables']}I")
            metadata["len_text"] = FISH_utils.parse_binary(pointer, metadata_bin, "<H")
            metadata["text"] = FISH_utils.parse_binary(pointer, metadata_bin, f"<{metadata['len_text']}s")
            print(pointer[0])

            print(buffer)
        # except FileNotFoundError:
        #     print(f"File {self.filename} not found.")
        # except Exception as e:
        #     print(f"An error occurred while reading the file: {e}")

    def write(self, csv_files):
        """
        Write data to the file.
        """
        self.write_metadata(csv_files)
        for csv_file in csv_files:
            self.write_page(csv_file)
        self.finish_writing_file()

        try:
            with open(self.filename, 'ab') as file:
                file.write(b"0")
                print(f"Data written to {self.filename}")
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")

    # todo: users need to define the metadata
    # todo: metadata: csv_table_names
    def write_metadata(self, csv_files):
        """
        Write metadata to the binary file.
        """
        metadata = {"magic": _fish_magic, "version": _version, "total_size": 100, "n_tables": 3, "tables": 0xFFC,
                    "text": b"0"}
        self.metadata = metadata
        # metadata_bytes = str(metadata).encode('utf-8')

        try:
            with open(self.filename, 'wb') as file:
                file.write(struct.pack(f"<{len(metadata['magic'])}s", metadata["magic"]))
                file.write(struct.pack(f"<f", metadata["version"]))
                file.write(struct.pack(f"<Q", metadata["total_size"]))
                file.write(struct.pack(f"<I", metadata["n_tables"]))
                file.write(struct.pack(f"<H", metadata["tables"]))
                self.__page_start_offset_pos = file.tell()
                for i in range(metadata["n_tables"]):
                    file.write(struct.pack(f"<I", 0))  # page start offset, finish it in the end.
                file.write(
                    struct.pack(f"<H", len(metadata["text"])))  # The maximum value of the text is 65536 characters.
                file.write(struct.pack(f"<{len(metadata['text'])}s", metadata["text"]))
                print(f"Metadata written to {self.filename}")
        except Exception as e:
            print(f"An error occurred while writing metadata to the file: {e}")

    # todo: the sort method needed for each kind of table
    def write_page(self, csv_file):
        col_names = FISH_utils.get_column_names(csv_file)
        metadata = FISH_utils.get_hash_lines(csv_file)
        csv_data = FISH_utils.read_4dn_csv(csv_file)
        item_formats = FISH_utils.get_row_formats(csv_data)
        dtypes_list = FISH_utils.generate_dtype(item_formats)

        csv_data_sorted = csv_data.sort_values(by=['Chrom_Start', 'Chrom_End', 'Spot_ID'])
        csv_data_sorted.reset_index(drop=True, inplace=True)
        unique_count = csv_data_sorted['Chrom_Start'].nunique()
        self.write_page_metadata(metadata, item_formats, unique_count)
        self.write_content(csv_data_sorted, dtypes_list)
        self.finish_writing_page()

    def write_page_metadata(self, metadata, item_formats, unique_count):
        try:
            col_names = FISH_utils.get_column_names_from_metadata(metadata=metadata)
            metadata_without_col_names = [item for item in metadata if "##columns=" not in item]
        except Exception as e:
            print(f"An error occurred while read column names. {e}")

        try:
            with open(self.filename, 'ab') as file:
                self.__page_start_offset_list.append(file.tell())
                file.write(struct.pack(f"<{len(_fish_magic_page)}s", _fish_magic_page))
                # todo: add the page(table) name, also add sort-way
                # file.write(struct.pack(f"<B", len(_page_name)))
                # file.write(struct.pack(f"<{len(_page_name)}s", _page_name))
                for d in metadata_without_col_names:
                    file.write(struct.pack(f"<B", len(d)))
                    file.write(struct.pack(f"<{len(d)}s", d.encode('utf-8')))
                for i, c in enumerate(col_names):
                    file.write(struct.pack(f"<B", len(c)))
                    file.write(struct.pack(f"<{len(c)}s", c.encode('utf-8')))
                    file.write(struct.pack(f"<B", len(item_formats[i])))
                    file.write(struct.pack(f"<{len(item_formats[i])}s", item_formats[i].encode('utf-8')))
                self.__vir_offsets_offset = file.tell()
                for i in range(unique_count):
                    file.write(struct.pack(f"<I", 0))  # key name, e.g. chrom_start, trace_id
                    file.write(struct.pack(f"<Q", 0))  # virtual offset, (chunk_start(6bytes), in_chunk(2bytes))
                print(f"CSV table metadata written to {self.filename}")
        except Exception as e:
            print(f"An error occurred while writing metadata to the file: {e}")

    # todo: add what to sort in the write.
    # todo: change the first_occurrences subset to a parameter instead of a constant.
    def write_content(self, csv_data, dt):
        self.__chunk_offsets_buffer = []
        # Identify repeated values
        repeated_mask = csv_data.duplicated(subset='Chrom_Start', keep='first')
        repeated_values = csv_data.loc[repeated_mask, 'Chrom_Start'].unique()

        # Find first occurrences of these repeated values
        first_occurrences = csv_data[
            csv_data['Chrom_Start'].isin(repeated_values) & ~csv_data.duplicated(subset='Chrom_Start', keep='first')]
        the_chosen_column_index_dict = dict(zip(first_occurrences['Chrom_Start'], first_occurrences.index))
        row_length = UNIT_LENGTH * len(dt)

        binary_csv_data = csv_data.to_records(index=False).astype(dt).tobytes()
        self.__buffer += binary_csv_data
        while len(self.__buffer) >= MAX_UNCOMPRESSED_BLOCK_SIZE:
            self.write_chunk(self.__buffer[:MAX_UNCOMPRESSED_BLOCK_SIZE])
            self.__buffer = self.__buffer[MAX_UNCOMPRESSED_BLOCK_SIZE:]

        # virtual_offset = {key(e.g. chrom_start): (chunk_start, in_chunk)}
        virtual_offset = {
            key: (self.__chunk_offsets_buffer[value * row_length // MAX_UNCOMPRESSED_BLOCK_SIZE],
                  value * row_length % MAX_UNCOMPRESSED_BLOCK_SIZE)
            for key, value in the_chosen_column_index_dict.items()}
        self.__vir_offsets_buffer = FISH_utils.map_vo_dictionary_to_binary(virtual_offset)

    def write_chunk(self, data):
        c = zlib.compressobj(
            self.clevel, zlib.DEFLATED, -15, zlib.DEF_MEM_LEVEL, 0
        )
        compressed_data = c.compress(data) + c.flush()
        del c
        with open(self.filename, 'ab') as file:
            self.__chunk_offsets_buffer.append(file.tell())
            file.write(compressed_data)
        return compressed_data

    def finish_writing_page(self):
        FISH_utils.write_data_at_offset(self.filename, self.__vir_offsets_offset, self.__vir_offsets_buffer)
        self.__chunk_offsets_buffer = []
        self.__vir_offsets_offset = 0
        print("Done writing page!")

    def finish_writing_file(self):
        # Write the total size into the metadata
        with open(self.filename, 'r+b') as file:  # Open the file in read/write binary mode
            total_size = os.path.getsize(self.filename)
            file.seek(8)  # Move the file pointer to the specified offset
            file.write(struct.pack("<Q", total_size))  # Write the data at the offset

        # Write the page start offset into the metadata
        binary_page_start = b""
        for n in self.__page_start_offset_list:
            binary_page_start += struct.pack("<I", n)
        FISH_utils.write_data_at_offset(self.filename, self.__page_start_offset_pos, binary_page_start)
        print("Done writing files")


# Example usage
if __name__ == "__main__":
    # # Record the start time
    # start_time = time.time()

    file_handler = FISH_4dn('example.fish')
    # #  for test, I use three same csv data.
    csv_files = ['./Dataset/4DNFIQCHBYZ6_DNA-spot_trace_core.csv', './Dataset/4DNFIQCHBYZ6_DNA-spot_trace_core.csv',
                 './Dataset/4DNFIQCHBYZ6_DNA-spot_trace_core.csv']  # List of CSV files to write
    file_handler.write(csv_files)  # Write data from CSV files to the binary file
    #
    # # Record the end time
    # end_time = time.time()
    #
    # # Calculate the elapsed time
    # elapsed_time = end_time - start_time
    # print(f"Elapsed time: {elapsed_time} seconds")

    file_handler.read_metadata()

