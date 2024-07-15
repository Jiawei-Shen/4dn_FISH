import argparse

def main():
    parser = argparse.ArgumentParser(description="Add your inputs here. Up to 10 files, core is required")
    parser.add_argument('--core', type=str, required=True, help='This is the MANDATORY core table of the 4DN FISH-omics Format for Chromatin Tracing')
    parser.add_argument('--rna', type=str, help="This table is used to store and share the results of RNA FISH-omics experiments, CONDITIONALLY REQUIRED")
    parser.add_argument('--quality', type=str, help='This table is highly RECOMMENDED and it is designed to provide quality metrics for the Spot localization, information about the optical Channel, and various aberration corrections that have been applied prior to localization')
    parser.add_argument('--bio', type=str, help="This table is highly RECOMMENDED and it is designed to store and share biological properties associated with individual Spots")
    parser.add_argument('--demultiplexing', type=str, help='This table is OPTIONAL and is designed to be used in the case of multiplexed FISH experiments')
    parser.add_argument('--trace', type=str, help='This OPTIONAL table is used to document properties that are globally associated with individual Traces')
    parser.add_argument('--cell', type=str, help='This OPTIONAL table is used to document properties that are globally associated with individual Cells')
    parser.add_argument('--subcell', type=str, help='This CONDITIONALLY REQUIRED table is used to document properties that are globally associated with individual sub-cellular ROIs that typically correspond to sub-nuclear features')
    parser.add_argument('--extracell', type=str, help='This CONDITIONALLY REQUIRED table is used to document properties that are globally associated with individual extracellular structures')
    parser.add_argument('--mapping', type=str, help='This table is used to provide the boundaries of Cells and other ROIs identified as part of this experiment. CONDITIONALLY REQUIRED if --subcell, -cell, and/or -extracell tables are provided')

    args = parser.parse_args()

    if args.cell and args.subcell is None:
        parser.error("--subcell is required if --cell is provided")

    if args.cell and args.extracell is None:
        parser.error("--extracell is required if --cell is provided")

    if args.subcell and args.mapping is None or args.extracell and args.mapping is None or args.cell and args.mapping is None:
        parser.error("--mapping is required if --subcell, --extracell or --cell is provided")

    file_dictionary = {'core': args.core}
    if args.rna != None:
        file_dictionary['rna'] = args.rna
    if args.quality != None:
        file_dictionary['quality'] = args.quality
    if args.bio != None:
        file_dictionary['bio'] = args.bio
    if args.demultiplexing != None:
        file_dictionary['demultiplexing'] = args.demultiplexing
    if args.trace != None:
        file_dictionary['trace'] = args.trace
    if args.cell != None:
        file_dictionary['cell'] = args.cell
    if args.subcell != None:
        file_dictionary['subcell'] = args.subcell
    if args.extracell != None:
        file_dictionary['extracell'] = args.extracell
    if args.mapping != None:
        file_dictionary['mapping'] = args.mapping

    print(file_dictionary)

if __name__ == "__main__":
    main()