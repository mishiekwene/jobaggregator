from django.db import models

# Create your models here.
class Search(models.Lookup):
    lookup_name = 'search'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs), params

models.CharField.register_lookup(Search)
models.TextField.register_lookup(Search)



class JobTitles(models.Model):
    id = models.AutoField('id', primary_key=True)
    onetsoc_code = models.CharField('onet_id', max_length=25, db_index=True, unique=True)
    title = models.CharField('name', max_length=255)
    description = models.TextField('description')
    # tech_skills = models.ManyToManyField('api.TechSkills')

    class Meta:
        db_table = 'occupation_data'

    def __str__(self):
        return self.title

class TechSkills(models.Model):
    id = models.AutoField('id', primary_key=True)
    name = models.CharField('name', max_length=500, unique=True)
    

    def __str__(self):
        return self.name
    
class ContentModel(models.Model):
    element_id = models.CharField('element_id', max_length=20, primary_key=True)
    element_name = models.CharField('element_name', max_length=1000)
    description = models.CharField('description', max_length=1000)

    class Meta:
        db_table = 'content_model_reference'

class Abilities(models.Model):
    id = models.AutoField('id', primary_key=True)
    onetsoc_code = models.ForeignKey('api.JobTitles', on_delete=models.CASCADE, to_field='onetsoc_code')
    element_id = models.ForeignKey('api.ContentModel', on_delete=models.CASCADE, to_field='element_id')
    not_relevant = models.CharField('relevant', max_length=10, null=True)


    class Meta:
        db_table = 'abilities'


class Knowledge(models.Model):
    id = models.AutoField('id', primary_key=True)
    job_title = models.ForeignKey('api.JobTitles', on_delete=models.CASCADE, to_field='onetsoc_code')
    knowledge_content = models.ForeignKey('api.ContentModel', on_delete=models.CASCADE, to_field='element_id')
    not_relevant = models.CharField('relevant', max_length=10, null=True)

class OtherSkills(models.Model):
    id = models.AutoField('id', primary_key=True)
    job_title = models.ForeignKey('api.JobTitles', on_delete=models.CASCADE, to_field='onetsoc_code')
    other_skill_content = models.ForeignKey('api.ContentModel', on_delete=models.CASCADE, to_field='element_id')
    not_relevant = models.CharField('relevant', max_length=10, null=True)

class Jobs(models.Model):
    id = models.AutoField('id', primary_key=True)
    title = models.CharField('title', max_length=255, default="null")
    company_name = models.CharField('company_name', max_length=255, default="null")
    job_link = models.CharField('job_link', max_length=1000, default="null")
    company_link = models.CharField('company_link', max_length=1000, default="null")
    location = models.CharField('location', max_length=500, default="null")
    time_posted = models.CharField('time_posted',max_length=50, default="null")
    time_extracted = models.CharField('time_extracted',max_length=50, default="null")
    num_of_applicants = models.CharField('no_of_applicants', max_length=255, default="null")
    description = models.TextField('description', default="null")
    salary = models.CharField('salary', max_length=1000, default="null")
    rating_link = models.CharField('rating_link', max_length=100, default="null")
    rating_avg = models.CharField('rating_avg', max_length=10, default="null")
    rating_count = models.CharField('rating_count', max_length=10, default="null")
    medium = models.CharField('medium',default="null", choices=(('indeed', 'Indeed'), ('cvlib', 'CvLibrary'), ('adzuna', 'Adzuna'), ('reeds', 'Reeds'), ('guardian', 'Guardian'),
    ('jobstoday', 'JobsToday'), ('wework', 'WeWork'), ('jobsac', 'JobsAc'), ('charity', 'CharityJob'), ('findajob', 'Find a job'), ('tes', 'TES')), max_length=20)
    remote = models.BooleanField('remote')
    job_type = models.CharField('job_type', max_length=50, default='null')
    lower_sal = models.FloatField('lower_sal', null=True)
    higher_sal = models.FloatField('higher_sal', null=True)
    sal_freq = models.CharField('sal_freq', max_length=20, null=True)
    avg_sal = models.FloatField('avg_sal', null=True)
    date_posted = models.CharField('date_posted', max_length=50, null=True)
    county = models.CharField('county', max_length=100, null=True)
    state = models.CharField('state', max_length=100, null=True)
    job_type1 = models.CharField('job_type1', max_length=100, null=True)
    job_type2 = models.CharField('job_type2', max_length=100, null=True)

    def __str__(self):
        return self.title


class TechSkillTitle(models.Model):
    class Meta:
        db_table = 'occupation_data_tech_skills'

    id = models.AutoField('id', primary_key=True)
    jobtitles = models.ForeignKey('api.JobTitles',to_field='onetsoc_code', on_delete=models.CASCADE)
    techskills = models.ForeignKey('api.TechSkills',to_field='name', on_delete=models.CASCADE)
    hot_tech = models.CharField('hot_tech', max_length=5)

# class JobLocations(models.Model):
#     id = models.AutoField('id', primary_key=True)
#     name = models.CharField('location', max_length=500)
