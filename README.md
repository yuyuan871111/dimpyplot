# dimpyplot
A Python frontend to the LigPlot+ program, allowing batch processing of Protein Data Bank (PDB) files through the DIMPLOT algorithm.

# Requirements
1. UNIX / Linux / MacOS X
2. Python 3.7
3. LigPlot+ from the EBI: http://www.ebi.ac.uk/thornton-srv/software/LigPlus/
4. components.cif from the PDB: ftp://ftp.wwpdb.org/pub/pdb/data/monomers/components.cif  
5. Ability to 'cd' in the Terminal

# How to Use
1. Copy dimpyplot.py to the directory containing the PDB files you want to process (the working directory), or your $PATH.
2. Run: `python3 dimplot`  
    default:
    ```
    dimpyplot.py --LigPlus_path /Users/yuyuan/bin/LigPlus \  
                 --components_cif /Users/yuyuan/bin/LigPlus/data/components.cif \  
                 --ligplot_plus /Users/yuyuan/bin/LigPlus/lib/exe_mac64/ \  
                 --wkdir ./test_pdb \  
                 --chain1 A --chain2 B
    ```
6. Dimpyplot will process every PDB file in the working directory, generating new PDB files of the interaction surface, and PostScript files of the LigPlots.
