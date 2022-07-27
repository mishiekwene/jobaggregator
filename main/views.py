from django.shortcuts import redirect, render
from django.views import View
import requests
from django.http import JsonResponse
from api.models import Jobs, TechSkillTitle, JobTitles
from django.core.paginator import Paginator
from .forms import SkillSearchForm
import re

# Create your views here.
class HomeView(View):
    def get(self, request):
        latest = Jobs.objects.all().order_by('-id')[:9]
        return render(request, 'home.html', context={'latest':latest})

class SearchView(View):
    form_class = SkillSearchForm
    def get(self, request):
        form = self.form_class()
        jobs = Jobs.objects.all()
        paginator = Paginator(jobs, 10)
        page_number = request.GET.get('page')
        page_obj =paginator.get_page(page_number)
        latest = Jobs.objects.all().order_by('-id')[:9]
        return render(request, 'search.html', context={'page_obj':page_obj, 'latest':latest})


class FilterView(View):
    form_class = SkillSearchForm
    def get(self, request):
        form = self.form_class()
        category = request.GET.get('category')
        skills = request.GET.getlist('searches')
        if not skills:
            return redirect('main:search')
        skill_list = []
        for i in skills:
            skill_list.append(re.sub(r'(\b\w+\b)', r'+\1', i))
        job_role_skill=None
        if len(skills)==0:
            jobs = Jobs.objects.all()

        elif len(skills)>=1:
            if category=='hard_skill' or category=='soft_skill':
                jobs = Jobs.objects.filter(description__search=skill_list).order_by('-time_extracted')

            elif category=='job_role':
                try:
                    job_title = JobTitles.objects.get(title=skills[0])
                    job_role_skill = TechSkillTitle.objects.filter(jobtitles=job_title.onetsoc_code, hot_tech='Y')
                except:
                    job_role_skill=None
                jobs=Jobs.objects.filter(title__search=skills).order_by('-time_extracted')
        
        paginator = Paginator(jobs, 10)
        page_number = request.GET.get('page')
        page_obj =paginator.get_page(page_number)
        latest = Jobs.objects.all().order_by('-id')[:9]

        return render(request, 'search.html', context={'form':form,'page_obj':page_obj, 'latest':latest, 'job_role_skill':job_role_skill, 'cat':skills[0]})


 
def suggest_api(request):
    search = request.GET.get('search')
    type_search = request.GET.get('type_search')
    if type_search == 'hard_skill':
        headers = {'Content-Type': "application/json", 'api-key':'0I7kbYJQiQmzhk1lVxGj81Hfml9dMtiuo8xGbFLnldAzSeAyGGL3'}
        url = 'https://jobify.search.windows.net/indexes/azureblob-index/docs/suggest?api-version=2021-04-30-Preview&suggesterName=sg&search='+search
        response_data = requests.request('GET', url, headers=headers)
        response_data = response_data.json()
        response = response_data['value']
        new_data = []
        for i in response:
            m = {'text':i['@search.text'], 'id':i['@search.text']}
            new_data.append(m)
        return JsonResponse(new_data, safe=False)

    elif type_search == 'job_role':
        headers = {'Content-Type': "application/json", 'api-key':'0I7kbYJQiQmzhk1lVxGj81Hfml9dMtiuo8xGbFLnldAzSeAyGGL3'}
        url = 'https://jobify.search.windows.net/indexes/job-role/docs/suggest?api-version=2021-04-30-Preview&suggesterName=sg&search='+search
        response_data = requests.request('GET', url, headers=headers)
        response_data = response_data.json()
        response = response_data['value']
        new_data = []
        for i in response:
            m = {'text':i['@search.text'], 'id':i['@search.text']}
            new_data.append(m)
        return JsonResponse(new_data, safe=False)