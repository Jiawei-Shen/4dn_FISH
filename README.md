# 4dn_FISH

## Step 1. Finish the metadata writing
1. The input is xxx.csv file. It should be in the write() function.
2. the file metadata should not contain too much table metadata, but the basic file information.
3. the table metadata (csv) should be in the page metadata.
4. we gonna sort the table into different parameters.
5. Then we will store the data into different chunks. (bgzf)
6. For those small data (not sure how small) we can store the index into the header
7. using zlib to compress the data. 
8. Make sure that every csv tables have the default sorted parameters!