import csv
import pandas as pd
import re
import numpy as np
import struct
import zlib


def count_hash_lines_and_get_column_header(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            hash_lines_count = sum(1 for line in lines if line.startswith('#'))
            last_header = None
            for line in reversed(lines):
                if line.startswith('##columns'):
                    match = re.search(r'\(([^)]+)\)', line.strip())
                    if match:
                        last_header = match.group(1).split(',')
                    break
        return hash_lines_count, last_header
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def get_hash_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            hash_lines_count = sum(1 for line in lines if line.startswith('#'))
            hash_lines = [line for line in lines if line.startswith('#')]
            last_header = None
            for line in reversed(lines):
                if line.startswith('##columns'):
                    match = re.search(r'\(([^)]+)\)', line.strip())
                    if match:
                        last_header = match.group(1).split(',')
                    break
        return hash_lines
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def get_column_names(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            last_header = None
            for line in reversed(lines):
                if line.startswith('##columns'):
                    match = re.search(r'\(([^)]+)\)', line.strip())
                    if match:
                        last_header = match.group(1).split(',')
                    break
        return last_header
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def get_column_names_from_metadata(metadata):
    try:
        lines = metadata
        last_header = None
        for line in lines:
            if line.startswith('##columns'):
                match = re.search(r'\(([^)]+)\)', line.strip())
                if match:
                    last_header = match.group(1).split(',')
                break
        return last_header
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def read_csv_file(file_path):
    """
    Reads a CSV file and returns its contents as a list of lists.
    """
    data = []
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        print(f"Data read from {file_path}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    return data


def convert_row_to_bytes(row):
    """
    Converts a list (row) to a byte string.
    """
    return ','.join(row).encode('utf-8')


def read_csv_with_skipped_lines_and_set_header(file_path, skip_lines_count, column_names):
    try:
        df = pd.read_csv(file_path, skiprows=skip_lines_count, header=None)
        df.columns = column_names
        return df
    except Exception as e:
        return f"An error occurred while reading the CSV file: {e}"


def read_4dn_csv(file_path='./Dataset/4DNFIQCHBYZ6_DNA-spot_trace_core.csv'):
    hash_lines_count, last_header = count_hash_lines_and_get_column_header(file_path)

    # Read the CSV file, skipping the lines starting with '#' and setting the column names
    df = read_csv_with_skipped_lines_and_set_header(file_path, hash_lines_count, last_header)
    # if isinstance(df, pd.DataFrame):
    #     print(df.head())
    # else:
    #     print(df)
    return df


def get_row_formats(df, row_index=2):
    """
    Get the formats (data types) of each item in a specific row of a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to extract the row from.
    row_index (int): The index of the row to extract.

    Returns:
    list: A list containing the data types of each item in the row.
    """
    # Get the specific row
    row = df.iloc[row_index]

    # Create a list to store the data types
    formats = []

    # Populate the list with data types of each item in the row
    for column in df.columns:
        # Access the individual item using loc to avoid implicit type conversion
        item_type = type(df.loc[row_index, column]).__name__
        formats.append(item_type)

    return formats


def generate_dtype(type_list):
    # Define a mapping from string type names to NumPy data types
    type_mapping = {
        'int64': '<i8',
        'float64': '<f8'
    }

    # Create field names
    field_names = [f'field{i + 1}' for i in range(len(type_list))]

    # Create the dtype list
    dtype_list = [(field_names[i], type_mapping[type_list[i]]) for i in range(len(type_list))]

    # Generate the composite data type
    dt = np.dtype(dtype_list)
    return dt


def write_data_at_offset(file_path, offset, data):
    """
    Write data to a file at a specific offset.

    Parameters:
    file_path (str): The path to the file.
    offset (int): The position in the file where data should be written.
    data (bytes): The data to be written to the file.

    Returns:
    None
    """
    try:
        with open(file_path, 'r+b') as file:  # Open the file in read/write binary mode
            file.seek(offset)  # Move the file pointer to the specified offset
            file.write(data)   # Write the data at the offset
        print("Data written successfully.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def map_vo_dictionary_to_binary(input_dict):
    """
    Map the virtual offsets dictionary into a binary format with struct.pack.

    Parameters:
    input_dict (dict): The input dictionary in the format {key: (coffset, uoffset)}.

    Returns:
    bytes: The binary representation of the dictionary.
    """
    result = b''

    for key, (coffset, uoffset) in input_dict.items():
        # Pack the key as a 4-byte little-endian unsigned integer
        packed_key = struct.pack('<I', key)

        # Calculate the virtual offset as described
        virtual_offset = (coffset << 16) | uoffset

        # Pack the virtual offset as an 8-byte little-endian unsigned long long
        packed_offset = struct.pack('<Q', virtual_offset)

        # Combine the packed key and packed offset
        result += packed_key + packed_offset

    return result


# we assume the number is "I" type (4 bytes)
def binary_to_characters(number, table_types):
    result = []
    mask = 1 << 16
    table_types = extend_list_to_16(table_types)

    for i in range(16):
        if number & (mask >> i):
            result.append(table_types[i])

    return result


def extend_list_to_16(input_list):
    # Calculate how many empty strings are needed
    empty_strings_needed = 16 - len(input_list)

    # Add the empty strings to the list
    extended_list = input_list + [""] * empty_strings_needed

    return extended_list


def parse_binary(pointer, bin_content, bin_format):
    ptr = pointer[0]
    format_len = struct.calcsize(bin_format)
    result = struct.unpack(bin_format, bin_content[ptr:ptr+format_len])
    pointer[0] += format_len
    if len(result) == 1:
        result = result[0]
    else:
        result = list(result)
    return result


# For debug use
if __name__ == "__main__":
    core_df = read_4dn_csv()
    cell_data_df = read_4dn_csv(file_path='./Dataset/4DNFITOO96GG_cell_data.csv')
    spot_df = read_4dn_csv(file_path='./Dataset/4DNFI5WKRHYC_spot_biological_data.csv')

    merged_df = pd.merge(core_df, spot_df, on='Spot_ID')
    merged_df = pd.merge(merged_df, cell_data_df, on='Cell_ID')

    print('Done!')
