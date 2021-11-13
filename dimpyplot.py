#!/usr/bin/env python3

import subprocess
import os

### Define LigPlot+ environment here
LigPlus_path = '/Your/Application/Path/LigPlus'
components_cif = f'{LigPlus_path}/params/components.cif' # Location of components.cif
ligplot_plus = f'{LigPlus_path}/lib/exe_mac64/' # Location of your LigPlus executable folder

### Define the chains you want to process here
wkdir = 'test_pdb'
chain1 = 'A'
chain2 = 'B'

def dimplot(filename):
	"""Emulates running the LigPlot+ DIMPLOT algorithm. Rewriting as a CLI to allow for a batch mode."""
	file_prefix = filename.strip('.pdb')[0]

	# Run HBadd
	subprocess.check_call(['{}hbadd'.format(ligplot_plus), filename, components_cif, '-wkdir', './'], shell = False)


	# Run HBplus
	subprocess.check_call(['{}hbplus'.format(ligplot_plus), '-L', '-h', '2.90', '-d', '3.90', '-N', filename, '-wkdir', './'], shell = False)


	# Run HBplus again
	subprocess.check_call(['{}hbplus'.format(ligplot_plus), '-L', '-h', '2.70', '-d', '3.35', filename, '-wkdir', './'], shell = False)


	# Run dimer
	subprocess.check_call(['{}dimer'.format(ligplot_plus), filename, chain1, chain2], shell = False)


	# Run dimhtml
	subprocess.check_call(['{}dimhtml'.format(ligplot_plus), 'none', '-dimp', '-dir', './', '-flip', '-ctype', '1'], shell = False)


	# Run ligplot
	subprocess.check_call([
		'{}ligplot'.format(ligplot_plus), 'dimplot.pdb', '-wkdir', './',
		'-prm', '{}/lib/params/dimplot.prm'.format(LigPlus_path), '-ctype', '1'
		], shell = False)


	# Rename trashy files
	files_to_rename = [_ for _ in os.listdir(wkdir) if
		'dimplot.' in _[0:8] or 'ligplot.' in _[0:8]]

	for file_to_rename in files_to_rename:
		subprocess.check_call([
			'mv',
			file_to_rename,
			'./{}.{}'.format(filename.split('.pdb')[0], file_to_rename)
			])

def main():
	"""Main function."""
	# Get list of pdb files in the directory
	pdb_files = [_ for _ in os.listdir(wkdir) if
 		(_[-4:] == '.pdb') and ('dimplot' not in _) and ('ligplot' not in _)]
	print(pdb_files)
	for pdb_file in pdb_files:
		os.chdir(wkdir)
		dimplot(filename=pdb_file)
	quit()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\n\nGoodbye!\n\n')
