from django.contrib import admin
from .models import Job, Resume, AnalysisReport

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'candidate_email', 'uploaded_at')
    search_fields = ('candidate_name', 'candidate_email')
    list_filter = ('uploaded_at',)

@admin.register(AnalysisReport)
class AnalysisReportAdmin(admin.ModelAdmin):
    list_display = ('resume', 'job', 'match_score', 'created_at')
    list_filter = ('job', 'created_at')
    search_fields = ('resume__candidate_name',)
