import zlib

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


# Compress
csv_file_path = 'without_headers.csv'        # Path to the CSV file to compress
compressed_file_path = 'test1.csv.zlib'  # Path to save the compressed file

compress_csv(csv_file_path, compressed_file_path)

# Decompress
compressed_file_path = 'test1.csv.zlib'  # Path to the compressed file
decompressed_file_path = 'test2.csv'  # Path to save the decompressed file

decompress_file(compressed_file_path, decompressed_file_path)