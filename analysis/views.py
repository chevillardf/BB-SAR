from django.shortcuts import render, redirect
from django.db.models import Q
from bbs.models import BB
from molecules.models import Molecule
from utils.bb_operations import get_mmps_from_bb_ids, get_mmps_stats, get_mmps_from_bb_id_with_scores, get_bb_combo, combo_contains_all_tags, combine_with_bb_id, does_combination_exist
from utils.data_visualization import plot_mmps_ppty_relPlot, plot_mmps_pptyFold_barPlot, get_bbs_boxPlot, get_duo_swarmPlot
from utils.db_operations import get_project_series_from_session
from utils.df_analysis import describe_ppty_bbs_df
from utils.proj_settings import ppties_bb_rows_project,  mols_ppties_headers_project, mols_ppties_project, bbs_ppties_scores_header_project, bbs_ppties_scores_project
import pandas as pd
import numpy as np

def analysis_home(request):
    series_name = get_project_series_from_session(request)
    project = get_project_series_from_session(request)
    n_bb_tags = get_project_series_from_session(request)
        
    if series_name:
        series_name = series_name.series_name
        project = project.project
        n_bb_tags = n_bb_tags.n_bb_tags
    else:
        return redirect('projects_home')
    
    if n_bb_tags == 4:
        bb_tags = ['A', 'B', 'C', 'D']
        combos = ['Duo', 'Trio']
    else:
        bb_tags = ['A', 'B', 'C']
        combos = ['Duo']
    properties = ppties_bb_rows_project.get(project.project_name, [])
    
    context = {
        'bb_tags': bb_tags,
        'properties': properties, 
        'combos': combos,
        'series_name':series_name,
        'project_name':project
    }

    return render(request, 'analysis/analysis_home.html', context)

# TODO: pass combos with option to remove a BB tag from solution

def generate_combos(request):
    project = get_project_series_from_session(request).project
    series_name = get_project_series_from_session(request).series_name
    n_bb_tags = get_project_series_from_session(request).n_bb_tags
    combo = request.GET.get('combo') or request.POST.get('combo')
    property = request.GET.get('property') or request.POST.get('property')
    bb_id = request.GET.get('bb_id')
    included_bb_id = request.POST.get('included_bb_id')
    excluded_bb_id = request.POST.get('excluded_bb_id')
    
    bb_letter = bb_id[0] if bb_id else None
    if n_bb_tags == 4:
        all_bbs = ['A', 'B', 'C', 'D']
    else:
        all_bbs = ['A', 'B', 'C']
    remaining_bbs = [bb for bb in all_bbs if bb != bb_letter]

    if not property:
        return redirect('analysis_home')

    n = 2 if combo == 'Duo' else 3

    mols = Molecule.objects.filter(**{f'{property}__isnull': False}, series=series_name).values()
    df = pd.DataFrame.from_records(mols)
    if df.empty:
        return redirect('analysis_home')
    if n_bb_tags == 4:
        df = df.dropna(subset=['A_id', 'B_id', 'C_id', 'D_id'], how='any')
        all_bb_ids = df[['A_id', 'B_id', 'C_id', 'D_id']].values.tolist()
    else:
        df = df.dropna(subset=['A_id', 'B_id', 'C_id'], how='any')
        all_bb_ids = df[['A_id', 'B_id', 'C_id']].values.tolist()
    bb_combo_df = get_bb_combo(n, all_bb_ids, df, property)
    
    filt = bb_combo_df['bbs_combo'].apply(lambda combo: combo_contains_all_tags(combo, remaining_bbs))
    bb_combo_df = bb_combo_df[filt]
    
    if included_bb_id:
        if ',' in included_bb_id:
            included_bb_ids = included_bb_id.split(',') if ',' in included_bb_id else [included_bb_id]
            included_bb_ids = [bb_id.strip() for bb_id in included_bb_ids]
            filt = bb_combo_df['bbs_combo'].apply(lambda x: any(bb in x for bb in included_bb_ids))
        else:
            filt = bb_combo_df['bbs_combo'].apply(lambda x: included_bb_id in x)
        bb_combo_df = bb_combo_df[filt]

    if excluded_bb_id:
        pass

    # remove already existing mols
    if bb_id:
        bb_combo_df['bb_ids'] = bb_combo_df['bbs_combo'].apply(lambda x: combine_with_bb_id(x, bb_id))
        filt = bb_combo_df['bb_ids'].apply(does_combination_exist)
        bb_combo_df = bb_combo_df[~filt]

    context = {
        'property': property,
        'combo': combo,
        'bb_combo_df': bb_combo_df,
        'series_name':series_name,
        'project_name':project
    }

    return render(request, 'analysis/combos_results.html', context)

def generate_mmps(request, property=None, bb_id=None):
    series_name = get_project_series_from_session(request).series_name
    project = get_project_series_from_session(request).project
    n_bb_tags = get_project_series_from_session(request).n_bb_tags
    property = request.GET.get('property') if request.method == 'GET' else request.POST.get('property')
    bb_id = request.GET.get('bb_id') if request.method == 'GET' else request.POST.get('bb_id')

    if not property or not bb_id:
        return redirect('analysis_home')

    bb = BB.objects.filter(bb_id=bb_id, series__series_name=series_name).first()
    if not bb:
        return redirect('analysis_home')  
    
    mols = Molecule.objects.filter(**{f'{property}__isnull': False}, series=series_name).values()
    df = pd.DataFrame.from_records(mols)
    df = get_mmps_from_bb_id_with_scores(df, bb_id, property, n_bb_tags)
    context = {
        'property': property, 
        'bb_id':bb_id, 
        'df':df,
        'series_name':series_name,
        'project_name':project
    }

    return render(request, 'analysis/mmps_results.html', context)

def get_mmps_ppty_relplot(request):
    series_name = get_project_series_from_session(request).series_name
    project = get_project_series_from_session(request).project
    n_bb_tags = get_project_series_from_session(request).n_bb_tags
    property = request.GET.get('property')
    bb1_id = request.GET.get('bb1_id')
    bb2_id = request.GET.get('bb2_id')
    bb_ids = [bb1_id, bb2_id]
    bb_tag = bb1_id[0]+'_id'

    if not property or not bb1_id or not bb2_id:
        return redirect('analysis_home')

    mols = Molecule.objects.filter(**{f'{property}__isnull': False}, series=series_name).values()
    df = pd.DataFrame.from_records(mols)
    df = get_mmps_from_bb_ids(df, bb_ids, property, n_bb_tags)
    plot_mmps_ppty_relPlot(df, bb_tag, property)
    df = get_mmps_stats(df, property, bb_tag, bb1_id)
    column_headers = df.columns.tolist()
    plot_mmps_pptyFold_barPlot(df, property, column_headers[1], column_headers[2]) 
    context = {
        'property': property, 
        'bb_ids': bb_ids, 
        'df':df, 
        'bb_tag':bb_tag, 
        'headers': column_headers, 
        'property_bb1_id': column_headers[1], 
        'property_bb2_id': column_headers[2],
        'series_name':series_name,
        'project_name':project
    }
    return render(request, 'analysis/mmp_home.html', context)

def display_bbs_ppty_boxPlot(request, bb_tag=None, property=None, min_data_points=None):
    series_name = get_project_series_from_session(request).series_name
    n_bb_tags = get_project_series_from_session(request).n_bb_tags
    project = get_project_series_from_session(request).project
    if bb_tag is None and property is None:
        bb_tag = request.POST['bb_tag']
        property = request.POST['property']
        min_data_points = request.POST['min_data_points']
    property_median = property + '_median'

    if n_bb_tags == 4:
        mols = Molecule.objects.filter(**{f'{property}__isnull': False},series=series_name).exclude(Q(A_id__isnull=True) | Q(B_id__isnull=True) | Q(C_id__isnull=True) | Q(D_id__isnull=True))
    else:
        mols = Molecule.objects.filter(**{f'{property}__isnull': False},series=series_name).exclude(Q(A_id__isnull=True) | Q(B_id__isnull=True) | Q(C_id__isnull=True))
    df = pd.DataFrame.from_records(mols.values())
    
    if df.empty:
        return redirect('analysis_home')
    
    df = df[df['A_id'].notna()]
    min_data_points = int(min_data_points)
    df = df.groupby(bb_tag+'_id').filter(lambda x: len(x) >= min_data_points) # keep only min_data_points data points per bb
    n_bbs = df[bb_tag+'_id'].nunique()
    n_mols = len(df.index)
    bb_ids = df[bb_tag+'_id'].unique().tolist()

    bbs = BB.objects.filter(**{f'{property_median}__isnull': False},series__series_name=series_name, bb_tag=bb_tag, bb_id__in=bb_ids)
    bbs_ppty_df = pd.DataFrame.from_records(bbs.values()) # be sure the reset_index was applied when creating bbs.json, if not it will bug here as index dont match bb_id
    
    #bbs_ppty_df = describe_ppty_bbs_df(df, bb_tag+'_id', property) # to be remove since stats are computed already
    bbs_ppty_df.replace({np.nan: None}, inplace=True)
    
    get_bbs_boxPlot(df, bb_tag+'_id', property, series_name, n_bbs-0.5)
    
    context = {
        'bb_tag': bb_tag, 
        'property': property, 
        'bbs_ppties_df': bbs_ppty_df,
        'bbs_ppties_scores_header_project':bbs_ppties_scores_header_project.get(project.project_name, []),
        'bbs_ppties_scores_project': bbs_ppties_scores_project.get(project.project_name, []),
        'n_bbs':n_bbs,
        'n_mols': n_mols,
        'series_name':series_name,
        'project_name':project
    }

    return render(request, 'analysis/bbs_ppty_boxPlot.html', context)

def display_duo_swarmPlot(request, bb_id=None, property=None):
    series_name = get_project_series_from_session(request).series_name
    project = get_project_series_from_session(request).project
    n_bb_tags = get_project_series_from_session(request).n_bb_tags
    #TODO: apply this elegant filter to bb view
    if bb_id is None and property is None:
        bb_id = request.POST['bb_id']
        property = request.POST['property']
    bb_tag = bb_id[0]
    if n_bb_tags == 4:
        mols = Molecule.objects.filter(**{f'{property}__isnull': False, f'{bb_tag}_id':bb_id},series=series_name).exclude(Q(A_id__isnull=True) | Q(B_id__isnull=True) | Q(C_id__isnull=True) | Q(D_id__isnull=True))
        bb_duo_tags = ['A', 'B', 'C', 'D']
    else:
        mols = Molecule.objects.filter(**{f'{property}__isnull': False, f'{bb_tag}_id':bb_id},series=series_name).exclude(Q(A_id__isnull=True) | Q(B_id__isnull=True) | Q(C_id__isnull=True) )
        bb_duo_tags = ['A', 'B', 'C']
    df = pd.DataFrame.from_records(mols.values())
    if df.empty:
        return redirect('analysis_home')
    df = df[df['A_id'].notna()]
    df.replace({np.nan: None}, inplace=True)
    
    bb_duo_tags.remove(bb_tag)
    context = {
        'bb_duo_tags': bb_duo_tags,
        'bb_id':bb_id,
        'property':property,
        'mols':mols,
        'mols_ppties_df':df,
        'mols_ppties_headers':mols_ppties_headers_project.get(project.project_name, []),
        'mols_ppties':mols_ppties_project.get(project.project_name, []),
        'series_name':series_name,
        'n_bb_tags': n_bb_tags,
        'project_name':project
    }

    for bb in bb_duo_tags:
        get_duo_swarmPlot(df, property, bb_id, bb)

    return render(request, 'analysis/duo_ppty_swarmPlot.html', context)