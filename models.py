from django.db import models
from datetime import datetime

class Person(models.Model):
    full_name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    
    father_name = models.CharField(max_length=200, blank=True, null=True)
    mother_name = models.CharField(max_length=200, blank=True, null=True)
    siblings = models.TextField(blank=True, null=True)
    
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=120, blank=True, null=True)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    vk_profile = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    other_social = models.TextField(blank=True, null=True)
    
    current_address = models.CharField(max_length=500, blank=True, null=True)
    home_address = models.CharField(max_length=500, blank=True, null=True)
    work_address = models.CharField(max_length=500, blank=True, null=True)
    
    work_place = models.CharField(max_length=300, blank=True, null=True)
    job_title = models.CharField(max_length=200, blank=True, null=True)
    education = models.CharField(max_length=300, blank=True, null=True)
    school = models.CharField(max_length=300, blank=True, null=True)
    
    car_info = models.CharField(max_length=200, blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    photos = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(default=datetime.utcnow)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.CharField(max_length=100, default='Анонимный')

    class Meta:
        managed = True
        db_table = 'person'
        app_label = 'cyber_models' 

    def __str__(self):
        return f'{self.full_name} ({self.id})'

class SearchHistory(models.Model):
    search_query = models.CharField(max_length=500)
    search_type = models.CharField(max_length=50)
    searched_at = models.DateTimeField(default=datetime.utcnow)
    results_count = models.IntegerField(default=0)
    ip_address = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'search_history'
        app_label = 'cyber_models' 