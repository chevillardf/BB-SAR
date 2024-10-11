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

from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Molecule
from bbs.models import BB
from utils.data_operations import process_field
from utils.db_operations import get_query, get_project_series_from_session
from utils.df_analysis import describe_bbs_ppty_df
from utils.mol_operations import has_substr
from utils.proj_settings import mols_ppties_headers_project, mols_ppties_project, ppties_main_left_mol_tab_project, ppties_main_right_mol_tab_project, ppties_2ndary_left_mol_tab_project, ppties_2ndary_right_mol_tab_project, ppties_bbb_left_mol_tab_project, ppties_bbb_right_mol_tab_project, ppties_pk_left_mol_tab_project, ppties_pk_right_mol_tab_project
import pandas as pd
import numpy as np

def molecule_home(request, mol_id):
    series_name = get_project_series_from_session(request)
    project = get_project_series_from_session(request).project

    if series_name:
        n_bb_tags = series_name.n_bb_tags
        n_A = series_name.n_A
        n_B = series_name.n_B
        n_C = series_name.n_C
        series_name = series_name.series_name
        mol = Molecule.objects.filter(mol_id=mol_id, series=series_name).first()
    else:
        mol = None

    bbs_id = getattr(mol, 'bbs_id').replace('[', '').replace(']', '').replace(' ', '').replace('\'', '').split(',')
    bbs = BB.objects.filter(bb_id__in=bbs_id, series__series_name=series_name) #To filter BB objects by series_name, you need to join through the Series model using the __ syntax for spanning relationship
    
    if n_bb_tags == 4:
        analogs_A = Molecule.objects.filter(~Q(A_id=bbs_id[0]) & Q(B_id=bbs_id[1]) & Q(C_id=bbs_id[2]) & Q(D_id=bbs_id[3]) & Q(series=series_name)).values()
        analogs_B = Molecule.objects.filter(Q(A_id=bbs_id[0]) & ~Q(B_id=bbs_id[1]) & Q(C_id=bbs_id[2]) & Q(D_id=bbs_id[3]) & Q(series=series_name)).values()
        analogs_C = Molecule.objects.filter(Q(A_id=bbs_id[0]) & Q(B_id=bbs_id[1]) & ~Q(C_id=bbs_id[2]) & Q(D_id=bbs_id[3]) & Q(series=series_name)).values()
        analogs_D = Molecule.objects.filter(Q(A_id=bbs_id[0]) & Q(B_id=bbs_id[1]) & Q(C_id=bbs_id[2]) & ~Q(D_id=bbs_id[3]) & Q(series=series_name)).values()
        df_A = pd.DataFrame.from_records(analogs_A)
        df_A['B_id'] = df_A['C_id'] = df_A['D_id'] = None
        df_B = pd.DataFrame.from_records(analogs_B)
        df_B['A_id'] = df_B['C_id'] = df_B['D_id'] = None
        df_C = pd.DataFrame.from_records(analogs_C)
        df_C['B_id'] = df_C['A_id'] = df_C['D_id'] = None
        df_D = pd.DataFrame.from_records(analogs_D)
        df_D['A_id'] = df_D['C_id'] = df_D['B_id'] = None
        mols_ppties_df = pd.concat([df_A, df_B, df_C, df_D], ignore_index=True)
    else:
        analogs_A = Molecule.objects.filter(~Q(A_id=bbs_id[0]) & Q(B_id=bbs_id[1]) & Q(C_id=bbs_id[2]) & Q(series=series_name)).values()
        analogs_B = Molecule.objects.filter(Q(A_id=bbs_id[0]) & ~Q(B_id=bbs_id[1]) & Q(C_id=bbs_id[2]) & Q(series=series_name)).values()
        analogs_C = Molecule.objects.filter(Q(A_id=bbs_id[0]) & Q(B_id=bbs_id[1]) & ~Q(C_id=bbs_id[2]) & Q(series=series_name)).values()
        df_A = pd.DataFrame.from_records(analogs_A)
        df_A['B_id'] = df_A['C_id'] = None
        df_B = pd.DataFrame.from_records(analogs_B)
        df_B['A_id'] = df_B['C_id'] = None
        df_C = pd.DataFrame.from_records(analogs_C)
        df_C['B_id'] = df_C['A_id'] = None
        mols_ppties_df = pd.concat([df_A, df_B, df_C], ignore_index=True)
    mols_ppties_df.replace({np.nan: None}, inplace=True)
    # TODO: debug as only analogs for 1 bb are displayed (or only 1 tag is shown)
    try:
        mols_analogs = mols_ppties_df['mol_id'].tolist()
    except:
        mols_analogs = ''
    mols = Molecule.objects.filter(mol_id__in=mols_analogs, series=series_name) #TODO: is mols useful? it does not appear in molecule_home
    #TODO: fix table so rows are filled automatically like columns headers
    context = {
        'mol': mol,
        'mols': mols,
        'bbs': bbs,
        'mols_ppties_df':mols_ppties_df,
        'mols_ppties_headers': mols_ppties_headers_project.get(project.project_name, []),
        'mols_ppties': mols_ppties_project.get(project.project_name, []),
        'ppties_main_left_mol_tab':ppties_main_left_mol_tab_project.get(project.project_name, []),
        'ppties_main_right_mol_tab':ppties_main_right_mol_tab_project.get(project.project_name, []),
        'ppties_2ndary_left_mol_tab':ppties_2ndary_left_mol_tab_project.get(project.project_name, []),
        'ppties_2ndary_right_mol_tab':ppties_2ndary_right_mol_tab_project.get(project.project_name, []),
        'ppties_bbb_left_mol_tab':ppties_bbb_left_mol_tab_project.get(project.project_name, []),
        'ppties_bbb_right_mol_tab':ppties_bbb_right_mol_tab_project.get(project.project_name, []),
        'ppties_pk_left_mol_tab':ppties_pk_left_mol_tab_project.get(project.project_name, []),
        'ppties_pk_right_mol_tab':ppties_pk_right_mol_tab_project.get(project.project_name, []),
        'series_name':series_name,
        'n_bb_tags':n_bb_tags,
        'n_A': n_A,
        'n_B': n_B,
        'n_C': n_C,
        'project_name':project
    }
    return render(request, 'molecules/molecule_home.html', context)

def molecules_home(request):
    series_name = get_project_series_from_session(request)
    project = get_project_series_from_session(request)
    if series_name:
        n_bb_tags = series_name.n_bb_tags
        series_name = series_name.series_name
        project = project.project
        mols = Molecule.objects.filter(series=series_name)
    else:
        return redirect('projects_home')
    
    substr_smi = request.GET.get('smiles', '')
    mol_id = request.GET.get('molId', '')
    A_id = request.GET.get('A_id', '')
    B_id = request.GET.get('B_id', '')
    C_id = request.GET.get('C_id', '')
    D_id = request.GET.get('D_id', '')
    filter_ec50 = request.GET.get('currentFilterEC50', 20000)
    filter_ec50_on = request.GET.get('enableEC50Filter') == 'on'
    filter_HLM = request.GET.get('currentFilterHLM', 1250)
    filter_HLM_on = request.GET.get('enableHLMFilter') == 'on'
    filterMDR1PappAB = request.GET.get('currentFilterMDR1PappAB', 0)
    filter_MDR1PappAB_on = request.GET.get('enableMDR1PappABFilter') == 'on'
    filterMDR1Efflux = request.GET.get('currentFilterMDR1Efflux', 100)
    filter_MDR1Efflux_on = request.GET.get('enableMDR1EffluxFilter') == 'on'
    filterSolFaSSIF = request.GET.get('currentFilterSolFaSSIF', 0)
    filter_SolFaSSIF_on = request.GET.get('enableSolFaSSIFFilter') == 'on'
    filterLogD = request.GET.get('currentFilterLogD', 5)
    filter_LogD_on = request.GET.get('enableLogDFilter') == 'on'
    filterDGSH = request.GET.get('currentFilterDGSH', 2500)
    filter_DGSH_on = request.GET.get('enableDGSHFilter') == 'on'
    filter_PXR = request.GET.get('currentFilterPXR', 50)
    filter_PXR_on = request.GET.get('enablePXRFilter') == 'on'
    filter_CYPt = request.GET.get('currentFilterCYPt', 50)
    filter_CYPt_on = request.GET.get('enableCYPtFilter') == 'on'
    conditions = []
    
    if substr_smi:
        mols_ppties_df = pd.DataFrame.from_records(mols.values())
        mols_ppties_df["has_substr"] = mols_ppties_df.apply(lambda x: has_substr(x.mol_smi, substr_smi), axis=1)
        filt = mols_ppties_df['has_substr'] == True
        mols_ppties_df = mols_ppties_df[filt]
        mols_with_substr = mols_ppties_df['mol_id'].tolist()
        mols = mols.filter(mol_id__in=mols_with_substr)

    if mol_id:
        mol_ids = [id.strip() for id in mol_id.split(',')]
        if len(mol_ids) > 1: # multiple mol_id
            mols = mols.filter(mol_id__in=mol_ids)
            
        else: # single mol_id
            if mol_id.isnumeric():
                mols = mols.filter(mol_id__in=mol_ids)
            else: # no id was retrieved or incorrect input
                mols = mols.all().order_by('-id')[:0]

    if (A_id or B_id or C_id or D_id):
        if A_id:
            A_ids = process_field(A_id, 'A')
            conditions.append(get_query(A_ids, 'A_id'))
        if B_id:
            B_ids = process_field(B_id, 'B')
            conditions.append(get_query(B_ids, 'B_id'))
        if C_id:
            C_ids = process_field(C_id, 'C')
            conditions.append(get_query(C_ids, 'C_id'))
        if D_id:
            D_ids = process_field(D_id, 'D')
            conditions.append(get_query(D_ids, 'D_id'))

        # If at least two fields are filled, apply the AND operator
        if len(conditions) >= 2:
            query = conditions.pop()
            for condition in conditions:
                query &= condition
        else:
            query = conditions[0]

        mols = mols.filter(query).values()
    mols = mols.filter(EC50_main__lte=int(filter_ec50)) if filter_ec50_on else mols
    mols = mols.filter(HLM__lte=int(filter_HLM)) if filter_HLM_on else mols
    mols = mols.filter(MDR1_PappAB__gte=int(filterMDR1PappAB)) if filter_MDR1PappAB_on else mols
    mols = mols.filter(MDR1_efflux__lte=int(filterMDR1Efflux)) if filter_MDR1Efflux_on else mols
    mols = mols.filter(sol_FaSSIF__gte=int(filterSolFaSSIF)) if filter_SolFaSSIF_on else mols
    mols = mols.filter(logD__lte=filterLogD) if filter_LogD_on else mols
    mols = mols.filter(GSH__lte=filterDGSH) if filter_DGSH_on else mols
    mols = mols.filter(PXR_EC50__gte=filter_PXR) if filter_PXR_on else mols
    mols = mols.filter(CYP_testo__gte=filter_CYPt) if filter_CYPt_on else mols

    if not any([mol_id, substr_smi, A_id, B_id, C_id, D_id, filter_ec50_on, filter_HLM_on, filter_MDR1PappAB_on, filter_MDR1Efflux_on, filter_SolFaSSIF_on, filter_LogD_on, filter_DGSH_on, filter_PXR_on, filter_CYPt_on]):
        mols = mols.all().order_by('-mol_id')[:50]

    mols_ppties_df = pd.DataFrame.from_records(mols.values()).replace({np.nan: None})
    
    context = {
        'mols':mols,
        'mols_ppties_df':mols_ppties_df,
        'mols_ppties_headers': mols_ppties_headers_project.get(project.project_name, []),
        'mols_ppties': mols_ppties_project.get(project.project_name, []),
        'series_name':series_name,
        'n_bb_tags': n_bb_tags,
        'project_name':project.project_name,
        'currentFilterEC50': filter_ec50,
        'currentFilterHLM': filter_HLM,
        'currentFilterMDR1PappAB': filterMDR1PappAB,
        'currentFilterMDR1Efflux': filterMDR1Efflux,
        'currentFilterSolFaSSIF':filterSolFaSSIF,
        'currentFilterLogD':filterLogD,
        'currentFilterDGSH': filterDGSH,
        'currentFilterPXR': filter_PXR,
        'currentFilterCYPt': filter_CYPt,
    }
    return render(request, 'molecules/molecules_home.html', context)

def suggested_molecules(request, mol_id, property):
    #TODO: unified project, series, n_bb_tags across all views?
    project = get_project_series_from_session(request).project
    series_name = get_project_series_from_session(request).series_name
    n_bb_tags = get_project_series_from_session(request).n_bb_tags
    mol = Molecule.objects.filter(mol_id=mol_id, series=series_name).first()
    bbs_id = getattr(mol, 'bbs_id').replace('[', '').replace(']', '').replace(' ', '').replace('\'', '').split(',')
    bbs = BB.objects.filter(bb_id__in=bbs_id, series__series_name=series_name)
    ppty_value = getattr(mol, property)
    mols = Molecule.objects.filter(**{f'{property}__isnull': False, 'series':series_name}).values()
    df = pd.DataFrame.from_records(mols)
    if property in ['HLM', 'MDR1_efflux', 'EC50_main']:
        sort_ascending = True
    else:
        sort_ascending = False
    if n_bb_tags == 4:
        results_df_A = describe_bbs_ppty_df(df, 'A_id', bbs_id[0], bbs_id, property, no_single=True).sort_values(by='score', ascending=sort_ascending).head(3)
        results_df_A['A_id'] = results_df_A['bb_id_col']
        results_df_A['D_id'] = results_df_A['C_id'] = results_df_A['B_id'] = None
        results_df_B = describe_bbs_ppty_df(df, 'B_id', bbs_id[1], bbs_id, property, no_single=True).sort_values(by='score', ascending=sort_ascending).head(3)
        results_df_B['B_id'] = results_df_B['bb_id_col']
        results_df_B['D_id'] = results_df_B['C_id'] = results_df_B['A_id'] = None
        results_df_C = describe_bbs_ppty_df(df, 'C_id', bbs_id[2], bbs_id, property, no_single=True).sort_values(by='score', ascending=sort_ascending).head(3)
        results_df_C['C_id'] = results_df_C['bb_id_col']
        results_df_C['D_id'] = results_df_C['B_id'] = results_df_C['A_id'] = None
        results_df_D = describe_bbs_ppty_df(df, 'D_id', bbs_id[3], bbs_id, property, no_single=True).sort_values(by='score', ascending=sort_ascending).head(3)
        results_df_D['D_id'] = results_df_D['bb_id_col']
        results_df_D['C_id'] = results_df_D['B_id'] = results_df_D['A_id'] = None
        mols_ppty_df = pd.concat([results_df_A, results_df_B, results_df_C, results_df_D], ignore_index=True)
    else:
        results_df_A = describe_bbs_ppty_df(df, 'A_id', bbs_id[0], bbs_id, property, no_single=True).sort_values(by='score', ascending=sort_ascending).head(3)
        results_df_A['A_id'] = results_df_A['bb_id_col']
        results_df_A['C_id'] = results_df_A['B_id'] = None
        results_df_B = describe_bbs_ppty_df(df, 'B_id', bbs_id[1], bbs_id, property, no_single=True).sort_values(by='score', ascending=sort_ascending).head(3)
        results_df_B['B_id'] = results_df_B['bb_id_col']
        results_df_B['C_id'] = results_df_B['A_id'] = None
        results_df_C = describe_bbs_ppty_df(df, 'C_id', bbs_id[2], bbs_id, property, no_single=True).sort_values(by='score', ascending=sort_ascending).head(3)
        results_df_C['C_id'] = results_df_C['bb_id_col']
        results_df_C['B_id'] = results_df_C['A_id'] = None
        mols_ppty_df = pd.concat([results_df_A, results_df_B, results_df_C], ignore_index=True)
        pass
    mols_ppty_df.replace({np.nan: None}, inplace=True)

    context = {
        'mol_id': mol_id,
        'property': property,
        'mols': len(mols),
        'bbs':bbs,
        'ppty_value': ppty_value,
        'mols_ppty_df': mols_ppty_df,
        'series_name':series_name,
        'n_bb_tags':n_bb_tags,
        'project_name':project
    }

    return render(request, 'molecules/suggested_molecules.html', context)