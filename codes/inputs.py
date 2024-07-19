import argparse
import os

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

def main():
    parser = argparse.ArgumentParser(description="For more detailed help, go to [link]")

    # add the arguments
    parser.add_argument('--core', type=str, required=True, help='[path] This is the path input for the DNA-Spot/Trace Data core table')
    parser.add_argument('--rna', type=str, help='[path] This is the path input for the RNA-Spot Data table')
    parser.add_argument('--quality', type=str, help='[path] This is the path input for the Spot Quality table')
    parser.add_argument('--bio', type=str, help='[path] This is the path input for the Spot Biological Data table')
    parser.add_argument('--demultiplexing', type=str, help='[path] This is the path input for the Spot Demultiplexing table')
    parser.add_argument('--trace', type=str, help='[path] This is the path input for the Trace Data table')
    parser.add_argument('--cell', type=str, help='[path] This is the path input for the Cell Data table')
    parser.add_argument('--subcell', type=str, help='[path] This is the path input for the Sub-Cell ROI Data table')
    parser.add_argument('--extracell', type=str, help='[path] This is the path input for the Extra-Cell ROI Data table')
    parser.add_argument('--mapping', type=str, help='[path] This is the path input for the Cell/ROI Mapping table')
    
    parser.add_argument('--files', nargs='+', help='A list of files (optional)')

    args = parser.parse_args()

    # Conditional requirement checks
    if args.cell and args.subcell is None:
        parser.error("--subcell is required if --cell is provided")

    if args.cell and args.extracell is None:
        parser.error("--extracell is required if --cell is provided")

    if (args.subcell or args.extracell or args.cell) and args.mapping is None:
        parser.error("--mapping is required if --subcell, --extracell, or --cell is provided")

    # Collect the provided arguments into a dictionary
    if not csvfile_exists(args.core):
        parser.error(f"The file {args.core} does not exist")
    file_dictionary = {'core': args.core}

    # Add the inputs to dictionary, as well as checking if the file path exists
    add_to_input_dictionary(parser, 'rna', args.rna, file_dictionary)
    add_to_input_dictionary(parser, 'quality', args.quality, file_dictionary)
    add_to_input_dictionary(parser, 'bio', args.bio, file_dictionary)
    add_to_input_dictionary(parser, 'demultiplexing', args.demultiplexing, file_dictionary)
    add_to_input_dictionary(parser, 'trace', args.trace, file_dictionary)
    add_to_input_dictionary(parser, 'cell', args.cell, file_dictionary)
    add_to_input_dictionary(parser, 'subcell', args.subcell, file_dictionary)
    add_to_input_dictionary(parser, 'extracell', args.extracell, file_dictionary)
    add_to_input_dictionary(parser, 'mapping', args.mapping, file_dictionary)
    
    print(file_dictionary)

if __name__ == "__main__":
    main()
    