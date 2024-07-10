import zlib
import pandas as pd

def compress_csv(input_file_path, output_file_path):
    # Read the CSV file in binary mode
    with open(input_file_path, 'rb') as csv_file:
        csv_data = csv_file.read()
    
    # Compress the data using zlib
    compressed_data = zlib.compress(csv_data)
    
    # Write the compressed data to a new file
    with open(output_file_path, 'wb') as compressed_file:
        compressed_file.write(compressed_data)
    

def decompress_file(compressed_file_path, output_file_path):
    # Read the compressed file in binary mode
    with open(compressed_file_path, 'rb') as compressed_file:
        compressed_data = compressed_file.read()
    
    # Decompress the data using zlib
    decompressed_data = zlib.decompress(compressed_data)
    
    # Write the decompressed data to a new file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(decompressed_data)


def query_compressed_csv_zlib(file_path, query):
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


# Compress
csv_file_path = '/Users/aidenqian/Documents/GitHub/4dn_FISH/without_headers.csv'        # Path to the CSV file to compress
compressed_file_path = 'test1.csv.zlib'  # Path to save the compressed file

compress_csv(csv_file_path, compressed_file_path)

# Decompress
# compressed_file_path = 'test1.csv.zlib'  # Path to the compressed file
# decompressed_file_path = 'test2.csv'  # Path to save the decompressed file

# decompress_file(compressed_file_path, decompressed_file_path)

# compressed_file_path = '/Users/aidenqian/Documents/GitHub/4dn_FISH/test1.csv.zlib'  # Path to the compressed CSV file
query = 'Trace_ID == 1'  # Query to filter the data

result_df = query_compressed_csv_zlib(compressed_file_path, query)
print(result_df)