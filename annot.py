import os
import sys
from bs4 import BeautifulSoup


def readlines(filename):
	"""function: takes in a .annot and reads the lines
	   Input: a filename (with quotations)
	   Output: string with file contents read
	"""
	if ".annot" in filename: 
		file = open(filename, "r")
		contents = file.read()
		file.close()
		return contents
	else:
		print("Perhaps you mistyped!")
		file = input("Please enter the .annot file you would like to convert? ")
		readline(file)


def parse(contents):
	"""function: uses Beautiful Soup to parse xhtml bodies of annotations
	   Input: parsed text (contents), and an export filename (with quotations)
	   Output: metadata and string with annotations stripped of any XHTML tags
	"""
	soup = BeautifulSoup(contents, 'lxml-xml')
	title = soup.find('title').get_text()
	author = soup.find('creator').get_text() 
	#publisher = soup.find('publisher').get_text()
	annotations = soup.find_all('annotation')

	# YAML metadata
	metadata ="""---
	title: {}
	author: {}
	---

	""".format(title, author)
	return metadata, annotations


def export(metadata, annotations, filename):
	"""function: takes in metadata and a string with annotations stripped of any XHTML tags (annotations),
				 and writes each annotation to a markdown file, which is saved as filename.md
	   Input: metadata, annotations soup file and an export filename
	   Output: none.
	"""
	export = []
	export.append(metadata)

	# parse through each annotation, enumerating each 
	for i, annotation in enumerate(annotations):
	    date = annotation.date.get_text()
	    citation = annotation.target.find('text').get_text()
	    export.append('{}. "{}" ({})\n\n'.format(i,citation, date))
	    note = annotation.content.find('text')
	    if note:
	        export.append('> > ' + note.get_text() + "\n\n")
	
	with open(filename + ".md", "w", encoding = "utf-8") as result:
		result.writelines(export)


def main():
	print("Welcome to the .annot to Markdown converter")
	file = input("What is the .annot file you would like to convert? ")
	exportFile = input("What would you like to call the .md file? ")
	contents = readlines(file)
	metadata, annnotations = parse(contents)
	print(metadata)
	print(annnotations)
	export(metadata, annnotations, exportFile)
	print("Thank you for using this tool!")


if __name__== "__main__":
 main()
