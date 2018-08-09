# reptiles
Compare which reptile species are available in [NCBI's Taxonomy Browser](https://www.ncbi.nlm.nih.gov/Taxonomy/taxonomyhome.html/) to those in the [Reptile Database](http://reptile-database.org/) (RDB).

## Purpose
(To be written)

## Usage

To run the script, you need [Python 2.7](https://www.python.org/download/releases/2.7/), the [re](https://docs.python.org/2/library/re.html) module (installed by default), and the [xlsxwriter](https://xlsxwriter.readthedocs.io/) module.

Follow these steps:

1. Have the RDB data ready in a tab-delimited file called `reptile_database_names.txt`. This file should have two columns, with a header row of `any_name\tcurrent_name`. 

2. Download NCBI's taxonomy data. This can be done via their [FTP server](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/). Download `taxdmp.zip`, unzip it, and keep `names.dmp` and `nodes.dmp`. 

3. Run `NCBI_reptiles.py` in the same folder as the above files.


## Output

### Console output

The console will output counts of:
* reptiles in RDB but not NCBI
* reptiles in both RDB and NCBI
* reptiles in NCBI but not RDB

Within species that are in NCBI but not RDB, it additionally prints counts of:
* species labeled "aff.", "cf.", or "sp."
* hybrid species
* species that contain numerical digits
* species that are classified as synonyms in RDB

### File output

Two new files are created.

* `NCBI_reptile_list.txt`: a list of NCBI reptile species and their taxonomy ids.
* `Reptile comparison.xlsx`: an Excel workbook containing separate worksheets with lists of reptiles. The worksheets correspond to the counts outputted to the console.

### Technical notes

* The script only looks for NCBI reptile species, not subspecies. When comparing NCBI species with RDB, the script only chooses RDB species that are from the current name column, and that are binomials (two words). Otherwise, the RDB species is classified as a synonym.
* None of these categories overlap: "aff.", "cf.", "sp.", hybrid, numbered, synonym. If there is a reptile that is in two of the previous categories, it enters only the highest category according to the following rank: synonym > "aff." = "cf." = "sp." = hybrid > numbered.

## Questions?
For any questions, please email Akhil (email address written at top of `NCBI_reptiles.py`).

## Acknowledgements
* Peter Uetz, for the idea.
* Detlef Leipe, for help with sorting through NCBI's database.
