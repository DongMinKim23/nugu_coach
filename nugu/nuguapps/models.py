from django.db import models

# Create your models here.
class Schedule(models.Model):
    # date = models.DateTimeField()

    month = models.IntegerField()
    day = models.IntegerField()
    start_time = models.IntegerField()
    name = models.CharField(max_length=20)
    
    check = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Sub_test(models.Model):
    year = models.IntegerField()
    date = models.DateTimeField()
    seq = models.IntegerField()    


class Main_test(models.Model):
    year = models.IntegerField()
    date = models.DateTimeField()
    seq = models.IntegerField()
    
class Ranked_cut(models.Model):
    college = models.CharField(max_length=20)
    grade_cut = models.FloatField()
    # kor_lang = models.IntegerField()
    # math = models.IntegerField()
    # Eng = models.IntegerField()
    # science = models.IntegerField()
    # society = models.IntegerField()
    
class Care(models.Model):
    symptom = models.CharField(max_length=20)
    food = models.TextField(default=False)
    sport = models.TextField(default=False)
    
class stretch(models.Model):
    symptom = models.CharField(max_length=20)
    action = models.TextField(default=False)