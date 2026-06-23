import os
import re
import google.generativeai as genai
from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# A comprehensive predefined list of skills to match against, in lowercase
SKILL_DB = [
    # Technical
    'python', 'java', 'c++', 'javascript', 'html', 'css', 'sql', 'mysql',
    'postgresql', 'mongodb', 'aws', 'docker', 'kubernetes', 'git', 'django',
    'flask', 'react', 'angular', 'vue.js', 'node.js', 'spring boot', 'machine learning',
    'deep learning', 'nlp', 'natural language processing', 'scikit-learn', 'tensorflow',
    'pytorch', 'linux', 'bash', 'agile', 'scrum', 'data analysis', 'pandas', 'numpy',
    'excel', 'power bi', 'tableau', 
    
    # Business, Sales, Marketing, MBA
    'communication', 'leadership', 'problem solving', 'strategic planning', 
    'project management', 'b2b sales', 'b2c', 'crm', 'salesforce', 'hubspot',
    'digital marketing', 'seo', 'sem', 'content marketing', 'email marketing', 
    'social media marketing', 'market research', 'financial modeling', 'budgeting',
    'forecasting', 'p&l management', 'supply chain', 'operations management',
    'negotiation', 'client relations', 'business development', 'product management',
    'brand management', 'data-driven decision making', 'roi analysis'
]

def preprocess_text(text):
    """
    Cleans the raw text: lowercases, removes special characters, and extra spaces.
    """
    # Convert to lowercase
    text = text.lower()
    # Remove special characters but keep words and spaces
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_skills(text):
    """
    Extracts skills from text using a predefined skill database and regex matching.
    """
    cleaned_text = preprocess_text(text)
    
    extracted_skills = set()
    
    # Simple regex based keyword matching
    for skill in SKILL_DB:
        # Match whole words only to avoid partial matches (e.g. matching 'c' in 'contact')
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, cleaned_text):
            extracted_skills.add(skill.title())
            
    return list(extracted_skills)

def calculate_match_score(resume_text, job_desc_text):
    """
    Calculates a similarity score (0.0 to 100.0) between a resume and a job description.
    """
    if not resume_text or not job_desc_text:
        return 0.0
        
    resume_cleaned = preprocess_text(resume_text)
    job_desc_cleaned = preprocess_text(job_desc_text)
    
    # Vectorize the text
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([job_desc_cleaned, resume_cleaned])
    
    # Calculate Cosine Similarity
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    
    return round(similarity * 100, 2)

def generate_suggestions(resume_skills, resume_text, job_desc_text):
    """
    Generates actionable suggestions to improve the resume using the Google Gemini LLM API,
    falling back to rule-based logic if the API key is not configured or fails.
    """
    suggestions = []
    
    if not job_desc_text:
        return ["No job description provided for comparison."]
        
    # Attempt to use Gemini LLM for smart rewriting
    if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            You are an expert ATS (Applicant Tracking System) optimizer and Executive Resume Coach. 
            I will provide you with a candidate's resume text and a target job description. 
            
            Based on the job description, provide exactly 3 highly specific, actionable bullet points to improve the resume.
            Focus heavily on rewriting weak bullet points into strong, metric-driven accomplishments (e.g. "Instead of 'Managed team', say 'Directed a team of 5 to increase sales by 20%'").
            
            Format your response as a simple list. Do not use Markdown headings. Start each point directly.
            
            ---
            CANDIDATE RESUME:
            {resume_text[:2000]}...
            
            ---
            TARGET JOB DESCRIPTION:
            {job_desc_text[:1000]}...
            """
            
            response = model.generate_content(prompt)
            if response.text:
                # Split by newlines or dashes to form the list
                raw_suggestions = [s.strip('* -') for s in response.text.split('\n') if s.strip()]
                # Prepend an AI identifier
                suggestions = [f"**✨ AI Insight**: {s}" for s in raw_suggestions if len(s) > 10][:4]
                if suggestions:
                    return suggestions
        except Exception as e:
            print(f"Gemini API Error: {e}")
            # Fall through to rule-based logic below
    
    # ----------------------------------------------------
    # Fallback to standard Rule-Based logic if no API Key
    # ----------------------------------------------------
    
    # Find missing skills
    job_skills = extract_skills(job_desc_text)
    missing_skills = [skill for skill in job_skills if skill not in resume_skills]
    
    if missing_skills:
        suggestions.append(f"**Missing Critical Skills**: Consider adding these skills mentioned in the job description to your resume if you possess them: {', '.join(missing_skills)}.")
    else:
        suggestions.append("**Skill Match**: Great job! Your resume covers all the key skills found in the job description.")
        
    # Analyze Impact Words / Action Verbs
    impact_words = ['developed', 'led', 'managed', 'optimized', 'increased', 'decreased', 'negotiated', 'spearheaded', 'strategized', 'launched', 'architected', 'drove', 'maximized']
    found_impact_words = [word for word in impact_words if word in preprocess_text(resume_text)]
    
    if len(found_impact_words) < 3:
        suggestions.append("**Use Stronger Action Verbs**: Your resume lacks impact words. Try starting your bullet points with words like: 'Spearheaded', 'Optimized', 'Negotiated', or 'Drove' instead of passive phrases.")
    else:
        suggestions.append(f"**Action Verbs**: Good use of impact words like '{', '.join(found_impact_words[:3])}'. This helps convey a results-oriented approach.")
        
    # Check Resume Length (approximate words)
    words_count = len(resume_text.split())
    if words_count < 150:
        suggestions.append("**Resume Too Short**: Your resume seems a bit brief (under 150 words). Make sure to elaborate on your accomplishments, responsibilities, and use the STAR method for your bullet points.")
    elif words_count > 800:
        suggestions.append("**Resume Might Be Too Long**: Your resume is quite lengthy. Hiring managers typically spend only 6-7 seconds scanning a resume. Consider trimming it down to highlight relevant achievements.")
        
        suggestions.append("**💡 Pro Tip**: Add your Google Gemini API key to `settings.py` to unlock AI-powered bullet-point rewriting!")
        
    return suggestions

def generate_cover_letter(resume_text, job_desc_text):
    """
    Generates a personalized cover letter using Google Gemini LLM based on the resume and job description.
    """
    if not resume_text or not job_desc_text:
        return "Not enough data to generate a cover letter."

    if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            You are an expert career coach and executive resume writer.
            Write a complete, professional, and compelling cover letter for the candidate based on the provided resume and target job description.
            Highlight the candidate's specific skills that perfectly match the job requirements.
            Do not include placeholders like "[Your Name]" unless absolutely necessary.
            Instead, adapt to the tone and experience level found in the resume.
            Keep it structured, between 3 to 4 paragraphs, and formatted naturally without markdown headings.

            ---
            CANDIDATE RESUME:
            {resume_text[:3000]}...
            
            ---
            TARGET JOB DESCRIPTION:
            {job_desc_text[:2000]}...
            """
            
            response = model.generate_content(prompt)
            if response.text:
                return response.text
                
        except Exception as e:
            print(f"Gemini API Error during Cover Letter Generation: {e}")
            return "An error occurred while generating the cover letter with AI. Please check your API key and connection."
            
    return "The Cover Letter Generator requires a valid Google Gemini API Key. Please configure `GEMINI_API_KEY` in your `.env` file to unlock this feature."

def generate_interview_questions(resume_text, job_desc_text):
    """
    Generates 5 custom interview questions using Google Gemini LLM based on candidate's skill gaps or details.
    """
    if not resume_text or not job_desc_text:
        return "Not enough data to generate targeted interview questions."

    if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            You are a technical hiring manager and an expert recruiter.
            Review the following candidate's resume and target job description. 
            Identify the core requirements the job requires, and look at the candidate's experience.
            Based primarily on gaps in their experience, or areas where they need to provide more depth, 
            generate exactly 5 custom, highly-relevant interview questions that you would ask them during an interview.
            
            Format the output strictly as a numbered list from 1 to 5 without markdown headings or introductory filler. 

            Candidate Resume Text:
            {resume_text[:2000]}...

            Job Description:
            {job_desc_text[:2000]}...
            """
            
            response = model.generate_content(prompt)
            if response.text:
                return response.text
                
        except Exception as e:
            print(f"Gemini API Error during Interview Question generation: {e}")
            return "An error occurred while connecting to the AI for interview questions."
            
    return "Please configure the Gemini API key to activate AI Generated Interview Prep."
