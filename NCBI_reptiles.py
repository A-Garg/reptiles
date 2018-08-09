#################################
#                               #
#  NCBI_reptiles.py             #
#  Akhil Garg, garga4@vcu.edu   #
#  Updated 2018-08-08           #
#                               #
#################################

'''
This script takes data from NCBI's taxonomy database and the Reptile Database (RDB).
    Of the NCBI taxonomy data, it finds species that are classified as reptiles.
    It then compares RDB reptiles to those in NCBI.

This script takes in 3 files:
    1. names.dmp (from taxdmp.zip from ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/)
    2. nodes.dmp (from taxdmp.zip from ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/)
    3. reptile_database_names.txt from RDB

It outputs 2 files: NCBI_reptile_list.txt and reptile_comparison.xlsx, 
    plus some counts about the data.
    
    NCBI_reptile_list.txt: a list of NCBI reptile species and their taxonomy ids.
    reptile_comparison.xlsx: an Excel workbook containing separate worksheets with
                             lists of reptiles. The worksheets correspond to the 
                             counts outputted to the console.
'''



''' Imports '''


import re #regex
import xlsxwriter #to create Excel workbooks



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
    Returns a list of tax_ids with that rank
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


# Reptiles are located under 3 root tax ids, all of which fall under cellular organisms
# 8504:    reptiles with overlapping scales
# 1294634: crocodylians
# 8459:    turtles, tortoises, and terrapins
reptile_taxids = [8504, 1294634, 8459]


# Collect all of the reptile species and subspecies into a list     
print ("\nCollecting reptile species...")       
NCBI_reptile_taxids = []

# Create a list of all of the species and subspecies in the taxonomy tree
# Ignore subspecies. If needed, subspecies can be re-activated
species_list    = list_a_rank("species")
#subspecies_list = list_a_rank("subspecies")
all_species =  species_list #+ subspecies_list

# Counter to keep track of progress
species_processed = 0

# Iterate through every species, verify that it is a reptile
# If the species is a reptile, add it to the NCBI reptile list
for tax_id in all_species:
    
    species_processed += 1
    # Print a message every 100,000 lines
    if (species_processed % 100000 == 0):
         print ("Processing line " + str(species_processed) + "...")
         print (str(round(float(species_processed)/len(all_species)*100,2)) + "% complete.")

    # Check if the species is a reptile
    for reptile_family in reptile_taxids:
        if is_parent(tax_id, reptile_family):
            NCBI_reptile_taxids.append(tax_id)
            break

print ("100.0% complete.\n")            
print (str(len(NCBI_reptile_taxids)) + " reptile species and subspecies collected.")

# Store and write all of the NCBI reptile species to a set and to a file
print ("Writing them to NCBI_reptile_list.txt...")

NCBI_reptile_species = set()

with open("NCBI_reptile_list.txt", "w") as f:
    f.write("Scientific name\tTax ID\n")
    for reptile_taxid in NCBI_reptile_taxids:
    
        reptile_name = taxid_scientificname[reptile_taxid]
        NCBI_reptile_species.add(reptile_name)
        
        f.write(reptile_name)
        f.write("\t")
        f.write(str(reptile_taxid))
        f.write("\n")

print ("Done writing to file.\n")



''' Collect RDB reptiles '''


# cn means current name
RDB_cn_species  = set()
RDB_synonyms    = set()
# Dictionary to map synonyms to current names
RDB_syn_cn_dict = {}

with open('reptile_database_names.txt') as f:
    for line in f:
    
        line = line.strip()
        
        # Ignore the header row
        if line == 'any_name\tcurrent_name': continue
        
        line = line.split('\t')
        RDB_synonyms.add(line[0])
        
        # Only add binomials to RDB_cn_species
        # Some synonym columns are blank, and these can be ignored
        # Blank columns will generate an IndexError
        try:
            if line[1].count(' ') == 1: 
                RDB_cn_species.add(line[1])
            # Add trinomials and such to synonyms
            else: RDB_synonyms.add(line[1])
            
            # Map synonym to current name 
            # (even if current name isn't a binomial)
            RDB_syn_cn_dict[line[0]] = line[1]

        except IndexError:
            continue
        
        

        

''' Compare NCBI and RDB reptiles '''


# Counts in each set
print('There are {:5d} current name species in RDB.'.format(len(RDB_cn_species)))
print('There are {:5d} synonyms in RDB.'.format(len(RDB_synonyms)))
print('There are {:5d} reptile species in NCBI.'.format(len(NCBI_reptile_species)))


# Comparing the sets
RDB_only_species  = sorted(list(RDB_cn_species - NCBI_reptile_species))
NCBI_only_species = sorted(list(NCBI_reptile_species - RDB_cn_species))
common_species    = sorted(list(RDB_cn_species & NCBI_reptile_species))

print('There are {:5d} species in RDB but not in NCBI.'.format(len(RDB_only_species)))
print('There are {:5d} species in NCBI but not in RDB.'.format(len(NCBI_only_species)))
print('There are {:5d} species in both RDB and NCBI.'  .format(len(common_species)))
print('\n')



''' Count various NCBI-only taxon types '''


print('Within NCBI only species...')

# Create variables to store these cases of reptiles
aff      = []
cf       = []
BOLD     = []
hybrid   = []
sp       = []
numbered = []
synonym  = []

# List of NCBI only reptile "kins" that are not numbered
not_number_list = ["aff.", "cf.", " x ", "sp."]

for name in NCBI_only_species:

    # Check for synonym in RDB
    # If found, break out of the loop and don't count it as one of the others,
    # instead count it as a synonym
    if name in RDB_synonyms:
        synonym.append(name)
        continue
    
    if "aff." in name: aff.append(name)
    if "cf."  in name: cf.append(name)
    # Ignore BOLD because it's a subset of "sp."
    #if "BOLD" in name: BOLD.append(name)
    if " x "  in name: hybrid.append(name)
    if "sp."  in name: sp.append(name)
    
    # Count other numbered species (regex search for one or more digits)
    # But don't count any of the previously-counted species
    if not any([x in name for x in not_number_list]) and re.search(".*\d+.*", name):
        numbered.append(name)

# Count number of reptiles that fit into these special "kin" categories
# For use later for counts of various categories        
subtotal = len(aff) + len(cf) + len(hybrid) + len(sp) + len(numbered) + len(synonym)
        
print("Number of aff.:        {:5d}".format(len(aff)))
print("Number of cf.:         {:5d}".format(len(cf)))
#print("Number of BOLDs:      {:5d}".format(len(BOLD)))
print("Number of hybrids:     {:5d}".format(len(hybrid)))
print("Number of sp.:         {:5d}".format(len(sp)))
print("Number of numbereds:   {:5d}".format(len(numbered)))
print("Number of synonyms:    {:5d}".format(len(synonym)))

print('Note: sp. includes BOLD species, which are not counted separately.\n')

print('Subtotal of above: {}'.format(subtotal))
print('Others: {NCBI_only_tot} - {subtot} = {others}'.format(NCBI_only_tot = len(NCBI_only_species),
                                                             subtot = subtotal,
                                                             others = len(NCBI_only_species) - subtotal))




''' Write data to Excel workbook '''


# Initialize worksheets
workbook = xlsxwriter.Workbook('reptile_comparison.xlsx')
RDB_only_worksheet  = workbook.add_worksheet('RDB_only')
common_worksheet    = workbook.add_worksheet('common')
NCBI_only_worksheet = workbook.add_worksheet('NCBI_only')


# Write reptiles to worksheet

# Write header rows for each worksheet
RDB_only_worksheet.write (0,0,'reptile_name')

common_worksheet.write   (0,0,'reptile_name')
common_worksheet.write   (0,1,'tax_id')

NCBI_only_worksheet.write(0,0,'reptile_name')
NCBI_only_worksheet.write(0,1,'tax_id')
NCBI_only_worksheet.write(0,2,'kin')
NCBI_only_worksheet.write(0,3,'synonym')



# Now write reptiles to worksheets
row = 1
for reptile in RDB_only_species:
    RDB_only_worksheet.write(row, 0, reptile)
    row += 1
row = 1

for reptile in common_species:
    common_worksheet.write(row, 0, reptile)
    common_worksheet.write(row, 1, name_taxid[reptile])
    row += 1
row = 1

for reptile in NCBI_only_species:
    NCBI_only_worksheet.write(row, 0, reptile)
    NCBI_only_worksheet.write(row, 1, name_taxid[reptile])
    # Add a third column for special kin designations
    if reptile in aff:
        NCBI_only_worksheet.write(row, 2, 'aff')
    if reptile in cf:
        NCBI_only_worksheet.write(row, 2, 'cf')
    if reptile in hybrid:
        NCBI_only_worksheet.write(row, 2, 'hybrid')
    if reptile in sp:
        NCBI_only_worksheet.write(row, 2, 'sp')
    if reptile in numbered:
        NCBI_only_worksheet.write(row, 2, 'numbered')  
    if reptile in synonym:
        NCBI_only_worksheet.write(row, 2, 'synonym')       
        NCBI_only_worksheet.write(row, 3, RDB_syn_cn_dict[reptile])        
    row += 1

    
workbook.close()
