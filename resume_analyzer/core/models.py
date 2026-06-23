from django.db import models
from django.contrib.auth.models import User

class Job(models.fields.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Paste the target job description here")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    candidate_name = models.CharField(max_length=255, blank=True)
    candidate_email = models.EmailField(blank=True)
    pdf_file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # NLP Extracted Data
    extracted_text = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text="Extracted skills (comma separated)")

    def __str__(self):
        return f"{self.candidate_name or 'Anonymous'} - {self.pdf_file.name}"

class AnalysisReport(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    match_score = models.FloatField(default=0.0, help_text="Match Score Percentage")
    improvement_suggestions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.resume} against Job: {self.job.title} - {self.match_score:.2f}%"
