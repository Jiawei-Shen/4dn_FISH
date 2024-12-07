import struct

class Writer:
	# converts txt to binary, writes into a binary file
	def __init__(self):
		self.core_file = open("test1.FISH", "wb")
	
	def write_core_header(self, header_list):
		'''
		Writes the metadata for DNA core table
		
		Format:                               Max characters allowed
		FISH
		##FOF-CT_version=v___________________ (float)
		##Table_namespace= __________________ (15 char)
		##genome_assembly= __________________ (10 char)
		##XYZ_unit= _________________________ (6 char)
		#lab_name: __________________________ (30 char)
		#experimenter_contact: ______________ (30 char)
		#Software_Title: ____________________ (20 char)
		#Software_Type: _____________________ (20 char)
		#Software_Authors: __________________ (80 char)
		#Software_Description: ______________ (100 char)
		#Software_Repository: _______________ (60 char)
		#Software_PreferredCitationID: ______ (100 char)
		#additional_tables: _________________ (175 char)
		##columns= __________________________ (66 char)
		'''

		# byte sizes for header categories
		sizes = ["15s", "10s", "6s", "30s", "30s", "20s", "20s", "80s", "100s", "60s", "100s", "175s", "66s"]

		# writes into file
		self.core_file.write(struct.pack("4s", header_list[0].encode('utf-8')))
		self.core_file.write('\n'.encode('utf-8'))
		self.core_file.write(struct.pack("f", header_list[1]))

		counter = 0
		for row in header_list[2:]:
			self.core_file.write('\n'.encode('utf-8'))
			self.core_file.write(struct.pack(sizes[counter], row.encode("utf-8")))
			counter+=1
			
# ------------------------------------
# This part is sorta more like the Reader class, but I didn't make a class
# 1. Open the file to read
# 2. Take the splits of each metadata line, and add the wanted data into a list
# 3. Use .write_header to write the metadata into a .FISH file

# reads the input csv file
fin = open("test.csv", "r")

# metadata
core_splits = ["e=", "y=", "t=", ": ", ": ", ": ", ": ", ": ", ": ", ": ", ": ", ": "]
# spot_splits = ["e=", "t=", ": ", ": ", ": ", ": ", ": "]
magic_size = "FISH"
version = float(fin.readline().split("=v")[1][:-1])
variables = [magic_size, version]

for split in core_splits:
	variables.append(fin.readline().split(split)[1][:-1])
columns = fin.readline().split("=(")[1][:-2]
variables.append(columns)

# runs writer
test = Writer()

test.write_core_header(variables)

# writing the actual number data into a seperate csv file
new_file = open("without_headers.csv", "w")
new_file.write(columns + '\n')
Lines = fin.readlines()

for line in Lines:
	new_file.write(line)

"""metadata_size = len(variables)
core_df = pd.read_csv("without_headers.csv")
fin2 = open("test.FISH", "a")
core_df.to_csv('test.FISH', mode='a', index=True, header=True)"""