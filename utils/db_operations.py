from django.db.models import Q
from django.shortcuts import get_object_or_404
from projects.models import Series

def get_query(id_list, field):
    query = Q()
    for id in id_list:
        query |= Q(**{field: id})
    return query

def get_project_series_from_session(request):
    series_id = request.session.get('current_series_id')
    if series_id:
        return get_object_or_404(Series, id=series_id)
    return None