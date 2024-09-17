from rdkit import Chem

def has_substr(mol_smi, substr):
	try:
		if Chem.MolFromSmiles(mol_smi).HasSubstructMatch(Chem.MolFromSmarts(substr)):
			has_substr = True
		else:
			has_substr = False
	except:
		has_substr = False
	return has_substr