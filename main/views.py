from django.shortcuts import redirect, render
from django.views import View
import requests
from django.http import JsonResponse
from api.models import Jobs, TechSkillTitle, JobTitles, TechSkills
from django.core.paginator import Paginator
from .forms import SkillSearchForm, FilterForm
import re
from urllib.parse import urlencode

# Create your views here.
class HomeView(View):
    def get(self, request):
        latest = Jobs.objects.all().order_by('-id')[:9]
        return render(request, 'home.html', context={'latest':latest})

class SearchView(View):
    form_class = SkillSearchForm
    def get(self, request):
        form = self.form_class()
        filterForm = FilterForm()
        jobs = Jobs.objects.all()
        paginator = Paginator(jobs, 10)
        page_number = request.GET.get('page')
        page_obj =paginator.get_page(page_number)
        latest = Jobs.objects.all().order_by('-id')[:9]
        url1 = ''
        return render(request, 'search.html', context={'page_obj':page_obj, 'latest':latest, 'url1':url1})


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
        if len(skills)==0:
            jobs = Jobs.objects.all()

        elif len(skills)>=1:
            if category=='hard_skill' or category=='soft_skill':
                jobs = Jobs.objects.filter(description__search=skill_list).order_by('-time_extracted')


            elif category=='job_role':
                jobs = Jobs.objects.filter(title__search=skills).order_by('-time_extracted')


        
        paginator = Paginator(jobs, 10)
        page_number = request.GET.get('page')
        page_obj =paginator.get_page(page_number)
        latest = Jobs.objects.all().order_by('-id')[:9]
        url1 = urlencode({'searches':skills, 'category':category}, doseq=True)
        city_list = Jobs.objects.order_by().values_list('city', flat=True).distinct()
        print(city_list)

        return render(request, 'search.html', context={'page_obj':page_obj, 'latest':latest, 'category':category, 'skills':skills, 'url1':url1, 'city_list':city_list})

class AdFilterClass(View):
    form_class = FilterForm
    def get(self, request):
        form = self.form_class()
        category = request.GET.get('cat')
        skills = request.GET.getlist('skill')
        job_type = request.GET.get('job_type')
        state = request.GET.getlist('state')
        city = request.GET.getlist('city')


        skill_list = []
        for i in skills:
            skill_list.append(re.sub(r'(\b\w+\b)', r'+\1', i))
        if len(skills)==0:
            jobs = Jobs.objects.all()
            if job_type:
                if job_type!=5:
                    jobs = jobs.filter(job_type1=job_type)
            if state:
                jobs = jobs.filter(state__in=state)
            if city:
                jobs = jobs.filter(city__in=city)

        elif len(skills)>=1:
            if category=='hard_skill' or category=='soft_skill':
                jobs = Jobs.objects.all()
                if job_type:
                    if job_type!=5:
                        jobs = jobs.filter(job_type1=job_type, description__search=skill_list).order_by('-time_extracted')
                if state:
                    jobs = jobs.filter(state__in = state, description__search=skill_list).order_by('-time_extracted')
                if city:
                    jobs = jobs.filter(city__in = city, description__search=skill_list).order_by('-time_extracted')


            elif category=='job_role':
                jobs = Jobs.objects.all()
                if job_type:
                    if job_type!=5:
                        jobs = jobs.filter(job_type1=job_type, title__search=skill_list).order_by('-time_extracted')
                if state:
                    jobs = jobs.filter(state__in = state, title__search=skill_list).order_by('-time_extracted')
                if city:
                    jobs = jobs.filter(city__in = city, title__search=skill_list).order_by('-time_extracted')



        
        paginator = Paginator(jobs, 10)
        page_number = request.GET.get('page')
        page_obj =paginator.get_page(page_number)
        latest = Jobs.objects.all().order_by('-id')[:9]
        url1 = urlencode({'searches':skills, 'category':category}, doseq=True)
        city_list = Jobs.objects.order_by().values_list('city', flat=True).distinct()
        print(city_list)

        return render(request, 'search.html', context={'form':form,'page_obj':page_obj, 'latest':latest, 'category':category, 'skills':skills, 'job_type':job_type, 'state':state, 'url1':url1, 'city_list':city_list, 'city':city})


 
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


class JobRoleSearch(View):
    def get(self, request):
        title = request.GET.get('title')
        latest = Jobs.objects.all().order_by('-id')[:9]

        if title:
            job_role = JobTitles.objects.get(title=title)
            skills = TechSkillTitle.objects.filter(jobtitles=job_role, hot_tech='Y')
            
            paginator = Paginator(skills, 10)
            page_number = request.GET.get('page')
            page_obj =paginator.get_page(page_number)
            url1 = urlencode({'title':title}, doseq=True)

            return render(request, 'skill.html', context={'page_obj':page_obj, 'latest':latest, 'skills':skills, 'title':title, 'url1':url1})
        return render(request, 'skill.html', context={'latest':latest})
