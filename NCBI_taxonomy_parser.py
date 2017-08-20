#################################
#                               #
#  NCBI_taxonomy_parser.py      #
#  Akhil Garg, garga4@vcu.edu   #
#  Updated 2017-03-17           #
#                               #
#################################

'''
This script takes in three files: 
    1. reptile_database_names.txt (by Dr. Uetz)
    2. synonym_output.txt (output from https://www.ncbi.nlm.nih.gov/Taxonomy/TaxIdentifier/tax_identifier.cgi)
    3. current_name_output.txt (output from https://www.ncbi.nlm.nih.gov/Taxonomy/TaxIdentifier/tax_identifier.cgi)
    
The script then outputs two files:
    1. current_name_taxa.txt
    2. RDB_like_taxa.txt
    
Each of these files contains: the current reptile name, a list of synonyms for that name, and the tax id (if it exists)
Both of these output files contain the same information, but in different formats
'''

# Imports
from __future__ import print_function
from operator import itemgetter

# Dictionary to store reptile names and synonyms
reptiles = {}

# Get reptile names from Uetz's file and put into dictionary
with open("reptile_database_names.txt") as RDB:
    for line in RDB:
        # The first name before the tab is the synonym
        # The second is the current name
        line         = line.strip().split("\t")
        synonym      = line[0]
        current_name = line[1]
        
        # Add to dictionary 
        
        # If the current name exists already in the dictionary, append to it
        if current_name in reptiles: reptiles[current_name].append(synonym)
        # Otherwise, create a new dictionary entry
        else: reptiles[current_name] = [synonym]
        
# List to store each line of NCBI's output
NCBI_current_name_taxa = []
# For the synonyms, use a dictionary instead because it has faster lookup
NCBI_synonym_taxa = {}

# Get current reptile names from file and put into list of lists
with open("current_name_output.txt") as f:
    for line in f:
        
        # Ignore blank lines and the first line
        if line == "\n" or line.startswith("code"): continue
        
        # Each of the other lines is broken into four parts:
            # Code
            # Name provided
            # Preferred name
            # Lineage
        
        # Split the line across tabs and |
        append_list = line.split("\t|\t")
        # Strip the line of the "\n" at the end
        append_list[-1] = append_list[-1].strip()
        # Make the preferred name truly blank if necessary
        if append_list[2] == " ": append_list[2] = ""
        # Parse the last line into yet another nested list
        append_list[-1] = append_list[-1].split(" ")

        # Add the list to the current names list
        NCBI_current_name_taxa.append(append_list)

# For the synonyms, use a dictionary instead because it has faster lookup
with open("synonym_output.txt") as f:
    for line in f:
        
        # Ignore blank lines and the first line
        if line == "\n" or line.startswith("code"): continue
        
        # Each of the other lines is broken into four parts:
            # Code
            # Name provided
            # Preferred name
            # Lineage
        
        # Strip the line of its newline at the end
        line = line.strip()
        # Split the line across tabs and |
        line = line.split("\t|\t")
        
        # Get the synonym provided to NCBI
        synonym = line[1]
        
        # Get the tax id
        synonym_tax_id = line[-1].split(" ")[0]

        # Add the list to the synonyms dictionary
        NCBI_synonym_taxa[synonym] = synonym_tax_id
        
        
# Figure out which reptiles have tax ids and write to file
with open("current_name_taxa.txt", "w") as f:
    
    # Write a header
    f.write("Name given to NCBI (current name)\tList of synonyms\tTax ID\tNotes\n")
    
    # Write all of the species name and their tax ids
    # Sort the list first based on current_name (list position 1)
    # Sorting code from http://stackoverflow.com/questions/17555218/python-how-to-sort-a-list-of-lists-by-the-fourth-element-in-each-list
    for name in sorted(NCBI_current_name_taxa, key = itemgetter(1)): 

        # This if statement is to handle preferred names
        # name[2] is the preferred name
        # The if statement checks that name[2] is not blank
        if name[2]: 
            
            # Set a flag True so that we can make a note that we changed the current_name
            preferred_name_flag = True
            
        # This is the case where there is no preferred name
        else: preferred_name_flag = False
        
        # Check if a tax id exists
        # name[-1][0] gives the tax id 
            # the tax id is the last element of the list, and the first element of the sublist
            # if not name[-1][0] checks if the tax id is blank
        if not name[-1][0]:
            
            # Assume no tax id until proven otherwise
            tax_id = "no tax id"
            # Create a false flag, for note-taking later
            synonym_tax_id_flag = False
            
            # If no name is found, try searching synonyms
            for syn in reptiles[name[1]]:
                try:
                    # Checkes if there's a value (tax id) associated with the synonym
                    if NCBI_synonym_taxa[syn]:
                        # If there is a tax id found, save it
                        tax_id = NCBI_synonym_taxa[syn]
                        # Save the synonym corresponding to the tax id
                        synonym_with_taxid = syn
                        # Make a note that we found tax id using synonym
                        synonym_tax_id_flag = True
                        # If we find one tax id we don't need to look for others
                        break
                except KeyError:
                    print ("Key error. Probably some encoding error in " + syn)
        # If the current name has a tax id, save it
        else:
            tax_id = name[-1][0]
            # The synonym flag has to be set to false since we aren't using synonyms
            synonym_tax_id_flag = False

        
        # name[1] is the species name we gave to NCBI
        f.write (name[1] + "\t")
        # str(reptiles[name[1]]) gives the list of synonyms
        f.write (str(reptiles[name[1]]) + "\t")
        # And also write the tax_id
        f.write (tax_id)
        # Make a note of preferred name
        if preferred_name_flag: 
            f.write("\tNote--different preferred name available: " + name[2])
        # Make a note of synonym tax id
        if synonym_tax_id_flag:
            f.write("\tNote--used synonym tax id: " + synonym_with_taxid)

        # Then move onto the next line
        f.write ("\n")

# Create another version of the above file that more closely matches the original RDB file
with open("RDB_like_taxa.txt", "w") as f:
    
    # Write a header
    f.write("Synonym\tcurrent_species_or_subspecies_name\tTax ID\tNotes\n")
    
    # Write all of the species name and their tax ids
    # Sort the list first based on current_name (list position 1)
    # Sorting code from http://stackoverflow.com/questions/17555218/python-how-to-sort-a-list-of-lists-by-the-fourth-element-in-each-list
    for name in sorted(NCBI_current_name_taxa, key = itemgetter(1)): 

        # This if statement is to handle preferred names
        # name[2] is the preferred name
        # The if statement checks that name[2] is not blank
        if name[2]: 
            
            # Set a flag True so that we can make a note that we changed the current_name
            preferred_name_flag = True
            
        # This is the case where there is no preferred name
        else: preferred_name_flag = False
        
        # Check if a tax id exists
        # name[-1][0] gives the tax id 
            # the tax id is the last element of the list, and the first element of the sublist
            # if not name[-1][0] checks if the tax id is blank
        if not name[-1][0]:
            
            # Assume no tax id until proven otherwise
            tax_id = "no tax id"
            # Create a false flag, for note-taking later
            synonym_tax_id_flag = False
            
            # If no name is found, try searching synonyms
            for syn in reptiles[name[1]]:
                try:    
                    # Checkes if there's a value (tax id) associated with the synonym
                    if NCBI_synonym_taxa[syn]:
                        # If there is a tax id found, save it
                        tax_id = NCBI_synonym_taxa[syn]
                        # Save the synonym corresponding to the tax id
                        synonym_with_taxid = syn
                        # Make a note that we found tax id using synonym
                        synonym_tax_id_flag = True
                        # If we find one tax id we don't need to look for others
                        break
                        
                except KeyError:
                    print ("Key error. Probably some encoding error in " + syn)

        # If the current name has a tax id, save it
        else: 
            tax_id = name[-1][0]
            # The synonym flag has to be set to false since we aren't using synonyms
            synonym_tax_id_flag = False
        
        for synonym in reptiles[name[1]]:
            # Write the synonym first
            f.write(synonym + "\t")
            # Then write the NCBI name (name[1]) and tax_id
            f.write (name[1] + "\t")
            f.write (tax_id)
            # Make a note of preferred name
            if preferred_name_flag: 
                f.write("\tNote--different preferred name available: " + name[2])
            # Make a note of synonym tax id
            if synonym_tax_id_flag:
                f.write("\tNote--used synonym tax id: " + synonym_with_taxid)
            
            # Then move onto the next line
            f.write ("\n")
            
