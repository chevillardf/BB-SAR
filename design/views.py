from django.shortcuts import render, redirect
from bbs.models import BB
from molecules.models import Molecule
from utils.bb_operations import get_bb_combo, combo_contains_all_tags, combine_with_bb_id, does_combination_exist
from utils.db_operations import get_project_series_from_session
from utils.proj_settings import ppties_bb_rows_project
import pandas as pd

def design_home(request):
    project = get_project_series_from_session(request)
    series_name = get_project_series_from_session(request)
    if series_name:
        series_name = series_name.series_name
        project = project.project
    else:
        return redirect('projects_home')
    
    bb_tags = ['A', 'B', 'C', 'D']
    properties = ppties_bb_rows_project.get(project.project_name, [])
    combos = ['Duo', 'Trio']

    context = {
        'bb_tags': bb_tags, 
        'properties': properties, 
        'combos': combos,
        'series_name':series_name,
        'project_name':project
    }

    return render(request, 'design/design_home.html', context)

def design_new_mols(request):
    series_name = get_project_series_from_session(request).series_name
    project = get_project_series_from_session(request).project
    bb_fields = {
        'A_id': request.POST.get('A_id') or request.GET.get('A_id'),
        'B_id': request.POST.get('B_id') or request.GET.get('B_id'),
        'C_id': request.POST.get('C_id') or request.GET.get('C_id'),
        'D_id': request.POST.get('D_id') or request.GET.get('D_id')
    }
    filled_fields = {key: value for key, value in bb_fields.items() if value}
    filled_count = len(filled_fields)
    property = request.POST.get('property') or request.GET.get('property')
    accuracy_mode = request.POST.get('accuracy_mode', 'on') or 'off'
    all_bb_tags = ['A', 'B', 'C', 'D']

    mols = Molecule.objects.filter(**{f'{property}__isnull': False},series=series_name).values()
    df = pd.DataFrame.from_records(mols)
    if df.empty:
        return redirect('design_home')
    df = df.dropna(subset=['A_id', 'B_id', 'C_id', 'D_id'], how='any')
    all_bb_ids = df[['A_id', 'B_id', 'C_id', 'D_id']].values.tolist()
    
    if filled_count == 1:
        (filled_field_name, filled_value), = filled_fields.items()
        bb_tag = filled_field_name[0]
        bb_id = bb_tag+filled_value
        remaining_bbs = [bb for bb in all_bb_tags if bb != bb_tag]
        bb_combo_df = get_bb_combo(3, all_bb_ids, df, property)
        filt = bb_combo_df['bbs_combo'].apply(lambda combo: combo_contains_all_tags(combo, remaining_bbs))
        bb_combo_df = bb_combo_df[filt]
        bb_combo_df['bb_ids'] = bb_combo_df['bbs_combo'].apply(lambda x: combine_with_bb_id(x, bb_id))
        filt = bb_combo_df['bb_ids'].apply(does_combination_exist)
        bb_combo_df = bb_combo_df[~filt]
    elif filled_count == 2:
        pass
    elif filled_count == 3:
        pass
    else:
        return redirect('design_home')

    context = {
        'property': property,
        'bb_id':bb_id,
        'accuracy_mode':accuracy_mode,
        'bb_combo_df':bb_combo_df,
        'series_name':series_name,
        'project_name':project
    }
    
    return render(request, 'design/design_mols_results.html', context)