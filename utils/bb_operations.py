import pandas as pd
import numpy as np
from itertools import combinations
from molecules.models import Molecule
from django.conf import settings

unfavorable_gain_ppties = settings.UNFAVORABLE_GAIN_PPTIES

def get_bb_combo(n, list_of_bbs_id, df, ppty):
    # display_bbs_ppty_boxPlot/
    bb_combo_df = pd.DataFrame(columns=['bbs_combo', 'count', 'min', 'max', 'median', 'cv', 'score'])
    checked = set() # already checked combinations
    result = {}
    i = 0

    for bbs_id in list_of_bbs_id: # loop over all bbs_id and retrieve all combo sharing n elements
        cbs = combinations(bbs_id, n)
        for comb in cbs:
            if comb not in checked:
                groups = [l for l in list_of_bbs_id if all(i in l for i in comb)]
                if len(groups) > 1:
                    result[comb] = groups
                checked.add(comb)

    for k, v in result.items(): # for each combo, get stats
        lst = []
        for val in v:
            lst.append(str(val))
        filt = df['bbs_id'].astype(str).isin(lst)
        filt_df = df[filt]
        min_df = filt_df[ppty].min()
        max_df = filt_df[ppty].max()
        median_df = filt_df[ppty].median()
        count = filt_df[ppty].size
        mean = filt_df[ppty].mean()
        std = filt_df[ppty].std()
        cv = (filt_df[ppty].std() / filt_df[ppty].mean()) * 100
        if ppty in ['HLM', 'MDR1_efflux'] and cv != None:
            score = median_df + cv
        elif cv != None:
            score = median_df - cv
        else:
            score = None
            
        bb_combo_df.loc[i] = [k, count, min_df, max_df, median_df, cv, score]
        i += 1

    return bb_combo_df

def combo_contains_all_tags(combo, tags):
    return all(bb[0] in tags for bb in combo)

def combine_with_bb_id(combo, bb_id):
    return sorted(list(combo) + [bb_id])

def does_combination_exist(combo):
    #TODO: update so it take series as input
    combined_bbs = sorted(list(combo))
    return Molecule.objects.filter(bbs_id=combined_bbs).exists()

def get_bb_id(mol, bb_tag):
    # view: display_bbs_ppty_boxPlot
    return getattr(mol, f'{bb_tag}_id', None)

def calculate_n_bbs(mols, bb_tag):
    # view: display_bbs_ppty_boxPlot
    unique_bb_ids = set()
    for mol in mols:
        bb_id = get_bb_id(mol, bb_tag)
        if bb_id is not None:
            unique_bb_ids.add(bb_id)
    n_bbs = len(unique_bb_ids)
    return n_bbs

def get_n_mmps_from_bb_id(df, bb_id, ppty): # TODO: is this use?
    bb_tag = bb_id[0]+'_id'
    df = format_df_for_combos(df, bb_id, ppty)
    grouped = df.groupby(bb_tag)['combo'].apply(set)

    if bb_id not in grouped.index:
        print(f"bb_tag + ' ' {bb_id}' not found in the DataFrame.")
    else:
        results = []
        for other_bb_id in grouped.index:
            if bb_id != other_bb_id:
                n_mmps = len(grouped[bb_id].intersection(grouped[other_bb_id]))
                results.append({'ref_bb_id': bb_id, bb_tag: other_bb_id, 'n_mmps': n_mmps})

        result_df = pd.DataFrame(results)
        result_df = result_df.drop(columns='ref_bb_id')
        result_df.columns = ['bb_id', 'n_mmps']
    
    return result_df.sort_values(by='n_mmps', ascending=False)

def format_df_for_combos(df, bb_id, ppty):
    """
    df = [ppty,'A_id','B_id','C_id','D_id']
    df_out = [ppty, bb_id. combo]
    """
    bb_type = bb_id[0]
    df = df[[ppty,'A_id','B_id','C_id','D_id']]
    columns_to_include = [col for col in ['A_id', 'B_id', 'C_id', 'D_id'] if col[0] != bb_type]
    df['combo'] = df[columns_to_include].fillna('').astype(str).agg(''.join, axis=1)
    #df['combo'] = df[columns_to_include].agg(''.join, axis=1)
    df = df.drop(columns=columns_to_include)

    return df

def get_mmps_from_bb_ids(df, bb_ids, ppty, n_bb_tags):
    # for a given pair bbs_ids = [bb1, bb2] return all trio sharing this pair
    column_name = None

    if n_bb_tags == 4:
        if any(id.startswith('A') for id in bb_ids):
            column_name = 'A_id'
        elif any(id.startswith('B') for id in bb_ids):
            column_name = 'B_id'
        elif any(id.startswith('C') for id in bb_ids):
            column_name = 'C_id'
        elif any(id.startswith('D') for id in bb_ids):
            column_name = 'D_id'

        if column_name is not None:
            filt = df[column_name].isin(bb_ids)
            df = df[filt]
            # Remove all rows with duplicate [A, B, C, D] combinations
            df = df.drop_duplicates(subset=['A_id', 'B_id', 'C_id', 'D_id'])
            combo_column = [col for col in ['A_id', 'B_id', 'C_id', 'D_id'] if col != column_name]
            df['combo'] = df[combo_column[0]] + df[combo_column[1]] + df[combo_column[2]]
            # Filtering out singletons: Keep only rows where 'combo' appears more than once
            df = df.groupby('combo').filter(lambda x: len(x) > 1)
            
            return df[[ppty, 'combo', 'A_id', 'B_id', 'C_id', 'D_id']]
        else:
            return None
    else: # n_bb_)tags = 3
        if any(id.startswith('A') for id in bb_ids):
            column_name = 'A_id'
        elif any(id.startswith('B') for id in bb_ids):
            column_name = 'B_id'
        elif any(id.startswith('C') for id in bb_ids):
            column_name = 'C_id'
        
        if column_name is not None:
            filt = df[column_name].isin(bb_ids)
            df = df[filt]
            df = df.drop_duplicates(subset=['A_id', 'B_id', 'C_id'])
            combo_column = [col for col in ['A_id', 'B_id', 'C_id'] if col != column_name]
            df['combo'] = df[combo_column[0]] + df[combo_column[1]]
            df = df.groupby('combo').filter(lambda x: len(x) > 1)
                
            return df[[ppty, 'combo', 'A_id', 'B_id', 'C_id']]
        else:
            return None
    
def get_mmps_stats(df, ppty, pivot_column, bb1_id):
    df = df[['combo', ppty, pivot_column]]
    agg_df = df.groupby(['combo', pivot_column])[ppty].mean().reset_index()
    pivot_df = agg_df.pivot(index='combo', columns=pivot_column, values=ppty).reset_index()
    pivot_df.columns = [f'{ppty}_{col}' if col != 'combo' else col for col in pivot_df.columns]
    bb1_col = f'{ppty}_{bb1_id}'
    cols = [col for col in pivot_df.columns if col not in ['combo', bb1_col]]
    pivot_df = pivot_df[['combo', bb1_col] + cols]
    
    if len(pivot_df.columns) > 2:
        pivot_df['Fold_Change'] = pivot_df[pivot_df.columns[2]] / pivot_df[pivot_df.columns[1]] 
    else:
        pivot_df['Fold_Change'] = np.nan

    return pivot_df

def score_mmp(df, bb_ids, ppty, n_bb_tags):
    """
    df = [ppty,'A_id','B_id','C_id','D_id']
    bb_ids = [bb1_id, bb2_id]
    get_mmps_from_bb_ids = [ppty, 'combo', 'A_id', 'B_id', 'C_id', 'D_id']
    """
    
    df = get_mmps_from_bb_ids(df, bb_ids, ppty, n_bb_tags)
    df = get_mmps_stats(df, ppty,  bb_ids[0][0]+'_id', bb_ids[0])
    mean = df['Fold_Change'].agg('mean')
    std = df['Fold_Change'].agg('std')
    n_mmps = len(df)
    if ppty not in unfavorable_gain_ppties:
        n_positive_mmps = df[df['Fold_Change'] > 1]['Fold_Change'].count()
    else:
        n_positive_mmps = df[df['Fold_Change'] < 1]['Fold_Change'].count()
    ratio_positive_mmps = n_positive_mmps / n_mmps
    
    return [round(mean, 2), round(std, 2), n_positive_mmps, round(ratio_positive_mmps,2)]

def get_mmps_from_bb_id(df, bb_id, ppty):
    """
    df = [ppty,'A_id','B_id','C_id','D_id']
    format_df_for_combos = [ppty, bb_id. combo]
    grouped = [bb_id: list_of_combo]
    result_df = [bb_id, n_mmps]
    """
    bb_tag = bb_id[0]+'_id'
    df = format_df_for_combos(df, bb_id, ppty)
    grouped = df.groupby(bb_tag)['combo'].apply(set)

    if bb_id not in grouped.index:
        print(f"bb_tag + ' ' {bb_id}' not found in the DataFrame.")
        result_df = pd.DataFrame(columns=['bb_id', 'n_mmps'])

    else:
        results = []
        for other_bb_id in grouped.index:
            if bb_id != other_bb_id:
                n_mmps = len(grouped[bb_id].intersection(grouped[other_bb_id]))
                results.append({'ref_bb_id': bb_id, bb_tag: other_bb_id, 'n_mmps': n_mmps})

        result_df = pd.DataFrame(results)
        result_df = result_df.drop(columns='ref_bb_id')
        result_df.columns = ['bb_id', 'n_mmps']
        result_df = result_df[result_df['n_mmps'] > 0]
    
    return result_df.sort_values(by='n_mmps', ascending=False)

def get_mmps_from_bb_id_with_scores(original_df, bb1_id, ppty, n_bb_tags):
    """
    original_df= [ppty,'A_id','B_id','C_id','D_id']
    bb_mmps_df = [bb_id, n_mmps]
    bb_mmps_df_out = [bb_id, count, mean, n_positive_mmps, ...]
    """

    bb_mmps_df = get_mmps_from_bb_id(original_df, bb1_id, ppty)
    if bb_mmps_df.empty:
        bb_mmps_df = pd.DataFrame(columns=['mean', 'std', 'n_positive_mmps', 'n_negative_mmps', 'ratio_positive_mmps', 'ratio_negative_mmps'])

    # Iterate through each row in bb_mmps_df and append scores
    else:
        for index, row in bb_mmps_df.iterrows():
            bb2_id = row['bb_id']
            scores = score_mmp(original_df, [bb1_id, bb2_id], ppty, n_bb_tags)
            bb_mmps_df.loc[index, 'mean'] = scores[0]
            bb_mmps_df.loc[index, 'std'] = scores[1]
            bb_mmps_df.loc[index, 'n_positive_mmps'] = scores[2]
            bb_mmps_df.loc[index, 'ratio_positive_mmps'] = scores[3]
        bb_mmps_df['n_positive_mmps'] = bb_mmps_df['n_positive_mmps'].astype(int)
        bb_mmps_df['ratio_positive_mmps'] = (bb_mmps_df['ratio_positive_mmps']*100).astype(int)
        if ppty in unfavorable_gain_ppties:
            bb_mmps_df['mean'] = round(1/bb_mmps_df['mean'],2)
    return bb_mmps_df