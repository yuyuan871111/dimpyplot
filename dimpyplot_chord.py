import os
def dimplot_chord(wkdir, pdb_name, chain1, chain2, chain1_name, chain2_name):
    try:
        print("Dimplot calculation...")
        os.system(f"python3 dimpyplot.py --wkdir {wkdir} --chain1 {chain1} --chain2 {chain2} --dimplot >> {wkdir}/run.log")
        
        print("dimplot.hhb and dimplot.nnb preprocessing...")
        os.system(f"python3 chord_preprocess.py -w {wkdir} -n {pdb_name} -c1 {chain1} -c2 {chain2} -c1n {chain1_name} -c2n {chain2_name} >> {wkdir}/run.log")
        
        print("Chord diagram plotting...")
        os.system(f"Rscript chord_rplot.r -w {wkdir} -n {pdb_name} --chain1_name {chain1_name} --chain2_name {chain2_name} >> {wkdir}/run.log")
        
        print("____ complete ____")

    except Exception as e:
        print(e)


