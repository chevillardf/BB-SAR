# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

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