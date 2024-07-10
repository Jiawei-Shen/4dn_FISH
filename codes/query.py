import zlib
import pandas as pd

def compress(input_file_path, output_file_path):
    # Read the CSV file in binary mode
    with open(input_file_path, 'rb') as csv_file:
        csv_data = csv_file.read()
    
    # Compress the data using zlib
    compressed_data = zlib.compress(csv_data)
    
    # Write the compressed data to a new file
    with open(output_file_path, 'wb') as compressed_file:
        compressed_file.write(compressed_data)
    

def decompress(compressed_file_path, output_file_path):
    # Read the compressed file in binary mode
    with open(compressed_file_path, 'rb') as compressed_file:
        compressed_data = compressed_file.read()
    
    # Decompress the data using zlib
    decompressed_data = zlib.decompress(compressed_data)
    
    # Write the decompressed data to a new file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(decompressed_data)


def query_compressed_csv(file_path, query):
    # Full decompression
    # Read the compressed file
    with open(file_path, 'rb') as compressed_file:
        compressed_data = compressed_file.read()
    
    # Decompress the data using zlib
    decompressed_data = zlib.decompress(compressed_data)
    
    # Load the decompressed data into a pandas DataFrame
    from io import BytesIO
    decompressed_data_io = BytesIO(decompressed_data)
    df = pd.read_csv(decompressed_data_io)
    
    # Query the DataFrame
    result = df.query(query)
    
    return result

def build_index_zlib(file_path, key_col_index):
    index = {}
    decompressor = zlib.decompressobj()
    buffer_size = 47
    accumulated_data = ""
    offset = 0
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(buffer_size):
            decompressed_chunk = decompressor.decompress(chunk).decode('utf-8')
            accumulated_data += decompressed_chunk
            
            while '\n' in accumulated_data:
                line, accumulated_data = accumulated_data.split('\n', 1)
                
                if not line:
                    continue
                
                key = line.split(',')[key_col_index]
                index[key] = offset
                offset += len(line) + 1  # +1 for the newline character
    
    return index

def query_compressed_file_zlib(file_path, index, query_value):
    # not full decompression
    decompressor = zlib.decompressobj()
    buffer_size = 4096
    accumulated_data = ""
    offset = index.get(str(query_value))
    
    if offset is None:
        return None
    
    with open(file_path, 'rb') as f:
        f.seek(offset)
        while chunk := f.read(buffer_size):
            decompressed_chunk = decompressor.decompress(chunk).decode('utf-8')
            accumulated_data += decompressed_chunk
            
            while '\n' in accumulated_data:
                line, accumulated_data = accumulated_data.split('\n', 1)
                if not line:
                    continue
                
                if line.split(',')[1] == str(query_value):  # Assuming the key column is the first column
                    return line.strip()
    return None


# Compress
csv_file = '/Users/aidenqian/Documents/GitHub/4dn_FISH/without_headers.csv'        # Path to the CSV file to compress
compressed_file = 'test1.csv.zlib'  # Path to save the compressed file

compress(csv_file, compressed_file)

# Example usage
compressed_file_path = 'test1.csv.zlib'  # Path to the compressed CSV file
key_col_index = 1  # Index of the key column
index = build_index_zlib(compressed_file_path, key_col_index)
query_value = 1  # Value to query in the indexed column
result = query_compressed_file_zlib(compressed_file_path, index, query_value)
print(result)

# Decompress
# compressed_file = 'test1.csv.zlib'
# decompressed_file = 'test2.csv'

# decompress(compressed_file, decompressed_file)

# Queries compressed file
# compressed_file = '/Users/aidenqian/Documents/GitHub/4dn_FISH/test1.csv.zlib'  # Path to the compressed CSV file
query = 'Trace_ID == 1'  # Query to filter the data

result_df = query_compressed_csv(compressed_file, query)
print(result_df)