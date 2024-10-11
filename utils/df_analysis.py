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

import pandas as pd
from molecules.models import Molecule
import numpy as np

def describe_bb_ppties_df(dict, properties):
    # bbs/b_id
    # TODO: do we need this since stats are precalculated now?
    dfs = []

    for ppty in properties:
        df = pd.DataFrame.from_dict(dict)
        stat_df = df.groupby('bb_id')[ppty].agg(['min', 'max', 'median', 'mean', 'std','count']).reset_index()
        stat_df['property'] = ppty
        stat_df['mean'] = stat_df['mean']
        stat_df['std_deviation'] = stat_df['std']
        stat_df['cv'] = (stat_df['std_deviation'] / stat_df['mean']) * 100
        stat_df.rename(columns={ppty: 'value'}, inplace=True)

        if ppty in ['HLM', 'MDR1_efflux'] and stat_df['cv'].notna().all():
            stat_df['score'] = stat_df['median'] + stat_df['cv']
        elif stat_df['cv'].notna().all():
            stat_df['score'] = stat_df['median'] - stat_df['cv']
        else:
            stat_df['score'] = None

        dfs.append(stat_df)

    result_df = pd.concat(dfs, ignore_index=True)                             
    return result_df

def describe_bbs_ppty_df(df, bb_id_col, q_bb_id, bbs_id, property, no_single=False):
    # molecules/suggest/mol_id/property
    results = []
    bbs_trio_id = [bb_id for bb_id in bbs_id if bb_id != q_bb_id]

    grouped = df.groupby(bb_id_col)
    for name, group in grouped:
        if no_single and len(group) == 1:
            continue
        if name == q_bb_id:
            continue

        combined_bbs = sorted(bbs_trio_id + [name])
        #TODO: update so it take series as input
        combination_exists = Molecule.objects.filter(bbs_id=combined_bbs).exists()

        stats = group[property].describe()
        molecule = Molecule.objects.filter(bbs_id=combined_bbs).first()
        mol_id = molecule.mol_id if molecule and combination_exists else None
        ppty_value = getattr(molecule, property, None) if molecule and combination_exists else None
        
        entry = {
            'bb_id_col': name,
            'count': stats['count'],
            'min': stats['min'],
            'max': stats['max'],
            'median': group[property].median(),
            'mean': group[property].mean(),
            'std_deviation': group[property].std(),
            'cv': (group[property].std() / group[property].mean()) * 100,
            'exists': combined_bbs if combination_exists else None,
            'v_bbs_id': combined_bbs,
            'mol_id': mol_id,
            'ppty_value': ppty_value
        }
        
        if property in ['HLM', 'MDR1_efflux'] and not np.isnan((group[property].std()/group[property].mean()) * 100):
            entry['score'] = group[property].median() + ((group[property].std()/group[property].mean()) * 100)
        elif not np.isnan((group[property].std()/group[property].mean()) * 100):
            entry['score'] = group[property].median() - ((group[property].std()/group[property].mean()) * 100)

        results.append(entry)

    results_df = pd.DataFrame(results)
    results_df['ppty_value'].replace({pd.NA: None, np.nan: None}, inplace=True)

    return results_df

def describe_ppty_bbs_df(df, group_col, property):
    # display_bbs_ppty_boxPlot/
    grouped = df.groupby(group_col)
    results = []

    for name, group in grouped:
        stats = group[property].describe()
        entry = {
            'bb_id': name,
            'count': stats['count'],
            'min': stats['min'],
            'max': stats['max'],
            'median': group[property].median(),
            'mean': group[property].mean(),
            'std_deviation': group[property].std(),
            'cv': (group[property].std()/group[property].mean()) * 100,
        }
        if property in ['HLM', 'MDR1_efflux'] and not np.isnan((group[property].std()/group[property].mean()) * 100):
            entry['score'] = group[property].median() + ((group[property].std()/group[property].mean()) * 100)
        elif not np.isnan((group[property].std()/group[property].mean()) * 100):
            entry['score'] = group[property].median() - ((group[property].std()/group[property].mean()) * 100)
        else:
            entry['score'] = None
        
        results.append(entry)

    return pd.DataFrame(results)

