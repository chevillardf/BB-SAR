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

def has_substr(mol_smi, substr):
	try:
		if Chem.MolFromSmiles(mol_smi).HasSubstructMatch(Chem.MolFromSmarts(substr)):
			has_substr = True
		else:
			has_substr = False
	except:
		has_substr = False
	return has_substr