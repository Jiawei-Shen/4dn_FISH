import argparse
import os
import csv
import re
    
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

def csvfile_exists(file):
    if os.path.isfile(file):
        return True
    return False
    
def add_to_input_dictionary(parser, key, file, dictionary):
    if file is not None:
        if not csvfile_exists(file):
            parser.error(f"The file {file} does not exist")
        else:
            dictionary[key] = file
            return dictionary

def add_to_sort_dictionary(parser, file, key, column, dictionary):
    if column is not None:
        column_list = get_column_names(file)
        if column in column_list or " " + column in column_list:
            dictionary[key] = column
            return dictionary
        else:
            parser.error(f"The column {column} is not contained within {file}")

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

def main():
    description = """\
Arguments for inputting files:
Argument format: --[short_name] [file_path]

  [short_name] -> The short name for the file to input
  Possible short_names: --core, --rna, --quality, --bio, --demultiplexing, --trace, --cell, --subcell, --extracell, --mapping
  [file_path] -> Path of the file that is being inputted
For each file that you want to parse, you must add a new argument

Example Argument:
  --core core.path --trace trace.path

Arguments for sorting files:
Argument format: --[sort_short_name] [column_name]
  
  [sort_short_name] -> Name of argument, in the format of --sort_[blank]
  Possible sort_short_names:", help="--sort_core, --sort_rna, sort_quality, --sort_bio, --sort_demultiplexing, --sort_trace, --sort_cell, --sort_subcell, --sort_extracell, --sort_mapping
  [column_name] -> name of the column that is user is requesting to sort by
  For each file you want to sort, you must use a new argument

Example Argument:
    --sort_core Spot_ID --sort_trace FOV

Other Arguments
--text TEXT      [str] Space to add any additional comments
--clevel CLEVEL  [int] Compress level of files. A higher level means smaller size of the compressed file, but it takes a longer time to compress. Range = 1 to 9


"""
    parser = argparse.ArgumentParser(description=description, epilog = "For more detailed help, go to https://github.com/Jiawei-Shen/4dn_FISH/blob/Dev/userinput.md", formatter_class=argparse.RawDescriptionHelpFormatter, usage=argparse.SUPPRESS)

    # add the arguments
    parser.add_argument('--core', type=str, required=True, help=argparse.SUPPRESS)
    parser.add_argument('--rna', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--quality', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--bio', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--demultiplexing', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--trace', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--cell', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--subcell', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--extracell', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--mapping', type=str, help=argparse.SUPPRESS)
    
    # sort arguments
    parser.add_argument('--sort_core', default = 'Spot_ID', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--sort_rna', default = 'Spot_ID', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--sort_quality', default = 'Spot_ID', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--sort_bio', default = 'Spot_ID', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--sort_demultiplexing', default = 'Loc_ID', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--sort_trace', default = 'Trace_ID', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--sort_cell', default = 'Cell_ID', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--sort_subcell', default = 'Sub_Cell_ROI_ID', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--sort_extracell', default = 'Extra_Cell_ROI_ID', type=str, help=argparse.SUPPRESS)
    # mapping has three possible first columns
    parser.add_argument('--sort_mapping', default = None, type=str, help=argparse.SUPPRESS)

    # text argument
    parser.add_argument("--text", default = None, type=str, help=argparse.SUPPRESS)

    # compress level argument
    parser.add_argument("--clevel", default = 6, type=int, help=argparse.SUPPRESS)

    args = parser.parse_args()

    # Conditional requirement checks
    if args.cell and args.subcell is None:
        parser.error("--subcell is required if --cell is provided")

    if args.cell and args.extracell is None:
        parser.error("--extracell is required if --cell is provided")

    if (args.subcell or args.extracell or args.cell) and args.mapping is None:
        parser.error("--mapping is required if --subcell, --extracell, or --cell is provided")

    # Find the default mapping column if needed
    if args.mapping != None and args.sort_mapping == None:
        linenum, column_list = count_hash_lines_and_get_column_header(args.mapping)
        args.sort_mapping = column_list[0]

    if args.clevel > 9 or args.clevel < 1:
        parser.error("--clevel must be in range of 1 to 9")

    # Makes sure that the user can only sort if the file that they want to sort is provided as well
    input_list = [args.core, args.rna, args.quality, args.bio, args.demultiplexing, args.trace, args.cell, args.subcell, args.extracell, args.mapping]
    sort_list = [args.sort_core, args.sort_rna, args.sort_quality, args.sort_bio, args.sort_demultiplexing, args.sort_trace, args.sort_cell, args.sort_subcell, args.sort_extracell, args.sort_mapping]
    for i in range(10):
        if input_list[i] is None:
            sort_list[i] = None
    args.sort_core, args.sort_rna, args.sort_quality, args.sort_bio, args.sort_demultiplexing, args.sort_trace, args.sort_cell, args.sort_subcell, args.sort_extracell, args.sort_mapping = sort_list[0], sort_list[1], sort_list[2], sort_list[3], sort_list[4], sort_list[5], sort_list[6], sort_list[7], sort_list[8], sort_list[9]
    
    # Read info into dictionaries
    file_dictionary = {}
    sort_dictionary = {}

    # Add the inputs to dictionary, as well as checking if the file path exists
    add_to_input_dictionary(parser, 'core', args.core, file_dictionary)
    add_to_input_dictionary(parser, 'rna', args.rna, file_dictionary)
    add_to_input_dictionary(parser, 'quality', args.quality, file_dictionary)
    add_to_input_dictionary(parser, 'bio', args.bio, file_dictionary)
    add_to_input_dictionary(parser, 'demultiplexing', args.demultiplexing, file_dictionary)
    add_to_input_dictionary(parser, 'trace', args.trace, file_dictionary)
    add_to_input_dictionary(parser, 'cell', args.cell, file_dictionary)
    add_to_input_dictionary(parser, 'subcell', args.subcell, file_dictionary)
    add_to_input_dictionary(parser, 'extracell', args.extracell, file_dictionary)
    add_to_input_dictionary(parser, 'mapping', args.mapping, file_dictionary)

    # Adds sort information to dictionary, checking to see if the column exists as well
    add_to_sort_dictionary(parser, args.core, 'sort_core', args.sort_core, sort_dictionary)
    add_to_sort_dictionary(parser, args.rna, 'sort_rna', args.sort_rna, sort_dictionary)
    add_to_sort_dictionary(parser, args.quality, 'sort_quality', args.sort_quality, sort_dictionary)
    add_to_sort_dictionary(parser, args.bio, 'sort_bio', args.sort_bio, sort_dictionary)
    add_to_sort_dictionary(parser, args.demultiplexing, 'sort_demultiplexing', args.sort_demultiplexing, sort_dictionary)
    add_to_sort_dictionary(parser, args.trace, 'sort_trace', args.sort_trace, sort_dictionary)
    add_to_sort_dictionary(parser, args.cell, 'sort_cell', args.sort_cell, sort_dictionary)
    add_to_sort_dictionary(parser, args.subcell, 'sort_subcell', args.sort_subcell, sort_dictionary)
    add_to_sort_dictionary(parser, args.extracell, 'sort_extracell', args.sort_extracell, sort_dictionary)
    add_to_sort_dictionary(parser, args.mapping, 'sort_mapping', args.sort_mapping, sort_dictionary)
    
    # Print results
    print(file_dictionary)
    print(sort_dictionary)
    print("Text: " + str(args.text))
    print("Compress level: " + str(args.clevel))


if __name__ == "__main__":
    main()
