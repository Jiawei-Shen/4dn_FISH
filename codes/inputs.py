import argparse

def main():
    parser = argparse.ArgumentParser(description="Add your inputs here. Up to 10 files, core is required")
    
    # categories of arguments
    required = parser.add_argument_group('Required Arguments')
    conditional = parser.add_argument_group('Conditionally Required Arguments')
    recommended = parser.add_argument_group('Recommended Arguments')
    optional = parser.add_argument_group('Optional Arguments')

    # add the arguments
    required.add_argument('--core', type=str, required=True, help='This is the MANDATORY core table of the 4DN FISH-omics Format for Chromatin Tracing')
    conditional.add_argument('--rna', type=str, help="This table is used to store and share the results of RNA FISH-omics experiments, CONDITIONALLY REQUIRED")
    recommended.add_argument('--quality', type=str, help='This table is highly RECOMMENDED and it is designed to provide quality metrics for the Spot localization, information about the optical Channel, and various aberration corrections that have been applied prior to localization')
    recommended.add_argument('--bio', type=str, help="This table is highly RECOMMENDED and it is designed to store and share biological properties associated with individual Spots")
    optional.add_argument('--demultiplexing', type=str, help='This table is OPTIONAL and is designed to be used in the case of multiplexed FISH experiments')
    optional.add_argument('--trace', type=str, help='This OPTIONAL table is used to document properties that are globally associated with individual Traces')
    optional.add_argument('--cell', type=str, help='This OPTIONAL table is used to document properties that are globally associated with individual Cells')
    conditional.add_argument('--subcell', type=str, help='This CONDITIONALLY REQUIRED table is used to document properties that are globally associated with individual sub-cellular ROIs that typically correspond to sub-nuclear features')
    conditional.add_argument('--extracell', type=str, help='This CONDITIONALLY REQUIRED table is used to document properties that are globally associated with individual extracellular structures')
    conditional.add_argument('--mapping', type=str, help='This table is used to provide the boundaries of cells and other ROIs identified as part of this experiment. CONDITIONALLY REQUIRED if --subcell, --cell, and/or --extracell tables are provided')
    
    args = parser.parse_args()

    # Conditional requirement checks
    if args.cell and args.subcell is None:
        parser.error("--subcell is required if --cell is provided")

    if args.cell and args.extracell is None:
        parser.error("--extracell is required if --cell is provided")

    if (args.subcell or args.extracell or args.cell) and args.mapping is None:
        parser.error("--mapping is required if --subcell, --extracell, or --cell is provided")

    # Collect the provided arguments into a dictionary
    file_dictionary = {'core': args.core}
    if args.rna is not None:
        file_dictionary['rna'] = args.rna
    if args.quality is not None:
        file_dictionary['quality'] = args.quality
    if args.bio is not None:
        file_dictionary['bio'] = args.bio
    if args.demultiplexing is not None:
        file_dictionary['demultiplexing'] = args.demultiplexing
    if args.trace is not None:
        file_dictionary['trace'] = args.trace
    if args.cell is not None:
        file_dictionary['cell'] = args.cell
    if args.subcell is not None:
        file_dictionary['subcell'] = args.subcell
    if args.extracell is not None:
        file_dictionary['extracell'] = args.extracell
    if args.mapping is not None:
        file_dictionary['mapping'] = args.mapping

    print(file_dictionary)

if __name__ == "__main__":
    main()
    