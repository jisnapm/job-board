from rest_framework import serializers
from jobs.models import JobsDb

class JobSerializer(serializers.Serializer):
    employer = serializers.CharField(max_length= 100)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    category = serializers.ChoiceField(choices= JobsDb.CATEGORY_CHOICES, default="software")
    experience_level = serializers.ChoiceField(choices= JobsDb.EXPERIENCE_CHOICES, default="fresher")
    location = serializers.CharField(max_length=50)
    posted_date = serializers.DateTimeField(read_only= True)
    is_open = serializers.BooleanField(default= True)