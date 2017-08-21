#################################
#                               #
#  RDB_column_splitter.py       #
#  Akhil Garg, garga4@vcu.edu   #
#  Updated 2017-03-17           #
#                               #
#################################

'''
A very simple column splitter for a two-column tab-delimited file.

This script takes in the file reptile_database_names.txt by Peter Uetz.
    reptile_database_names.txt is a tab-delimited file 
    that maps reptile synonyms to their current species or subspecies name.

The script outputs two files, synonym_list.txt and current_name_list.txt.
    Each file contains one column from reptile_database_names.txt. 
    The entries are sorted alphabetically and duplicates are removed.
'''

# For removing files so that new files can be created 
### This is necessary because these files will appended to
import os

# Get reptile names from reptile_database_names.txt and put into sets
# I am using sets in order to remove duplicates
with open("reptile_database_names.txt") as RDB:
    synonym_list      = set()
    current_name_list = set()
    
    for line in RDB:
        # The first name before the tab is the synonym
        # The second is the current name
        line         = line.strip().split("\t")
        synonym      = line[0]
        current_name = line[1]
        
        synonym_list.add(synonym)
        current_name_list.add(current_name)
        
# Convert sets to lists and alphabetize them
# (The reason they were sets in the first place was to remove duplicates)
synonym_list = sorted(list(synonym_list))
current_name_list = sorted(list(current_name_list))


# Make sure these files are blank so they can be appended to
try: 
    os.remove("current_name_list.txt")
    os.remove("synonym_list.txt")
# This exception occurs when the file is not found by windows
# For when the output file already doesn't exist
except WindowsError:
    pass
    
# Write the names to files, separated by newline characters  
with open("synonym_list.txt","a") as synonyms:
    
    for reptile in synonym_list:
        synonyms.write(reptile)
        synonyms.write("\n")

with open("current_name_list.txt","a") as current_names:
    for reptile in current_name_list:
        current_names.write(reptile)
        current_names.write("\n")
            
