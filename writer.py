import struct

class Writer:
	# converts txt to binary, writes into a binary file
	def __init__(self):
		self.file = open("test.FISH", "wb")
	
	def write_core_header(self, header_list):
		# writes the metadata for DNA core table

		# byte sizes for header categories
		sizes = ["15s", "10s", "6s", "30s", "30s", "20s", "20s", "80s", "100s", "60s", "100s", "175s", "66s"]

		# writes into file
		self.file.write(struct.pack("4s", magic_size.encode('utf-8')))
		self.file.write('\n'.encode('utf-8'))
		self.file.write(struct.pack("f", version))
		self.file.write('\n'.encode('utf-8'))

		counter = 0
		for row in header_list[2:]:
			self.file.write(struct.pack(sizes[counter], row.encode("utf-8")))
			self.file.write('\n'.encode('utf-8'))
			counter+=1
			
# reads the input csv file
fin = open("test.csv", "r")

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

# runs writer
test = Writer()

test.write_core_header([magic_size, version, table_namespace, genome_assembly, xyz_unit, lab_name, experimenter_contact, software_title, software_type, software_authors, software_description, software_repository, software_preferredcitationid, additional_tables, columns])