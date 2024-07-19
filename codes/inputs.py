import argparse
import os
import csv

def column_exists(file_path, column):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row_num, row in enumerate(reader, start=1):
            for col_num, cell in enumerate(row, start=1):
                if column in cell:
                    return True
        return False

def csvfile_exists(file):
    if not os.path.isfile(file):
        return False
    return True
    
def add_to_input_dictionary(parser, key, file, dictionary):
    if file is not None:
        if not csvfile_exists(file):
            parser.error(f"The file {file} does not exist")
        else:
            dictionary[key] = file
            return dictionary

def add_to_sort_dictionary(parser, file, key, column, dictionary):
    if column is not None:
        if column_exists(file, column):
            dictionary[key] = column
            return dictionary
        else:
            parser.error(f"The column {column} is not contained within {file}")

def update_sort_list(list):
    return list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9]

def main():
    parser = argparse.ArgumentParser(description="For more detailed help, go to [link]")

    inputs = parser.add_argument_group("Arguments for inputting files")
    sorts = parser.add_argument_group("Arguments for sorting files")

    # add the arguments
    inputs.add_argument('--core', type=str, required=True, help='[path] This is the path input for the DNA-Spot/Trace Data core table')
    inputs.add_argument('--rna', type=str, help='[path] This is the path input for the RNA-Spot Data table')
    inputs.add_argument('--quality', type=str, help='[path] This is the path input for the Spot Quality table')
    inputs.add_argument('--bio', type=str, help='[path] This is the path input for the Spot Biological Data table')
    inputs.add_argument('--demultiplexing', type=str, help='[path] This is the path input for the Spot Demultiplexing table')
    inputs.add_argument('--trace', type=str, help='[path] This is the path input for the Trace Data table')
    inputs.add_argument('--cell', type=str, help='[path] This is the path input for the Cell Data table')
    inputs.add_argument('--subcell', type=str, help='[path] This is the path input for the Sub-Cell ROI Data table')
    inputs.add_argument('--extracell', type=str, help='[path] This is the path input for the Extra-Cell ROI Data table')
    inputs.add_argument('--mapping', type=str, help='[path] This is the path input for the Cell/ROI Mapping table')
    
    # sort arguments
    sorts.add_argument('--sort_core', default = 'Spot_ID', type=str, help='[str] Takes the name of a column of the core table. Default: Spot_ID')
    sorts.add_argument('--sort_rna', default = 'Spot_ID', type=str, help='[str] Takes the name of a column of the rna table. Default: Spot_ID')
    sorts.add_argument('--sort_quality', default = 'Spot_ID', type=str, help='[str] Takes the name of a column of the quality table. Default: Spot_ID')
    sorts.add_argument('--sort_bio', default = 'Spot_ID', type=str, help='[str] Takes the name of a column of the bio table. Default: Spot_ID')
    sorts.add_argument('--sort_demultiplexing', default = 'Loc_ID', type=str, help='[str] Takes the name of a column of the demultiplexing table. Default: Loc_ID')
    sorts.add_argument('--sort_trace', default = 'Trace_ID', type=str, help='[str] Takes the name of a column of the trace table. Default: Trace_ID')
    sorts.add_argument('--sort_cell', default = 'Cell_ID', type=str, help='[str] Takes the name of a column of the cell table. Default: Cell_ID')
    sorts.add_argument('--sort_subcell', default = 'Sub_Cell_ROI_ID', type=str, help='[str] Takes the name of a column of the subcell table. Default: Sub_Cell_ROI_ID')
    sorts.add_argument('--sort_extracell', default = 'Extra_Cell_ROI', type=str, help='[str] Takes the name of a column of the extracell table. Default: Extra_Cell_ROI')
    sorts.add_argument('--sort_mapping', default = None, type=str, help='[str] Takes the name of a column of the mapping table. Default: None')

    args = parser.parse_args()

    # Conditional requirement checks
    if args.cell and args.subcell is None:
        parser.error("--subcell is required if --cell is provided")

    if args.cell and args.extracell is None:
        parser.error("--extracell is required if --cell is provided")

    if (args.subcell or args.extracell or args.cell) and args.mapping is None:
        parser.error("--mapping is required if --subcell, --extracell, or --cell is provided")

    # Makes sure that the user can only sort if the file that they want to sort is provided as well
    input_list = [args.core, args.rna, args.quality, args.bio, args.demultiplexing, args.trace, args.cell, args.subcell, args.extracell, args.mapping]
    sort_list = [args.sort_core, args.sort_rna, args.sort_quality, args.sort_bio, args.sort_demultiplexing, args.sort_trace, args.sort_cell, args.sort_subcell, args.sort_extracell, args.sort_mapping]
    for i in range(10):
        if input_list[i] is None:
            sort_list[i] = None
    args.sort_core, args.sort_rna, args.sort_quality, args.sort_bio, args.sort_demultiplexing, args.sort_trace, args.sort_cell, args.sort_subcell, args.sort_extracell, args.sort_mapping = update_sort_list(sort_list)
    
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
    
    print(file_dictionary)
    print(sort_dictionary)

if __name__ == "__main__":
    main()
    