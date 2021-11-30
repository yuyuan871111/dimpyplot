# Dimpyplot
A Python frontend to the LigPlot+ program, allowing batch processing of Protein Data Bank (PDB) files through the DIMPLOT algorithm.

## Requirements
1. UNIX / Linux / MacOS X
2. Python 3.7
3. Install LigPlot+ from the EBI: http://www.ebi.ac.uk/thornton-srv/software/LigPlus/
4. Download `components.cif` from the PDB: ftp://ftp.wwpdb.org/pub/pdb/data/monomers/components.cif  
5. Ability to 'cd' in the Terminal  

## How to Use
1. Copy dimpyplot.py to the directory containing the PDB files you want to process (the working directory), or your $PATH.
2. Run: you can run either ligplot, dimplot or both.  
    * `python3 dimpyplot.py --fullreport` *(ligplot + dimplot)* 
    * `python3 dimpyplot.py --ligplot`  
    * `python3 dimpyplot.py --dimplot`  

    default parameteres:
    > --LigPlus_path `/Users/yuyuan/bin/LigPlus`  
    > --components_cif `/Users/yuyuan/bin/LigPlus/data/components.cif`   
    > --ligplot_plus `/Users/yuyuan/bin/LigPlus/lib/exe_mac64/`   
    > --wkdir `./test_pdb`   
    > --chain1 `A`  
    > --chain2 `B`

3. This tool will process every PDB file in the working directory, generating new PDB files of the interaction surface, and PostScript visulization files.
### Notes
* You can run `python3 dimpyplot.py -h` for help.  

# Dimpyplot + Chord Plot
With dimpyplot, you will get a series of interactions between two chains of protein complex. Chord plot is a kind of visualization to show which residues play an important role between protein interfaces.  
* Red line represents H-bond interactions.  
* Green-tone line represents hydrophobic interactions.  


## Requirements
1. Any requirements from dimpyplot  
2. Python3 packages: `pandas`, `os` and dependencies  
3. R 3.6.1 or above  
4. R packages: `magrittr=1.5`, `circlize=0.4.13`, `optparse=1.7.1` and dependencies  

## How to Use
**Run in python3**: you can change variables to fit to your pdb chain & name.  
* `wkdir`: destinate where your pdb located.  
* `pdb_name`: indicate which pdb your want to analysis in your pdb.
* `chain1`: which chain do you want to analysis in your pdb.
* `chain2`: the other chain you want to anlysis in your pdb.
* `chain1_name`: you can name as you want.
* `chain2_name`: you can name as you want.

Python3 script:
```
import os
from dimpyplot_chord import dimplot_chord

wkdir = './test_pdb'                #change here
pdb_name = '7a91_delta_npt_noPBC'   #change here
chain1 = 'A'                        #change here
chain2 = 'B'                        #change here
chain1_name = 'hACE2'               #change here
chain2_name = 'S1RBD'               #change here

dimplot_chord(wkdir, pdb_name, chain1, chain2, chain1_name, chain2_name)
```

