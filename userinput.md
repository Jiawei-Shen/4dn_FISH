Required Arguments:
  arguments that must be given

  --core CORE           This is the MANDATORY core table of the 4DN FISH-omics
                        Format for Chromatin Tracing

Conditionally Required Arguments:
  --rna RNA             This table is used to store and share the results of
                        RNA FISH-omics experiments, CONDITIONALLY REQUIRED
  --subcell SUBCELL     This CONDITIONALLY REQUIRED table is used to document
                        properties that are globally associated with
                        individual sub-cellular ROIs that typically correspond
                        to sub-nuclear features
  --extracell EXTRACELL
                        This CONDITIONALLY REQUIRED table is used to document
                        properties that are globally associated with
                        individual extracellular structures
  --mapping MAPPING     This table is used to provide the boundaries of cells
                        and other ROIs identified as part of this experiment.
                        CONDITIONALLY REQUIRED if --subcell, --cell, and/or
                        --extracell tables are provided

Recommended Arguments:
  --quality QUALITY     This table is highly RECOMMENDED and it is designed to
                        provide quality metrics for the Spot localization,
                        information about the optical Channel, and various
                        aberration corrections that have been applied prior to
                        localization
  --bio BIO             This table is highly RECOMMENDED and it is designed to
                        store and share biological properties associated with
                        individual Spots

Optional Arguments:
  --demultiplexing DEMULTIPLEXING
                        This table is OPTIONAL and is designed to be used in
                        the case of multiplexed FISH experiments
  --trace TRACE         This OPTIONAL table is used to document properties
                        that are globally associated with individual Traces
  --cell CELL           This OPTIONAL table is used to document properties
                        that are globally associated with individual Cells
