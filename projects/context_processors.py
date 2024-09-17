from .models import Project, Series

def project_series_processor(request):
    series = Series.objects.all()
    current_series_id = request.session.get('current_series_id', None)
    current_series = None

    if current_series_id:
        current_series = series.filter(id=current_series_id).first()

    return {
        'series': series,
        'current_series': current_series,
    }
