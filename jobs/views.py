from django.shortcuts import render, get_object_or_404
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

class JobRetrieveUpdateDeleteView(APIView):
    def get(self, request, pk):
        qs = get_object_or_404(JobsDb, id=pk)
        j_instance = JobSerializer(qs)
        return Response(data= j_instance.data)

    def put(self, request, pk):
        form_data = request.data
        j_instance = JobSerializer(data= form_data)
        if j_instance.is_valid():
            actualdata = j_instance.validated_data
            JobsDb.objects.filter(id = pk).update(**actualdata)
            return Response(data= {"message":"job data updated!"})
        else:
            return Response(data= j_instance.errors)

    def delete(self, request, pk):
        JobsDb.objects.filter(id = pk).delete()
        return Response(data= {"message":"job deleted!"})