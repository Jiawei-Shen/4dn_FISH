import pandas as pd
import re


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


def read_csv_with_skipped_lines_and_set_header(file_path, skip_lines_count, column_names):
    try:
        df = pd.read_csv(file_path, skiprows=skip_lines_count, header=None)
        df.columns = column_names
        return df
    except Exception as e:
        return f"An error occurred while reading the CSV file: {e}"


def read_4dn_csv(file_path='./Dataset/4DNFIQCHBYZ6_DNA-spot_trace_core.csv'):
    hash_lines_count, last_header = count_hash_lines_and_get_column_header(file_path)

    print(f"Lines starting with '#': {hash_lines_count}")
    print(f"Last header line: {last_header}")

    # Read the CSV file, skipping the lines starting with '#' and setting the column names
    df = read_csv_with_skipped_lines_and_set_header(file_path, hash_lines_count, last_header)
    if isinstance(df, pd.DataFrame):
        print(df.head())
    else:
        print(df)
    return df


if __name__ == "__main__":
    core_df = read_4dn_csv()
    cell_data_df = read_4dn_csv(file_path='./Dataset/4DNFITOO96GG_cell_data.csv')
    spot_df = read_4dn_csv(file_path='./Dataset/4DNFI5WKRHYC_spot_biological_data.csv')

    merged_df = pd.merge(core_df, spot_df, on='Spot_ID')
    merged_df = pd.merge(merged_df, cell_data_df, on='Cell_ID')

    print('Done!')
