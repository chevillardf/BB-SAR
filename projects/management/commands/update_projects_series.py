from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import models
from molecules.models import Molecule
from projects.models import Project, Series
from bbs.models import BB
from utils.mol_depiction import get_mol_svg
import json

bbs_files_path = ['data/DORA_Lactam_bbs.json']
mcs_files_path = ['data/DORA_Lactam_mols_bbs.json']

class UpdateBB(BaseCommand):
    def handle(self, *args, **kwargs):

        for bbs_file_path in bbs_files_path:
            with open(bbs_file_path) as f:
                bbs = json.load(f)

            bb_objects = []

            for bb in bbs:
                project_name = bb.get('project')
                project, _ = Project.objects.get_or_create(project_name=project_name)
                series_name = bb.get('series')
                series, _ = Series.objects.get_or_create(
                    project=project,
                    series_name=series_name,
                )

                bb = BB(
                    bb_smi=bb.get('bb_smi'),
                    bb_id=bb.get('bb_id'),
                    count=bb.get('count'),
                    bb_tag=bb.get('bb_tag'),
                    bb_flag=bb.get('bb_flag'),
                    BBB_Brain_count=bb.get('BBB_Brain_count'),
                    BBB_Brain_median=bb.get('BBB_Brain_median'),
                    BBB_Brain_score=bb.get('BBB_Brain_score'),
                    BBB_Brain_Plasma_ratio_count=bb.get('BBB_Brain_Plasma_ratio_count'),
                    BBB_Brain_Plasma_ratio_median=bb.get('BBB_Brain_Plasma_ratio_median'),
                    BBB_Brain_Plasma_ratio_score=bb.get('BBB_Brain_Plasma_ratio_score'),
                    BBB_Plasma_count=bb.get('BBB_Plasma_count'),
                    BBB_Plasma_median=bb.get('BBB_Plasma_median'),
                    BBB_Plasma_score=bb.get('BBB_Plasma_score'),
                    BBB_ratio_BrainPlasma_count=bb.get('BBB_ratio_BrainPlasma_count'),
                    BBB_ratio_BrainPlasma_median=bb.get('BBB_ratio_BrainPlasma_median'),
                    BBB_ratio_BrainPlasma_score=bb.get('BBB_ratio_BrainPlasma_score'),
                    BB_fu_count=bb.get('BB_fu_count'),
                    BB_fu_median=bb.get('BB_fu_median'),
                    BB_fu_score=bb.get('BB_fu_score'),
                    CYP_shift_count=bb.get('CYP_shift_count'),
                    CYP_shift_median=bb.get('CYP_shift_median'),
                    CYP_shift_score=bb.get('CYP_shift_score'),
                    CYP_testo_count=bb.get('CYP_testo_count'),
                    CYP_testo_median=bb.get('CYP_testo_median'),
                    CYP_testo_score=bb.get('CYP_testo_score'),
                    CYP_testo_rank=bb.get('CYP_testo_rank'),
                    EC50_main_count=bb.get('EC50_main_count'),
                    EC50_main_median=bb.get('EC50_main_median'),
                    EC50_main_score=bb.get('EC50_main_score'),
                    EC50_main_rank=bb.get('EC50_main_rank'),
                    GSH_count=bb.get('GSH_count'),
                    GSH_median=bb.get('GSH_median'),
                    GSH_score=bb.get('GSH_score'),
                    hERG_IC20_count=bb.get('hERG_IC20_count'),
                    hERG_IC20_median=bb.get('hERG_IC20_median'),
                    hERG_IC20_score=bb.get('hERG_IC20_score'),
                    HLM_count=bb.get('HLM_count'),
                    HLM_median=bb.get('HLM_median'),
                    HLM_score=bb.get('HLM_score'),
                    HLM_rank=bb.get('HLM_rank'),
                    logD_count=bb.get('logD_count'),
                    logD_median=bb.get('logD_median'),
                    logD_score=bb.get('logD_score'),
                    MDR1_PappAB_count=bb.get('MDR1_PappAB_count'),
                    MDR1_PappAB_median=bb.get('MDR1_PappAB_median'),
                    MDR1_PappAB_score=bb.get('MDR1_PappAB_score'),
                    MDR1_efflux_count=bb.get('MDR1_efflux_count'),
                    MDR1_efflux_median=bb.get('MDR1_efflux_median'),
                    MDR1_efflux_score=bb.get('MDR1_efflux_score'),
                    min_ratio_hM1R_hM2R_count=bb.get('min_ratio_hM1R_hM2R_count'),
                    min_ratio_hM1R_hM2R_median=bb.get('min_ratio_hM1R_hM2R_median'),
                    min_ratio_hM1R_hM2R_score=bb.get('min_ratio_hM1R_hM2R_score'),
                    OX1_IP1_EC50_count=bb.get('OX1_IP1_EC50_count'),
                    OX1_IP1_EC50_median=bb.get('OX1_IP1_EC50_median'),
                    OX1_IP1_EC50_score=bb.get('OX1_IP1_EC50_score'),
                    OX1_IP1_EC50_rank=bb.get('OX1_IP1_EC50_rank'),
                    PPB_fu_count=bb.get('PPB_fu_count'),
                    PPB_fu_median=bb.get('PPB_fu_median'),
                    PPB_fu_score=bb.get('PPB_fu_score'),
                    PXR_EC50_count=bb.get('PXR_EC50_count'),
                    PXR_EC50_median=bb.get('PXR_EC50_median'),
                    PXR_EC50_score=bb.get('PXR_EC50_score'),
                    ratio_hOX1R_hOX2R_count=bb.get('ratio_hOX1R_hOX2R_count'),
                    ratio_hOX1R_hOX2R_median=bb.get('ratio_hOX1R_hOX2R_median'),
                    ratio_hOX1R_hOX2R_score=bb.get('ratio_hOX1R_hOX2R_score'),
                    ratio_hOX1R_hOX2R_rank=bb.get('ratio_hOX1R_hOX2R_rank'),
                    sol_FaSSIF_count=bb.get('sol_FaSSIF_count'),
                    sol_FaSSIF_median=bb.get('sol_FaSSIF_median'),
                    sol_FaSSIF_score=bb.get('sol_FaSSIF_score'),
                    sol_pH6_count=bb.get('sol_pH6_count'),
                    sol_pH6_median=bb.get('sol_pH6_median'),
                    sol_pH6_score=bb.get('sol_pH6_score'),
                    BPI_calc_count=bb.get('BPI_calc_count'),
                    BPI_calc_median=bb.get('BPI_calc_median'),
                    BPI_calc_score=bb.get('BPI_calc_score'),
                    project=project,
                    series=series
                )
                bb_objects.append(bb)

            BB.objects.bulk_create(bb_objects)

class UpdateMolecule(BaseCommand):
    def handle(self, *args, **kwargs):

        for mcs_file_path in mcs_files_path:
            with open(mcs_file_path) as f:
                mols = json.load(f)

            molecule_objects = []

            for m in mols:
                project_instance, created = Project.objects.get_or_create(
                    project_name=m['project']
                )
                m = Molecule(
                    project=project_instance,
                    series=m.get('series'),
                    sub_series=m.get('sub_series'),
                    mol_smi=m.get('mol_smi'),
                    mol_id=m.get('mol_id'),
                    mol_flag=m.get('mol_flag'),
                    A_id=m.get('A_id'),
                    B_id=m.get('B_id'),
                    C_id=m.get('C_id'),
                    D_id=m.get('D_id'),
                    bbs_id=m.get('bbs_id'),
                    BB_fu=m.get('BB_fu'),
                    BBB_Brain=m.get('BBB_Brain'),
                    BBB_Brain_2=m.get('BBB_Brain_2'), 
                    BBB_Plasma=m.get('BBB_Plasma'),
                    BBB_Brain_Plasma_ratio=m.get('BBB_Brain_Plasma_ratio'), 
                    BBB_Plasma_2=m.get('BBB_Plasma_2'),
                    BBB_ratio_BrainPlasma=m.get('BBB_ratio_BrainPlasma'),
                    CYP_mida=m.get('CYP_mida'),
                    CYP_testo=m.get('CYP_testo'),
                    CYP_shift=m.get('CYP_shift'),
                    CYP2C9_IC50=m.get('CYP2C9_IC50'),
                    CYP2D6_IC50=m.get('CYP2D6_IC50'),
                    CYP2C9_screening_IC50=m.get('CYP2C9_screening_IC50'),
                    CYP2D6_screening_IC50=m.get('CYP2D6_screening_IC50'),
                    CYP3A4_screening_mida_IC50=m.get('CYP3A4_screening_mida_IC50'),
                    CYP3A4_screening_testo_IC50=m.get('CYP3A4_screening_testo_IC50'),
                    DogLM=m.get('DogLM'),
                    DMPK_status=m.get('DMPK_status'),
                    EC50_main=m.get('EC50_main'),
                    FLP_EC50=m.get('FLP_EC50'),
                    FLP_effect=m.get('FLP_effect'),
                    GSH=m.get('GSH'),
                    HLM=m.get('HLM'),
                    hM1R_FLIPR_IC50=m.get('hM1R_FLIPR_IC50_IC50'),
                    hM2R_FLIPR_IC50=m.get('hM2R_FLIPR_IC50_IC50'),
                    hM3R_FLIPR_IC50=m.get('hM3R_FLIPR_IC50_IC50'),
                    hM5R_FLIPR_IC50=m.get('hM5R_FLIPR_IC50_IC50'),
                    IP1_effect=m.get('IP1_effect'),
                    KineticEV_AUC=m.get('KineticEV_AUC'), 
                    KineticIV_AUC=m.get('KineticIV_AUC'), 
                    KineticEV_Cmax=m.get('KineticEV_Cmax'),
                    KineticIV_Clearance=m.get('KineticIV_Clearance'), 
                    logD=m.get('logD'),
                    MDR1_PappAB=m.get('MDR1_PappAB'),
                    MDR1_efflux=m.get('MDR1_efflux'),
                    min_ratio_hM1R_hM2R=m.get('min_ratio_hM1R_hM2R'),
                    MouseLM=m.get('MouseLM'),
                    OX1_IP1_EC50=m.get('OX1_IP1_EC50'),
                    PPB_fu=m.get('PPB_fu'),
                    PXR_EC50=m.get('PXR_EC50'),
                    PXR_Emax=m.get('PXR_Emax'),
                    ratio_hOX1R_hOX2R=m.get('ratio_hOX1R_hOX2R'),
                    RatLM=m.get('RatLM'), 
                    sol_FaSSIF=m.get('sol_FaSSIF'),
                    sol_pH6=m.get('sol_pH6'),
                    Tox_CellTiter_Glo_IC50=m.get('Tox_CellTiter_Glo_IC50'),
                    BPI_calc=m.get('BPI_calc'),
                )
                molecule_objects.append(m)

            Molecule.objects.bulk_create(molecule_objects)

class UpdateProjectSeries(BaseCommand):
    help = 'Update n_mols field in Series model based on projects.json data'

    def handle(self, *args, **kwargs):
        with open('data/projects.json') as file:
            projects_data = json.load(file)

        for project_data in projects_data:
            project_name = project_data["project_name"]
            series_name = project_data["series"]
            n_bb_tags = project_data["n_bb_tags"]
            n_bbs = project_data["n_bbs"]
            n_A = project_data["n_A"]
            n_B = project_data["n_B"]
            n_C = project_data["n_C"]
            n_D = project_data["n_D"]
            series_bbsar_coverage = project_data["series_bbsar_coverage"]
            sub_series = project_data.get("sub_series", "")

            project, _ = Project.objects.get_or_create(project_name=project_name)

            series, created = Series.objects.get_or_create(
                project=project,
                series_name=series_name,
                defaults={'series_bbsar_coverage':series_bbsar_coverage,'n_bb_tags':n_bb_tags, 'sub_series': sub_series, 'n_mols': 0, 'date_updated': timezone.now()}
            )
            if not created:
                series.n_bb_tags = n_bb_tags
                series.n_bbs = n_bbs
                series.n_A = n_A
                series.n_B = n_B
                series.n_C = n_C
                series.n_D = n_D
                series.series_bbsar_coverage = series_bbsar_coverage
                series.save()

            molecule_count = Molecule.objects.filter(series=series_name).count()
            series.n_mols = molecule_count
            series.date_updated = timezone.now()
            series.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully updated {molecule_count} mols for {project_name} - {series_name}'))

class Update2Ddepiction(BaseCommand):
    help = 'Update n_mols field in Project model'

    def handle(self, *args, **kwargs):
        for bbs_file_path in bbs_files_path:
            project_name = bbs_file_path.split('/')[1].split('_')[0]
            series_name = bbs_file_path.split('/')[1].split('_')[1]
            with open(bbs_file_path) as f:
                bbs = json.load(f)

            for bb in bbs:
                get_mol_svg(bb['bb_smi'], bb['bb_id'], 'bb', project_name, series_name)

        for mcs_file_path in mcs_files_path:
            project_name = mcs_file_path.split('/')[1].split('_')[0]
            series_name = mcs_file_path.split('/')[1].split('_')[1]
            with open(mcs_file_path) as f:
                mols = json.load(f)

            for mol in mols:
                get_mol_svg(mol['mol_smi'], mol['mol_id'], 'mol', project_name, series_name)

class Command(BaseCommand):
    help = 'Run all models update commands'

    def handle(self, *args, **kwargs):
        BB.objects.all().delete()
        Molecule.objects.all().delete()
        UpdateBB().handle()
        UpdateMolecule().handle()
        UpdateProjectSeries().handle()
        Update2Ddepiction().handle()

        self.stdout.write(self.style.SUCCESS('All update commands executed successfully'))
