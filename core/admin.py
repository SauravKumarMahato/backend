from django.contrib import admin
from . import models
from django.urls import reverse
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.db.models import F

# Register your models here.

admin.site.site_header = 'Lesson Plan Management'
admin.site.index_title = 'Admin'

#user
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'subject_count']
    search_fields = ['username']

    def subject_count(self, user):
        subject_count = user.subject_set.count()
        url = reverse('admin:core_subject_changelist') + '?' + urlencode({'user__id': str(user.id)})
        return format_html('<a href ="{}">{}</a>', url, subject_count)


#subject
@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['sub_name', 'sectionyear_count']
    search_fields = ['sub_name']
    autocomplete_fields = ['user']

    def sectionyear_count(self, subject):
        sectionyear_count = subject.sectionyear_set.count()
        url = reverse('admin:core_sectionyear_changelist') + '?' + urlencode({'subject__id': str(subject.id)})
        return format_html('<a href ="{}">{}</a>', url, sectionyear_count)
    

#section and year
@admin.register(models.SectionYear)
class SectionYearAdmin(admin.ModelAdmin):
    list_display = ['section', 'plan_count', 'chapter_count']
    search_fields = ['section']
    autocomplete_fields = ['subject']
    
    def plan_count(self, section_year):
        plan_count = section_year.plan_set.count()
        url = reverse('admin:core_plan_changelist') + '?' + urlencode({'section_year__id': str(section_year.id)})
        return format_html('<a href ="{}">{}</a>', url, plan_count)
    
    def chapter_count(self, section_year):
        chapter_count = section_year.chapter_set.count()
        url = reverse('admin:core_chapter_changelist') + '?' + urlencode({'section_year__id': str(section_year.id)})
        return format_html('<a href ="{}">{}</a>', url, chapter_count)
        
    
#plan
@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['plan_name', 'activity_count', 'test_count']
    search_fields = ['plan_name']
    autocomplete_fields = ['sectionyear']
    
    def activity_count(self, plan):
        activity_count = plan.activity_set.count()
        url = reverse('admin:core_activity_changelist') + '?' + urlencode({'plan__id': str(plan.id)})
        return format_html('<a href ="{}">{}</a>', url, activity_count)
    
    def test_count(self, plan):
        test_count = plan.test_set.count()
        url = reverse('admin:core_test_changelist') + '?' + urlencode({'plan__id': str(plan.id)})
        return format_html('<a href ="{}">{}</a>', url, test_count)
   

#activity
@admin.register(models.Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_detail']
    search_fields = ['activity_detail']
    autocomplete_fields = ['plan']


#test
@admin.register(models.Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['test_detail']
    search_fields = ['test_detail']
    autocomplete_fields = ['plan']


#chapter
@admin.register(models.Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['chapter_name', 'topic_count', 'assignment_count', 'resource_count']
    search_fields = ['chapter_name']
    autocomplete_fields = ['section_year']
    
    def topic_count(self, chapter):
        topic_count = chapter.topic_set.count()
        url = reverse('admin:core_topic_changelist') + '?' + urlencode({'chapter__id': str(chapter.id)})
        return format_html('<a href ="{}">{}</a>', url, topic_count)

    def assignment_count(self, chapter):
        assignment_count = chapter.assignment_set.count()
        url = reverse('admin:core_assignment_changelist') + '?' + urlencode({'chapter__id': str(chapter.id)})
        return format_html('<a href ="{}">{}</a>', url, assignment_count)
    
    def resource_count(self, chapter):
        resource_count = chapter.resource_set.count()
        url = reverse('admin:core_resource_changelist') + '?' + urlencode({'chapter__id': str(chapter.id)})
        return format_html('<a href ="{}">{}</a>', url, resource_count)
    

#assignment
@admin.register(models.Topic)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['topic_name']
    search_fields = ['topic_name']
    autocomplete_fields = ['chapter']

#assignment
@admin.register(models.Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['assign_name', 'updated_date', 'file']
    search_fields = ['assign_name']
    autocomplete_fields = ['chapter']


#resource
@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['res_name', 'updated_date', 'file']
    search_fields = ['res_name']
    autocomplete_fields = ['chapter']

