from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D

def get_mol_svg(mol_smi, mol_id, mol_type, project_name, series_name):
    mol = Chem.MolFromSmiles(mol_smi)
    d2d = rdMolDraw2D.MolDraw2DSVG(360,240)
    d2d.drawOptions().addStereoAnnotation = True
    #d2d.drawOptions().comicMode = True
    d2d.DrawMolecule(mol)
    d2d.FinishDrawing()
    svg = d2d.GetDrawingText()

    if mol_type == 'bb':
        with open('media/bbs/'+str(project_name)+'/'+str(series_name)+'/'+str(mol_id)+'.svg', 'w') as f:
            f.write(svg)
    else:
        with open('media/mols/'+str(project_name)+'/'+str(series_name)+'/'+str(mol_id)+'.svg', 'w') as f:
            f.write(svg)

    return None