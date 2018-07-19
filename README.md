# reptiles
Compare which reptile species are available in [NCBI's Taxonomy Browser](https://www.ncbi.nlm.nih.gov/Taxonomy/taxonomyhome.html/) to those in the [Reptile Database](http://reptile-database.org/) (RDB).

## Usage

Follow these steps:

1. Have the RDB data ready in a tab-delimited file called `reptile_database_names.txt`. This file should have two columns, with a header row of `synonym\tcurrent_species_or_subspecies_name`. 

2. Download NCBI's taxonomy data. This can be done via their [FTP server](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/). Download `taxdmp.zip`, unzip it, and keep `names.dmp` and `nodes.dmp`. 

3. Run `NCBI_reptiles.py` in the same folder as the above files.


## Output

### Console output

Counts of:
* reptiles in RDB but not NCBI
* reptiles in both RDB and NCBI
* reptiles in NCBI but not RDB

Within species that are in NCBI but not RDB, it additionally counts:
* species labeled "aff.", "cf.", or "sp."
* hybrid species
* species that contain numerical digits
* species that are classified as synonyms in RDB

### File output

Two new files are created.

* `NCBI_reptile_list.txt`: a list of NCBI reptile species and their taxonomy ids.
* `Reptile comparison.xlsx`: an Excel workbook containing separate worksheets with lists of reptiles. The worksheets correspond to the counts outputted to the console.


## Questions?
For any questions, please email Akhil (email address written in scripts).

## Acknowledgements
* Peter Uetz, for the idea.
* Detlef Leipe, for help with sorting through NCBI's database.
