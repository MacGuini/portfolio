import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse

from .models import Resume, Experience, Education, Skill, Project, Certification

from .forms import ResumeForm, EducationForm, ExperienceForm, SkillForm, ProjectForm, CertificationForm

# Resume views
@login_required(login_url='login')
def listResumes(request):
    resumes = Resume.objects.filter(user=request.user.profile)
    return render(request, 'resume/list_resumes.html', {'resumes':resumes})

@login_required(login_url='login')
def createResume(request):
    profile = request.user.profile
    form = ResumeForm()
    if request.method == "POST":
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = profile
            form.save()
            return redirect('edit-resume', pk=resume.id)
    return render(request, 'resume/create_resume.html', {'form':form})

@login_required(login_url='login')
def editResume(request, pk):
    resume = get_object_or_404(Resume, id=pk)
    form = ResumeForm(instance=resume)
    experience_form = ExperienceForm()
    education_form = EducationForm()
    skill_form = SkillForm()
    project_form = ProjectForm()
    certification_form = CertificationForm()

    if request.method == "POST":
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('edit-resume', pk=resume.id)
    else:
        form = ResumeForm(instance=resume)
    
    experiences = resume.experiences.all()
    educations = resume.educations.all()
    skills = resume.skills.all()
    projects = resume.projects.all()
    certifications = resume.certifications.all()
    
    context = {
        'form': form,
        'resume': resume,
        'resume_id': pk,
        'experience_form': experience_form,
        'education_form': education_form,
        'skill_form': skill_form,
        'project_form': project_form,
        'certification_form': certification_form,
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
        'projects': projects,
        'certifications': certifications
    }

    return render(request, 'resume/edit_resume.html', context)

@login_required(login_url='login')
def deleteResume(request, pk):
    resume = get_object_or_404(Resume, id=pk)
    if request.method == "POST":
        resume.delete()
        return redirect('list-resumes')
    return render(request, 'delete_template.html', {'object':resume})

# Experience views
@login_required(login_url='login')
def addExperience(request, pk):
    resume = get_object_or_404(Resume, id=pk)
    form = ExperienceForm()
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user.profile
            experience.save()

            # Check if any resumes are selected
            selected_resumes = request.POST.getlist('resumes')
            if selected_resumes:
                for resume_id in selected_resumes:
                    selected_resume = get_object_or_404(Resume, id=resume_id)
                    experience.resumes.add(selected_resume)
            else:
                # If no resumes are selected, add to the current resume
                experience.resumes.add(resume)

            return redirect('edit-resume', pk=resume.id)
    return render(request, 'resume/add_experience.html', {'experience_form': form, 'resume': resume})

@login_required(login_url='login')
def editExperience(request, pk):
    experience = get_object_or_404(Experience, id=pk)
    form = ExperienceForm(instance=experience)
    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get('next') or request.POST.get('next') or 'reverse(index)')
    return render(request, 'resume/edit_experience.html', {'experience_form': form})

@login_required(login_url='login')
def deleteExperience(request, pk):
    experience = get_object_or_404(Experience, id=pk)
    next_url = request.GET.get('next', 'edit-resume')
    if request.method == "POST":
        experience.delete()
        return redirect(next_url)
    return render(request, 'delete_template.html', {'object': experience})

@login_required(login_url='login')
def listExperiences(request, pk):
    resume = get_object_or_404(Resume, id=pk)
    user = resume.user
    experiences = Experience.objects.filter(user=user).order_by('position')
    experience_form = ExperienceForm()
    if request.method == "POST":
        experience_form = ExperienceForm(request.POST)
        if experience_form.is_valid():
            experience = experience_form.save(commit=False)
            experience.user = request.user.profile
            experience.save()
            experience.resumes.add(resume)
            return redirect('list-experiences', pk=pk)
    return render(request, 'resume/list_experiences.html', {'experiences': experiences, 'experience_form': experience_form, 'resume_id': pk})

# Education views
@login_required(login_url='login')
def addEducation(request, pk):
    resume = get_object_or_404(Resume, id=pk)
    form = EducationForm()
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user.profile
            education.save()
            # Check if any resumes are selected
            selected_resumes = request.POST.getlist('resumes')
            if selected_resumes:
                for resume_id in selected_resumes:
                    selected_resume = get_object_or_404(Resume, id=resume_id)
                    education.resumes.add(selected_resume)
            else:
                # If no resumes are selected, add to the current resume
                education.resumes.add(resume)

            return redirect('edit-resume', pk=resume.id)
    return render(request, 'resume/education_form.html', {'education_form': form, 'resume': resume})

@login_required(login_url='login')
def editEducation(request, pk):
    education = get_object_or_404(Education, id=pk)
    form = EducationForm(instance=education)
    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('edit-resume', pk=education.resume.id)
    return render(request, 'resume/education_form.html', {'education_form': form, 'resume': education.resume})

@login_required(login_url='login')
def deleteEducation(request, pk):
    education = get_object_or_404(Education, id=pk)
    next_url = request.GET.get('next', 'edit-resume')
    if request.method == "POST":
        education.delete()
        return redirect(next_url)    
    return render(request, 'delete_template.html', {'object': education})

# Skill views
@login_required(login_url='login')
def addSkill(request, pk):
    resume = get_object_or_404(Resume, id=pk)
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user.profile
            skill.save()
            # Check if any resumes are selected
            selected_resumes = request.POST.getlist('resumes')
            if selected_resumes:
                for resume_id in selected_resumes:
                    selected_resume = get_object_or_404(Resume, id=resume_id)
                    skill.resumes.add(selected_resume)
            else:
                # If no resumes are selected, add to the current resume
                skill.resumes.add(resume)
            return redirect('edit-resume', pk=resume.id)
    return render(request, 'resume/skill_form.html', {'skill_form': form, 'resume': resume})

@login_required(login_url='login')
def editSkill(request, pk):
    skill = get_object_or_404(Skill, id=pk)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('edit-resume', pk=skill.resume.id)
    return render(request, 'resume/skill_form.html', {'skill_form': form, 'resume': skill.resume})

@login_required(login_url='login')
def deleteSkill(request, pk):
    skill = get_object_or_404(Skill, id=pk)
    next_url = request.GET.get('next', 'edit-resume')
    if request.method == "POST":
        skill.delete()
        return redirect(next_url)
    return render(request, 'delete_template.html', {'object': skill})

# Project views
@login_required(login_url='login')
def addProject(request, pk):
    resume = get_object_or_404(Resume, id=pk)
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user.profile
            project.save()
            # Check if any resumes are selected
            selected_resumes = request.POST.getlist('resumes')
            if selected_resumes:
                for resume_id in selected_resumes:
                    selected_resume = get_object_or_404(Resume, id=resume_id)
                    project.resumes.add(selected_resume)
            else:
                # If no resumes are selected, add to the current resume
                project.resumes.add(resume)
            return redirect('edit-resume', pk=resume.id)
    return render(request, 'resume/project_form.html', {'project_form': form, 'resume': resume})

@login_required(login_url='login')
def editProject(request, pk):
    project = get_object_or_404(Project, id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('edit-resume', pk=project.resume.id)
    return render(request, 'resume/project_form.html', {'project_form': form, 'resume': project.resume})

@login_required(login_url='login')
def deleteProject(request, pk):
    project = get_object_or_404(Project, id=pk)
    next_url = request.GET.get('next', 'edit-resume')
    if request.method == "POST":
        project.delete()
        return redirect(next_url)
    return render(request, 'delete_template.html', {'object': project})

# Certification views
@login_required(login_url='login')
def addCertification(request, pk):
    resume = get_object_or_404(Resume, id=pk)
    form = CertificationForm()
    if request.method == "POST":
        form = CertificationForm(request.POST)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.user = request.user.profile
            certification.save()
            # Check if any resumes are selected
            selected_resumes = request.POST.getlist('resumes')
            if selected_resumes:
                for resume_id in selected_resumes:
                    selected_resume = get_object_or_404(Resume, id=resume_id)
                    certification.resumes.add(selected_resume)
            else:
                # If no resumes are selected, add to the current resume
                certification.resumes.add(resume)
            return redirect('edit-resume', pk=resume.id)
    return render(request, 'resume/certification_form.html', {'certification_form': form, 'resume': resume})

@login_required(login_url='login')
def editCertification(request, pk):
    certification = get_object_or_404(Certification, id=pk)
    form = CertificationForm(instance=certification)
    if request.method == "POST":
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            return redirect('edit-resume', pk=certification.resume.id)
    return render(request, 'resume/certification_form.html', {'certification_form': form, 'resume': certification.resume})

@login_required(login_url='login')
def deleteCertification(request, pk):
    certification = get_object_or_404(Certification, id=pk)
    next_url = request.GET.get('next', 'edit-resume')
    if request.method == "POST":
        certification.delete()
        return redirect(next_url)
    return render(request, 'delete_template.html', {'object': certification})

# Update order views
@csrf_protect
def update_experience_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        for item in data['order']:
            experience = Experience.objects.get(id=item['id'])
            experience.position = item['position']
            experience.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_protect
def update_education_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        for item in data['order']:
            education = Education.objects.get(id=item['id'])
            education.position = item['position']
            education.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_protect
def update_skill_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        for item in data['order']:
            skill = Skill.objects.get(id=item['id'])
            skill.position = item['position']
            skill.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_protect
def update_project_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        for item in data['order']:
            project = Project.objects.get(id=item['id'])
            project.position = item['position']
            project.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_protect
def update_certification_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        for item in data['order']:
            certification = Certification.objects.get(id=item['id'])
            certification.position = item['position']
            certification.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
