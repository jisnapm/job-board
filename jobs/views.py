from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from jobs.models import JobsDb
from jobs.serializer import JobSerializer

# Create your views here.
class JobListCreateView(APIView):
    def get(self, request):
        qs = JobsDb.objects.all()
        job_instance = JobSerializer(qs, many= True)
        return Response(data= job_instance.data)

    def post(self, request):
        form_data = request.data
        job_instance = JobSerializer(data= form_data)
        if job_instance.is_valid():
            actualdata = job_instance.validated_data 
            JobsDb.objects.create(**actualdata)
            return Response(data= {"message":"jobs posted!"})
        else:
            return Response(data= job_instance.errors)