# User Inputs in Terminal
## Inputting CSV files
These are the arguments available. All arguments below take a path as an argument.
### Required Arguments:
#### --core           
                        This is the MANDATORY core table of the 4DN FISH-omics
                        Format for Chromatin Tracing

### Conditionally Required Arguments:
####  --rna            
                        This table is used to store and share the results of
                        RNA FISH-omics experiments, CONDITIONALLY REQUIRED
####  --subcell     
                        This CONDITIONALLY REQUIRED table is used to document
                        properties that are globally associated with
                        individual sub-cellular ROIs that typically correspond
                        to sub-nuclear features
 #### --extracell
                        This CONDITIONALLY REQUIRED table is used to document
                        properties that are globally associated with
                        individual extracellular structures
 #### --mapping     
                        This table is used to provide the boundaries of cells
                        and other ROIs identified as part of this experiment.
                        CONDITIONALLY REQUIRED if --subcell, --cell, and/or
                        --extracell tables are provided

### Recommended Arguments:
####  --quality     
                        This table is highly RECOMMENDED and it is designed to
                        provide quality metrics for the Spot localization,
                        information about the optical Channel, and various
                        aberration corrections that have been applied prior to
                        localization
 #### --bio             
                        This table is highly RECOMMENDED and it is designed to
                        store and share biological properties associated with
                        individual Spots

### Optional Arguments:
####  --demultiplexing
                        This table is OPTIONAL and is designed to be used in
                        the case of multiplexed FISH experiments
####  --trace         
                        This OPTIONAL table is used to document properties
                        that are globally associated with individual Traces
####  --cell           
                        This OPTIONAL table is used to document properties
                        that are globally associated with individual Cells
> [!TIP]
> The order that you input arguments do not matter. For example, `--core [file] --rna [file]` will function the same as `--rna [file] --core [file]`
### Examples:
#### Succesful running
##### _Input_
                        python inputs.py --core /Users/johndoe/Downloads/core.csv --rna /Users/johndoe/Downloads/rna.csv
##### _Output_
                        {'core': '/Users/johndoe/Downloads/core.csv', 'rna': '/Users/johndoe/Downloads/rna.csv'}
#### File Error
##### _Input_
                        python inputs.py --core /Users/johndoe/Downloads/thisisnotafile.csv
##### _Output_
                        inputs.py: error: The file /Users/johndoe/Downloads/thisisnotafile.csv does not exist

## Sorting CSV files
##### Sorting format: --sort_[file you want to sort] [column_name]
##### Example:
                        --sort_core Chrom_Start
### Constraints
* You may only input one column name
* You may only sort a file by a column if that file is provided using the input argument (see above)
* Column names are case sensitive, so `spot_id` and `Spot_ID` will be interpreted differently by the computer
> [!IMPORTANT]
> You may not input a column name that does not exist in a file.
> The following error will pop up: `error: The column column is not contained within file_path`
### Possible Arguments
#### --sort_core
                        Input = [str] name of column. Sorts the core table by the column provided
#### --sort_rna
                        Input = [str] name of column. Sorts the rna table by the column provided
#### --sort_quality
                        Input = [str] name of column. Sorts the quality table by the column provided
#### --sort_bio
                        Input = [str] name of column. Sorts the bio table by the column provided
#### --sort_demultiplexing
                        Input = [str] name of column. Sorts the demultiplexing table by the column provided
#### --sort_trace
                        Input = [str] name of column. Sorts the trace table by the column provided
#### --sort_cell
                        Input = [str] name of column. Sorts the cell table by the column provided
#### --sort_subcell
                        Input = [str] name of column. Sorts the subcell table by the column provided.
#### --sort_extracell
                        Input = [str] name of column. Sorts the extracell table by the column provided
#### --sort_mapping
                        Input = [str] name of column. Sorts the mapping table by the column provided
