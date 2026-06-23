from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UploadResumeForm
from .models import Resume, Job, AnalysisReport
from .utils.pdf_extractor import extract_text_from_pdf
from .utils.nlp_engine import extract_skills, calculate_match_score, generate_suggestions, generate_cover_letter, generate_interview_questions

def home(request):
    if request.method == 'POST':
        form = UploadResumeForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the resume basic data
            resume = form.save(commit=False)
            if request.user.is_authenticated:
                resume.user = request.user
            resume.save()

            # Retrieve the selected job description
            job = form.cleaned_data.get('job')

            # --- NLP Processing ---
            # 1. Extract Text from PDF
            resume_text = extract_text_from_pdf(resume.pdf_file.path)
            resume.extracted_text = resume_text

            # 2. Extract Skills
            resume_skills = extract_skills(resume_text)
            resume.skills = ", ".join(resume_skills)
            resume.save()

            # 3. Calculate Match Score
            match_score = calculate_match_score(resume_text, job.description)

            # 4. Generate AI Text Artifacts
            suggestions = generate_suggestions(resume_skills, resume_text, job.description)
            cover_letter = generate_cover_letter(resume_text, job.description)
            interview_questions = generate_interview_questions(resume_text, job.description)

            # 5. Save the Analysis Report
            report = AnalysisReport.objects.create(
                resume=resume,
                job=job,
                match_score=match_score,
                improvement_suggestions="\n".join(suggestions),
                cover_letter=cover_letter,
                interview_questions=interview_questions
            )

            return redirect('analysis_result', pk=report.pk)
    else:
        form = UploadResumeForm()

    return render(request, 'core/upload.html', {'form': form})

def analysis_result(request, pk):
    report = get_object_or_404(AnalysisReport, pk=pk)
    
    # Passing split suggestions to iterate over in template
    suggestions_list = report.improvement_suggestions.split("\n") if report.improvement_suggestions else []
    skills_list = report.resume.skills.split(", ") if report.resume.skills else []

    context = {
        'report': report,
        'resume': report.resume,
        'job': report.job,
        'suggestions_list': suggestions_list,
        'skills_list': skills_list
    }
    return render(request, 'core/result.html', context)

# --- Authentication Views ---

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('dashboard')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

# --- Dashboard View ---

@login_required
def dashboard(request):
    # Fetch all resumes uploaded by the current user
    resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
    
    # Pre-fetch the related AnalysisReports if any
    reports = AnalysisReport.objects.filter(resume__user=request.user).select_related('resume', 'job').order_by('-created_at')
    
    context = {
        'resumes': resumes,
        'reports': reports,
    }
    return render(request, 'core/dashboard.html', context)
