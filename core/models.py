from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

#user
class User(AbstractUser):
  pass
#subject
class Subject(models.Model):
  sub_name = models.CharField(max_length=225)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self) -> str:
    return self.sub_name

#section and year
class SectionYear(models.Model):
  section = models.CharField(max_length=255)
  subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

  def __str__(self) -> str:
    sec_yr = self.section + " " + self.year
    return sec_yr

#chapter
class Chapter(models.Model):
  chapter_name = models.CharField(max_length=255)
  section_year = models.ForeignKey(SectionYear, on_delete=models.CASCADE)

  def __str__(self) -> str:
    return self.chapter_name
  
  #topic
class Topic(models.Model):
  topic_name = models.CharField(max_length=255)
  chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

  def __str__(self) -> str:
    return self.topic_name

#plan
class Plan(models.Model):
  plan_name = models.CharField(max_length=255)
  sectionyear = models.ForeignKey(SectionYear, on_delete=models.CASCADE)

  def __str__(self) -> str:
    return self.plan_name


#assignment
class Assignment(models.Model):
  assign_name = models.CharField(max_length=255)
  updated_date = models.DateField(auto_now=True)
  file = models.FileField(upload_to='core/assignment/files')
  chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

  def __str__(self) -> str:
    return self.assign_name

#resource
class Resource(models.Model):
  res_name = models.CharField(max_length=255)
  updated_date = models.DateField(auto_now=True)
  file = models.FileField(upload_to='core/resource/files')
  chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

  def __str__(self) -> str:
    return self.res_name


# # chapters in plan
# class PlanChapter(models.Model):
#   plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
#   chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)


# topics in Plan
class PlanTopic(models.Model):
  plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
  chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE)


# assignments in Plan
class PlanAssignment(models.Model):
  plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
  chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
  assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)


# resources in Plan
class PlanResource(models.Model):
  plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
  chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
  resource = models.ForeignKey(Resource, on_delete=models.CASCADE)


#test
class Test(models.Model):
  test_detail = models.CharField(max_length=255)
  plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

  def __str__(self) -> str:
    return self.test_detail


#activity
class Activity(models.Model):
  activity_detail = models.CharField(max_length=255)
  plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

  def __str__(self) -> str:
    return self.activity_detail

