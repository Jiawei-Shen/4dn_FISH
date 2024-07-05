import struct
import pandas as pd

class Writer:
	# converts txt to binary, writes into a binary file
	def __init__(self):
		self.file = open("test.FISH", "wb")
	
	def write_core_header(self, header_list):
		# writes the metadata for DNA core table
		'''
		Format:
		FISH
		##FOF-CT_version=v___________________ (float)
		##Table_namespace=___________________ (max 15 char)
		##genome_assembly=___________________ (max 10 char)
		##XYZ_unit=__________________________ (max 6 char)
		#lab_name: __________________________ (max 30 char)
		#experimenter_contact: ______________ (max 30 char)
		#Software_Title: ____________________ (max 20 char)
		#Software_Type: _____________________ (max 20 char)
		#Software_Authors: __________________ (max 80 char)
		#Software_Description: ______________ (max 100 char)
		#Software_Repository: _______________ (max 60 char)
		#Software_PreferredCitationID: ______ (max 100 char)
		#additional_tables: _________________ (max 175 char)
		##columns= __________________________ (max 66 char)
		'''

		# byte sizes for header categories
		sizes = ["15s", "10s", "6s", "30s", "30s", "20s", "20s", "80s", "100s", "60s", "100s", "175s", "66s"]

		# writes into file
		self.file.write(struct.pack("4s", header_list[0].encode('utf-8')))
		self.file.write('\n'.encode('utf-8'))
		self.file.write(struct.pack("f", header_list[1]))
		self.file.write('\n'.encode('utf-8'))

		counter = 0
		for row in header_list[2:]:
			self.file.write(struct.pack(sizes[counter], row.encode("utf-8")))
			self.file.write('\n'.encode('utf-8'))
			counter+=1
			
# reads the input csv file
fin = open("test.csv", "r")
new_file = open("without_headers.csv", "w")

# metadata
magic_size = "FISH"
version = float(fin.readline().split("=v")[1][:-1])
table_namespace = fin.readline().split("e=")[1][:-1]
genome_assembly = fin.readline().split("y=")[1][:-1]
xyz_unit = fin.readline().split("t=")[1][:-1]
lab_name = fin.readline().split(": ")[1][:-1]
experimenter_contact = fin.readline().split(": ")[1][:-1]
software_title = fin.readline().split(": ")[1][:-1]
software_type = fin.readline().split(": ")[1][:-1]
software_authors = fin.readline().split(": ")[1][:-1]
software_description = fin.readline().split(": ")[1][:-1]
software_repository = fin.readline().split(": ")[1][:-1]
software_preferredcitationid = fin.readline().split(": ")[1][:-1]
additional_tables = fin.readline().split(": ")[1][:-1]
columns = fin.readline().split("=(")[1][:-2]

new_file.write(columns + '\n')
Lines = fin.readlines()

for line in Lines:
	new_file.write(line)


# runs writer
test = Writer()

variables = [magic_size, version, table_namespace, genome_assembly, xyz_unit, lab_name, experimenter_contact, software_title, software_type, software_authors, software_description, software_repository, software_preferredcitationid, additional_tables, columns]
test.write_core_header(variables)

"""metadata_size = len(variables)
core_df = pd.read_csv("without_headers.csv")
fin2 = open("test.FISH", "a")
fin.append(core_df)"""