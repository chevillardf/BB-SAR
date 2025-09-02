from rest_framework import serializers
from .models import BB

class BBSerializer(serializers.ModelSerializer):
    class Meta:
        model = BB
        fields = ['bb_smi', 'bb_id', 'EC50_main_score']
