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

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import Project, Series
from utils.proj_settings import mols_ppties_project

def projects_home(request):
    projects = Project.objects.prefetch_related('series_set').all()
    
    context = {
        'projects': projects,
    }
    return render(request, 'projects/projects_home.html', context)

def set_series(request, series_id):
    series = get_object_or_404(Series, id=series_id)
    request.session['current_series_id'] = series.id
    request.session['current_project_name'] = series.project.project_name
    request.session['current_series_name'] = series.series_name

    return redirect('projects_home')

def password_login(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == settings.SITE_PASSWORD:
            request.session['is_authenticated'] = True
            return redirect('projects_home')

    return render(request, 'projects/pw_login.html')