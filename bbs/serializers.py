from rest_framework import serializers
from .models import BB

class BBSerializer(serializers.ModelSerializer):
    class Meta:
        model = BB
        fields = ['bb_smi', 'bb_id', 'EC50_main_score', 'EC50_main_median', 'EC50_main_count', 'EC50_main_rank', 'HLM_score', 'HLM_median', 'HLM_count', 'HLM_rank','CYP_testo_score', 'CYP_testo_median', 'CYP_testo_count', 'CYP_testo_rank']
