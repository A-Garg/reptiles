# reptiles
Compare which reptile species are available in [NCBI's Taxonomy Browser](https://www.ncbi.nlm.nih.gov/Taxonomy/taxonomyhome.html/) to those in the [Reptile Database](http://reptile-database.org/) (RDB).

# Usage
The data from RDB is stored in `reptile_database_names.txt`. Follow these steps:

## RDB_column_splitter.py
The first thing to do is run `RDB_column_splitter.py` in the same folder as `reptile_database_names.txt`. This produces two files, `synonym_list.txt` and `current_name_list.txt`. 

## NCBI's status for each reptile
Take each of the output files from `RDB_column_splitter.py` and submit them to NCBI's [Taxonomy name/id Status Report Page](https://www.ncbi.nlm.nih.gov/Taxonomy/TaxIdentifier/tax_identifier.cgi). When submitting each file, be sure to check **full taxid lineage** beneath the form.

Save the output files as `synonym_output.txt` and `current_name_output.txt`, respectively, in the same folder as the other files.

## NCBI_taxonomy_parser.py
Run `NCBI_taxonomy_parser.py`. This script will parse through `synonym_output.txt` and `current_name_output.txt` to produce `current_name_taxa.txt` and `RDB_like_taxa.txt`, which will be useful for the next script.

## Taxonomy_tree.py
Before running this script, download NCBI's taxonomy data. This can be done via their [FTP server](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/). Download `taxdmp.zip`, unzip it, and keep `names.dmp` and `nodes.dmp`.

You can then run `Taxonomy_tree.py`.

## Output

You'll get four files as output:

1. NCBI_reptile_list.txt
2. NCBI_only_reptiles.txt
3. common_reptiles.txt
4. RDB_only_reptiles.txt
    
All of these files are tab/newline-separated. Each line contains the current reptile, a tab, followed by the taxid.
    
NCBI_reptile_list.txt contains all NCBI reptiles.
NCBI_only_reptiles.txt contains reptiles in NCBI but not in RDB.
common_reptiles.txt contains reptiles common to both NCBI and RDB.
RDB_only_reptiles.txt contains reptiles that are in RDB but not NCBI.

# More documentation
More documentation for each script is available in the first few lines of each script.

# Acknowledgements
* Peter Uetz, for the idea.
* Detlef Leipe, for help with sorting through NCBI's database.
