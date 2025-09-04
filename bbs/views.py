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
from .models import BB
from molecules.models import Molecule
from utils.db_operations import get_project_series_from_session
from utils.df_analysis import describe_bb_ppties_df
from utils.mol_operations import has_substr
from utils.proj_settings import mols_ppties_headers_project, mols_ppties_project, bbs_ppties_header_project, ppties_bb_rows_project,bbs_ppties_project
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import BBSerializer
import pandas as pd
import numpy as np

def bbs_home(request):
    current_series = get_project_series_from_session(request)
    project = get_project_series_from_session(request)
    if current_series:
        series_name = current_series.series_name
        project = project.project
        all_bbs = BB.objects.filter(series__series_name=series_name) #To filter BB objects by series_name, you need to join through the Series model using the __ syntax for spanning relationship
    else:
        return redirect('projects_home')
    
    tags = request.GET.getlist('tag') or ['A']
    bb_count = request.GET.get('currentFilterBBcount', 1)
    filter_bb_count_on = request.GET.get('enableBBcountFilter') == 'on'
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

    substr_smi = request.GET.get('smiles', '')
    all_bbs = all_bbs.filter(count__gte=int(bb_count)) if filter_bb_count_on else all_bbs
    all_bbs = all_bbs.filter(EC50_main_median__lte=int(filter_ec50)) if filter_ec50_on else all_bbs
    all_bbs = all_bbs.filter(HLM_median__lte=int(filter_HLM)) if filter_HLM_on else all_bbs
    all_bbs = all_bbs.filter(MDR1_PappAB_median__gte=int(filterMDR1PappAB)) if filter_MDR1PappAB_on else all_bbs
    all_bbs = all_bbs.filter(MDR1_efflux_median__lte=int(filterMDR1Efflux)) if filter_MDR1Efflux_on else all_bbs
    all_bbs = all_bbs.filter(sol_FaSSIF_median__gte=int(filterSolFaSSIF)) if filter_SolFaSSIF_on else all_bbs
    all_bbs = all_bbs.filter(logD_median__lte=filterLogD) if filter_LogD_on else all_bbs
    all_bbs = all_bbs.filter(GSH_median__lte=filterDGSH) if filter_DGSH_on else all_bbs
    all_bbs = all_bbs.filter(PXR_EC50_median__gte=filter_PXR) if filter_PXR_on else all_bbs
    all_bbs = all_bbs.filter(CYP_testo_median__gte=filter_CYPt) if filter_CYPt_on else all_bbs

    if substr_smi:
        df = pd.DataFrame.from_records(all_bbs.values())
        df["has_substr"] = df.apply(lambda x: has_substr(x.bb_smi, substr_smi), axis=1)
        filt = df['has_substr'] == True
        df = df[filt]
        bbs_with_substr = df['bb_id'].tolist()
        all_bbs = all_bbs.filter(bb_id__in=bbs_with_substr)

    if not tags:
        all_bbs = all_bbs.filter(bb_id__startswith='A')
    else:
        if 'All' in tags:
            all_bbs = all_bbs
        else:
            q_objects = Q()
            for tag in tags:
                q_objects |= Q(bb_id__startswith=tag)
            all_bbs = all_bbs.filter(q_objects)
    bbs_ppties_df = pd.DataFrame.from_records(all_bbs.values()).replace({np.nan: None})
    
    context = {
        'bbs': all_bbs,
        'bbs_ppties_df':bbs_ppties_df,
        'bbs_ppties_headers': bbs_ppties_header_project.get(project.project_name, []),
        'bbs_ppties': bbs_ppties_project.get(project.project_name, []),
        'selected_tags': tags,
        'currentFilterBBcount': bb_count,
        'currentFilterEC50': filter_ec50,
        'currentFilterHLM': filter_HLM,
        'currentFilterMDR1PappAB': filterMDR1PappAB,
        'currentFilterMDR1Efflux': filterMDR1Efflux,
        'currentFilterSolFaSSIF':filterSolFaSSIF,
        'currentFilterLogD':filterLogD,
        'currentFilterDGSH': filterDGSH,
        'currentFilterPXR': filter_PXR,
        'currentFilterCYPt': filter_CYPt,
        'substr_smi': substr_smi,
        'series_name':series_name,
        'project_name':project
    }
    return render(request, 'bbs/bbs_home.html', context)

def bb_home(request, bb_id):
    current_series = get_project_series_from_session(request)
    project = get_project_series_from_session(request).project
    n_bb_tags = get_project_series_from_session(request).n_bb_tags
    
    if current_series:
        series_name = current_series.series_name
        bb = BB.objects.filter(series__series_name=series_name, bb_id=bb_id).first()
    else:
        return redirect('projects_home')
    
    bb_tag = getattr(bb, 'bb_tag')
    if bb_tag == 'A':
        mols = Molecule.objects.filter(series=series_name, A_id=bb_id)
    elif bb_tag == 'B':
        mols = Molecule.objects.filter(series=series_name, B_id=bb_id)
    elif bb_tag == 'C':
        mols = Molecule.objects.filter(series=series_name, C_id=bb_id)
    else:
        mols = Molecule.objects.filter(series=series_name, D_id=bb_id)
    
    mols_ppties_df = pd.DataFrame.from_records(mols.values()).replace({np.nan: None})

    mols_properties = {property: [getattr(mol, property) for mol in mols] for property in ppties_bb_rows_project.get(project.project_name, [])}
    mols_id = [bb_id for mol in mols]
    dict_stats = {'bb_id': mols_id, **mols_properties}
    ppties_bb_df = describe_bb_ppties_df(dict_stats, ppties_bb_rows_project.get(project.project_name, [])).replace({np.nan: None})

    context = {
        'bb': bb,
        'mols': mols,
        'ppties_bb_df': ppties_bb_df,
        'mols_ppties_df':mols_ppties_df,
        'mols_ppties_headers':mols_ppties_headers_project.get(project.project_name, []),
        'mols_ppties':mols_ppties_project.get(project.project_name, []),
        'series_name':series_name,
        'n_bb_tags': n_bb_tags,
        'project_name':project
    }
    return render(request, 'bbs/bb_home.html', context)

@swagger_auto_schema(
        method='get',
        operation_summary="Query BB properties",
        operation_description="Returns potency, HLM, and CYP_testo statistics (count, median, rank, score) for a given SMILES building block. The SMILES must match exactly one building block in the database.",
        manual_parameters=[openapi.Parameter('smi', openapi.IN_QUERY, description="SMILES string", type=openapi.TYPE_STRING)],
        responses={
        200: BBSerializer,
        400: 'No SMILES provided',
        404: 'BB not found',
    }
)

@api_view(['GET'])
def bb_query(request):
    smiles = request.GET.get('bb_smi')
    if not smiles:
        return Response({"error": "No SMILES provided"}, status=400)
    
    try:
        bb = BB.objects.get(bb_smi=smiles)
        serializer = BBSerializer(bb)
        return Response(serializer.data)
    except BB.DoesNotExist:
        return Response({"error": "BB not found"}, status=404)