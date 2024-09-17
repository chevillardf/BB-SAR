from django.db import models
from django.utils import timezone

class Project(models.Model):
    project_name = models.CharField(max_length=25)

    def __str__(self):
        return str(self.project_name)
    
class Series(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    series_name = models.CharField(max_length=25)
    sub_series = models.CharField(max_length=25, blank=True)
    n_mols = models.IntegerField(default=0)
    series_bbsar_coverage = models.FloatField(default=0)
    n_bb_tags = models.IntegerField(default=0)
    n_bbs = models.IntegerField(default=0)
    n_A = models.IntegerField(default=0)
    n_B = models.IntegerField(default=0)
    n_C = models.IntegerField(default=0)
    n_D = models.IntegerField(default=0)
    date_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('project', 'series_name')

    def __str__(self):
        return f"{self.project.project_name} - {self.series_name}"