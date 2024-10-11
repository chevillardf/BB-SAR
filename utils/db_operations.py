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