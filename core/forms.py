from django import forms
from .models import Resume, Job

class UploadResumeForm(forms.ModelForm):
    job = forms.ModelChoiceField(
        queryset=Job.objects.all(), 
        required=True,
        empty_label="Select Job Description",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Resume
        fields = ['candidate_name', 'candidate_email', 'pdf_file', 'job']
        widgets = {
            'candidate_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'candidate_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
