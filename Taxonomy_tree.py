#################################
#                               #
#  Taxonomy_tree.py             #
#  Akhil Garg, garga4@vcu.edu   #
#  Updated 2017-03-17           #
#                               #
#################################

'''
This script takes in the files
    1. names.dmp (from taxdmp.zip from ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/)
    2. nodes.dmp (from taxdmp.zip from ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/)
    3. RDB_like_taxa.txt (from script NCBI_taxonomy_parser.py)

Each file contains one column from reptile_database_names.txt. 
'''

from __future__ import print_function

# Reptiles are located under 3 tax ids, all of which fall under cellular organisms
# 8504: reptiles with overlapping scales
# 8493: crocodylians
# 8459: turtles, tortoises, and terrapins
reptile_taxids = [8504, 8493, 8459]

''' Processing NCBI taxonomy files '''

# Dictionaries to store parts of taxonomy tree
name_taxid           = {}
taxid_scientificname = {}
taxid_parent         = {}
taxid_rank           = {}

# Process names corresponding to tax ids
with open("names.dmp") as f:
    
    # Counter will help track progress
    lines_processed = 0
    print ("\nProcessing names.dmp...")
    
    for line in f:
    
        lines_processed += 1
        
        # Print a message every 100,000 rows
        if (lines_processed % 100000 == 0):
             print("Processing line " + str(lines_processed) + "...")
        
        # Extract information from each line
        line = line.strip()
        line = line.split("\t|\t")
        
        taxid     = int(line[0])
        name      = line[1]
        name_type = line[3][0:-2]
    
        # Map common names to tax id
        name_taxid[name] = taxid
        
        # Map tax id to scientific name
        if name_type == "scientific name":
            taxid_scientificname[taxid] = name

# Process taxonomy tree            
with open("nodes.dmp") as f:
    
    lines_processed = 0
    print ("\nProcessing nodes.dmp...")

    for line in f:
    
        # Counter will help track progress
        lines_processed += 1
        # Print a message every 100,000 rows
        if (lines_processed % 100000 == 0):
             print("Processing line " + str(lines_processed) + "...")
        
        # Extract information from each line
        line = line.strip()
        line = line.split("\t|\t") 
        
        taxid        = int(line[0])
        parent_taxid = int(line[1])
        rank         = line[2]
        
        taxid_parent[taxid] = parent_taxid
        taxid_rank  [taxid] = rank
        
print ("Number of tax ids: " + str(len(taxid_parent)))

# Example code: if you wanted to count the number of tax ids labelled "order"
#print (sum([1 for rank in taxid_rank.values() if rank == "order"]))

''' Functions to work with NCBI taxonomy data '''

def list_parents(tax_id): 
    '''
    Given a tax id
    Returns a list of parent tax ids, including the original tax_id
    '''
    
    parent_list  = [tax_id]
    
    while True:
        parent = taxid_parent[tax_id]
        
        # 1 is the tax id of the root, so we can stop then.
        if parent == 1: break
        else: 
            parent_list.append(parent)
            
            # To make the while loop continue, do the same thing on the parent
            tax_id = parent
    
    return (parent_list)
    
    
def list_a_rank(rank):
    '''
    Pick one of:
        superkingdom
        kingdom
        phylum
        class
        order
        family
        genus
        species
        subspecies
        (and also some other sub-_____ ranks)
    Returns the number of tax_ids with that rank
    '''
    
    rank_list = []
    
    for t, r in taxid_rank.iteritems():
        if r == rank: rank_list.append(t)
        
    return rank_list

def is_parent(tax_id, parent):
    '''
    Given a tax id of a child and a parent tax id
    Returns True if the second tax id is a parent
    Otherwise returns False
    '''
    
    # 1 is the root, so it is guaranteed to be found
    if parent == 1 and tax_id != 1: return True

    # use a while loop to continue searching until we find what we are looking for
    while True:
        # find the taxid of the parent
        parent_taxid = taxid_parent[tax_id]

        # if it is found, exit the function
        if parent_taxid == parent:
            return True
        
        # if we reach the top of the tree, we can break out of the loop
        elif parent_taxid == 1:
            return False
            
        # if not, then set the current taxid to be the parent taxid and go round the loop again
        else:
            tax_id = parent_taxid
            
            
''' Finding all NCBI reptiles '''

# Collect all of the reptile species and subspecies into a list     
print ("\nCollecting reptile species...")       
NCBI_reptile_species = [] 

# Create a list of all of the species and subspecies in the taxonomy tree
all_species = list_a_rank("species") + list_a_rank("subspecies")

# Counter to keep track of progress
species_processed = 0

# Iterate through every species, verify that it is a reptile
# If the species is a reptile, add it to the NCBI reptile list
for tax_id in all_species:
    
    species_processed += 1
    # Print a message every 100,000 lines
    if (species_processed % 100000 == 0):
         print ("Processing line " + str(species_processed) + "...")
         print (str(float(species_processed)/len(all_species)*100) + "% complete.")

    # Check if the species is a reptile
    for reptile_family in reptile_taxids:
        if is_parent(tax_id, reptile_family):
            NCBI_reptile_species.append(tax_id)

print ("100.00% complete.\n")            
print (str(len(NCBI_reptile_species)) + " reptile species and subspecies collected.")

# Write all of the NCBI reptile species and subspecies to file
print ("Writing them to NCBI_reptile_list.txt...")

with open("NCBI_reptile_list.txt", "w") as f:
    f.write("Scientific name\tTax ID\n")
    for reptile in NCBI_reptile_species:
        f.write(taxid_scientificname[reptile])
        f.write("\t")
        f.write(str(reptile))
        f.write("\n")

print ("Done writing to file.")

''' Collecting RDB reptiles '''

print ("\nGetting list of RDB tax ids...")

RDB_taxid_list = []

# Note we could also easily use current_name_taxa.txt as the input file
with open("RDB_like_taxa.txt") as f:
    for line in f:
        
        # Ignore the first line
        if line == "Synonym	current_species_or_subspecies_name	Tax ID	Notes\n":
            continue
            
        # Parse line
        line   = line.strip().split("\t")
        tax_id = line[2]
        

        if tax_id == "no tax id": continue
        else: RDB_taxid_list.append(int(tax_id))

print ("Done.\n")

''' Comparing NCBI reptile list to RDB reptile list '''

# Find NCBI only reptiles
print ("Generating list of NCBI only reptiles \
and writing to 'NCBI_only_reptiles.txt'")
        
# The difference of two sets 
    #gives the elements in the first set that aren't in the second set        
NCBI_only_reptiles = set(NCBI_reptile_species) - set(RDB_taxid_list)

print ("There are " + str(len(NCBI_only_reptiles)) + " tax ids in NCBI but not in RDB.")

NCBI_only_reptiles = sorted(list(NCBI_only_reptiles))

with open("NCBI_only_reptiles.txt", "w") as f:
    f.write("Scientific name\tTax ID\n")
    for reptile in NCBI_only_reptiles:
        f.write(taxid_scientificname[reptile])
        f.write("\t")
        f.write(str(reptile))
        f.write("\n")
        
print ("Done writing to file.\n")

# Find reptiles that are both in RDB and in NCBI
print ("Generating list of reptiles both in RDB and NCBI \
and writing to 'common_reptiles.txt'")
        
# The & sign between two sets gives their intersection (common elements) 
common_reptiles = set(NCBI_reptile_species) & set(RDB_taxid_list)

print ("There are " + str(len(common_reptiles)) + " tax ids common to NCBI and RDB.")

common_reptiles = sorted(list(common_reptiles))

with open("common_reptiles.txt", "w") as f:
    f.write("Scientific name\tTax ID\n")
    for reptile in common_reptiles:
        f.write(taxid_scientificname[reptile])
        f.write("\t")
        f.write(str(reptile))
        f.write("\n")
        
print ("Done writing to file.\n")

# Find reptiles that are in RDB but not in NCBI
# This occurs when the 
print ("Generating list of reptiles in RDB but not in NCBI \
  and writing to 'RDB_only_reptiles.txt'")
        
# The difference between two sets gives elements in the first set that are not in the second 
RDB_only_reptiles = set(RDB_taxid_list) - set(NCBI_reptile_species)

print ("There are " + str(len(RDB_only_reptiles)) + " tax ids in RDB but not NCBI.")

RDB_only_reptiles = sorted(list(RDB_only_reptiles))

with open("RDB_only_reptiles.txt", "w") as f:
    f.write("Scientific name\tTax ID\n")
    for reptile in RDB_only_reptiles:
        f.write(taxid_scientificname[reptile])
        f.write("\t")
        f.write(str(reptile))
        f.write("\n")
        
print ("Done writing to file.")