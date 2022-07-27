from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from . import models
from . import serializers

# Create your views here.
class JobListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.JobSerializer
    queryset = models.Jobs.objects.all()
    def get(self, request, format=None):
        jobs = models.Jobs.objects.all()
        page = self.paginate_queryset(jobs)
        serializer = serializers.JobSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobRetrieve(APIView):
    serializer_class = serializers.JobSerializer
    def get_object(self, pk):
        try:
            return models.Jobs.objects.get(pk=pk)
        except models.Jobs.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        job = self.get_object(pk)
        serializer = serializers.JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        job = self.get_object(pk)
        serializer = serializers.JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        job = self.get_object(pk)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

