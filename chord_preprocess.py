#!/usr/bin/env python3

# import packages
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='chord plot preprocessing', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

## Define working directory, chains and which to plot
parser.add_argument('-w','--wkdir', type=str, default='./test_pdb', help='working directory')
parser.add_argument('-n','--pdb_name', type=str, default='7a91_delta_npt_noPBC', help='Define chains for analysis - chain1')
parser.add_argument('-c1', '--chain1', type=str, default='A', help='Define chains for analysis - chain1')
parser.add_argument('-c2', '--chain2', type=str, default='B', help='Define chains for analysis - chain2')
parser.add_argument('-c1n','--chain1_name', dest='chain1_name', help='input your name as you want (chain1)')
parser.add_argument('-c2n','--chain2_name', dest='chain2_name', help='input your name as you want (chain2)')

parser.set_defaults(chain1_name='hACE2', chain2_name='S1RBD')
args = parser.parse_args()

# define variables
pdb_name = args.pdb_name
wkdir = args.wkdir
chain_dict = {
    args.chain1:args.chain1_name,
    args.chain2:args.chain2_name
}

def hhb_process(wkdir, pdb_name):
    ## read data
    df = pd.read_table(f'{wkdir}/{pdb_name}.dimplot.hhb')
    df.drop(0, axis=0, inplace = True)

    ## clean data
    df_clean = pd.DataFrame(
        df['ligplot.hhb output:'].str.split('\ +').tolist(),
        columns=['donor_aa', 'donor_chain', 'donor_pos', 'donor_atom', 
                'receptor_aa', 'receptor_chain', 'receptor_pos', 'receptor_atom',
                'distance', '_']
        )
    df_clean.drop('_', axis=1, inplace=True)
    df_clean.replace({"donor_chain":chain_dict, "receptor_chain":chain_dict}, inplace =True)
    df_clean['donor_aapos'] = df_clean[['donor_aa', 'donor_pos']].agg(''.join, axis=1)
    df_clean['receptor_aapos'] = df_clean[['receptor_aa', 'receptor_pos']].agg(''.join, axis=1)

    # save csv 
    df_clean[['donor_chain', 'donor_aapos', 'donor_aa', 'donor_pos', 'donor_atom',
            'receptor_chain', 'receptor_aapos', 'receptor_aa', 'receptor_pos', 'receptor_atom', 
            'distance']].to_csv(f'{wkdir}/{pdb_name}.dimplot.hhb.csv', index=False)

def nnb_process(wkdir, pdb_name):
    ## read data
    df = pd.read_table(f'{wkdir}/{pdb_name}.dimplot.nnb')
    df.drop(0, axis=0, inplace = True)

    ## clean data
    df_clean = pd.DataFrame(
        df['ligplot.nnb output:'].str.split('\ +').tolist(),
        columns=['atom1_aa', 'atom1_chain', 'atom1_pos', 'atom1_atom', 
                'atom2_aa', 'atom2_chain', 'atom2_pos', 'atom2_atom',
                'distance', '_']
        )
    df_clean.drop('_', axis=1, inplace=True)
    df_clean.replace({"atom1_chain":chain_dict, "atom2_chain":chain_dict}, inplace =True)
    df_clean['atom1_aapos'] = df_clean[['atom1_aa', 'atom1_pos']].agg(''.join, axis=1)
    df_clean['atom2_aapos'] = df_clean[['atom2_aa', 'atom2_pos']].agg(''.join, axis=1)

    # save csv 
    df_clean[['atom1_chain', 'atom1_aapos', 'atom1_aa', 'atom1_pos', 'atom1_atom',
            'atom2_chain', 'atom2_aapos', 'atom2_aa', 'atom2_pos', 'atom2_atom', 
            'distance']].to_csv(f'{wkdir}/{pdb_name}.dimplot.nnb.csv', index=False)

if __name__ == '__main__':
    try:
        hhb_process(wkdir, pdb_name)
        nnb_process(wkdir,pdb_name)
    except:
        print("Please check your input.")
    