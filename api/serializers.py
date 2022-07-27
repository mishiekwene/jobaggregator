from rest_framework import serializers
from .models import Jobs

class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Jobs
        fields = '__all__'
    
    def create(self, validated_data):
        job, created = Jobs.objects.get_or_create(description= validated_data['description'], title=validated_data['title'], job_link=validated_data['job_link'], medium=validated_data['medium'],
        defaults={"company_name":validated_data.get('company_name', 'null'), "company_link":validated_data.get('company_link', 'null'),"location":validated_data.get('location', 'null'),"num_of_applicants":validated_data.get('num_of_applicants', 'null'),
        "remote":validated_data.get('remote', 0), "salary":validated_data.get('salary', 'null'), "time_extracted":validated_data.get('time_extracted', 'null'), "time_posted":validated_data.get('time_posted', 'null'), "job_type":validated_data.get('job_type', 'null'),
        })
        return job
