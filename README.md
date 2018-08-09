# reptiles
Compare which reptile species are available in [NCBI's Taxonomy Browser](https://www.ncbi.nlm.nih.gov/Taxonomy/taxonomyhome.html/) to those in the [Reptile Database](http://reptile-database.org/) (RDB).

- [Purpose](#purpose)
- [Usage](#usage)
- [Input details](#input-details)
- [Output details](#output-details)
- [Technical notes](#technical-notes)
- [Questions?](#questions)
- [Acknowledgements](#acknowledgements)


## Purpose
The Reptile Database (RDB) primarily classifies species based on morphology, whereas NCBI primarily classifies species based on genetic sequencing. We sought to examine the similarities and differences between these two databases. In the case of discrepancies, we classify them in order to help with resolving and preventing these discrepancies in the future.


## Usage

To run the script, you need [Python 2.7](https://www.python.org/download/releases/2.7/), the [re](https://docs.python.org/2/library/re.html) module (installed by default), and the [xlsxwriter](https://xlsxwriter.readthedocs.io/) module (usually not installed by default).

Follow these steps:

1. Download the RDB data `reptile_database_names.txt` from this repository. 

2. Download NCBI's taxonomy data. This can be done via their [FTP server](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/). Download `taxdmp.zip`, unzip it, and keep `names.dmp` and `nodes.dmp`. 

3. Run `NCBI_reptiles.py` in the same folder as the above files.

## Input details

There are 3 input files. One is from RDB and the other two are from NCBI.
* `reptile_database_names.txt` is a tab-delimited file consisting of two columns. The left column contains reptile synonyms, and the right column contains the associated current reptile names. The header row should be `any_name\tcurrent_name\n`. The file from July 2018 is included in this repository.
  * _"current reptile name"_ in this context refers to names that RDB considers to the primary, scientific name
  * _"reptile synonym"_ in this context refers to names that RDB considers to be a secondary name. Each synonym is associated with a current reptile name.
* `names.dmp` maps NCBI taxonomy IDs to their scientific names
* `nodes.dmp` maps NCBI taxonomy IDs to their parent taxonomy IDs and their rank (e.g. species, phylum)

## Output details

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

* `NCBI_reptile_list.txt`: a list of NCBI reptile species names and their taxonomy ids.
* `reptile_comparison.xlsx`: an Excel workbook containing separate worksheets with lists of reptiles. There are three worksheets:
  * `RDB_only` is a list of reptile names in RDB but not NCBI.
  * `common` is a list of reptile names in both RDB and NCBI. It includes each reptile's NCBI taxonomy ID.
  * `NCBI_only` is a list of reptile names in NCBI but not RDB. It includes each reptile's NCBI taxonomy ID. It additionally adds a third column for "kin", i.e. if the reptile name is one of the special categories from the console output ([see above](#console-output)). Finally, if the NCBI species matches only a synonym in RDB, the fourth column matches the current name associated with the synonym in RDB.
An example of `reptile_comparison.txt` is included in this repository.

## Technical notes

* The script only looks for NCBI reptile species, not subspecies. When comparing NCBI species with RDB, the script only chooses RDB species that are from the current name column, and that are binomials (two words). Otherwise, the RDB species is classified as a synonym.
* None of these categories overlap: "aff.", "cf.", "sp.", hybrid, numbered, synonym. If there is a reptile that is in two of the previous categories, it enters only the highest category according to the following rank: synonym > "aff." = "cf." = "sp." = hybrid > numbered.

## Questions?
For any questions, please email Akhil (email address written at top of `NCBI_reptiles.py`).

## Acknowledgements
* Peter Uetz, for the idea and with fixing errors.
* Detlef Leipe, for help with sorting through NCBI's database and with fixing errors.
