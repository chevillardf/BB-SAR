# forms.py
from django import forms
from .models import Project, Series

class ProjectSeriesForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), label="Select Project")
    series = forms.ModelChoiceField(queryset=Series.objects.none(), label="Select Series")

    def __init__(self, *args, **kwargs):
        super(ProjectSeriesForm, self).__init__(*args, **kwargs)
        if 'project' in self.data:
            try:
                project_id = int(self.data.get('project'))
                self.fields['series'].queryset = Series.objects.filter(project_id=project_id).order_by('series_name')
            except (ValueError, TypeError):
                pass
