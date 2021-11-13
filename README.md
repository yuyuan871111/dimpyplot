# dimpyplot
A Python frontend to the LigPlot+ program, allowing batch processing of Protein Data Bank (PDB) files through the DIMPLOT algorithm.

# Requirements
1. UNIX / Linux / MacOS X
2. Python 3.7
3. LigPlot+ from the EBI: http://www.ebi.ac.uk/thornton-srv/software/LigPlus/
4. components.cif from the PDB: ftp://ftp.wwpdb.org/pub/pdb/data/monomers/components.cif
4. Ability to 'cd' in the Terminal

# How to Use
1. Copy dimpyplot.py to the directory containing the PDB files you want to process (the working directory), or your $PATH.
2. Edit lines 6 and 7 to tell dimpyplot.py where to find LigPlus on your computer.
3. Edit lines 10 and 11 to tell dimpyplot.py which protein chains you want to study.
4. In the Terminal, cd to the working directory.
5. Do 'python3 dimpyplot.py'
6. Dimpyplot will process every PDB file in the working directory, generating new PDB files of the interaction surface, and PostScript files of the LigPlots.
