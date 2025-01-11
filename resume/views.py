import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse

from accounts import apps
from .models import Resume, Experience, Education, Skill, Project, Certification

from .forms import ResumeForm, EducationForm, ExperienceForm, SkillForm, ProjectForm, CertificationForm

# List resumes of the current user
@login_required(login_url='login')
def listResumes(request):
    resumes = Resume.objects.filter(user=request.user.profile)
    return render(request, 'resume/list_resumes.html', {'resumes':resumes})

# Create a new resume
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
            print("Resume is valid and saved!")
            # Return redirect to the index page with next element
            # return redirect(request.GET['next'] if 'next' in request.GET else 'index')
            return redirect('edit-resume', pk=resume.id)
        else:
            print(f"Form errors: {form.errors}")
    return render(request, 'resume/create_resume.html', {'form':form})

# Edit user resume
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
            print(f"Form errors: {form.errors}")
    else:
        form = ResumeForm(instance=resume)
    
    # Get related objects
    experiences = resume.experiences.all()
    educations = resume.educations.all()
    skills = resume.skills.all()
    projects = resume.projects.all()
    certifications = resume.certifications.all()
    
    # Prepare the template with the form and related objects

    context = {
        'form': form,
        'resume': resume,
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

# Update the order of experiences
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

# Update the order of educations
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

# Update the order of skills
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

# Update the order of projects
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

# Update the order of certifications
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

# Delete user resume
@login_required(login_url='login')
def deleteResume(request, pk):
    resume = get_object_or_404(Resume, id=pk)
    if request.method == "POST":
        resume.delete()
        return redirect('list-resumes')
    return render(request, 'delete_template.html', {'object':resume})

# Delete Expereince from resume
@login_required(login_url='login')
def deleteExperience(request, pk):
    experience = get_object_or_404(Experience, id=pk)
    next_url = request.GET.get('next', 'edit-resume')
    if request.method == "POST":
        experience.delete()
        
        return redirect(next_url)
    return render(request, 'delete_template.html', {'object': experience})

# Delete Education from resume
@login_required(login_url='login')
def deleteEducation(request, pk):
    education = get_object_or_404(Education, id=pk)
    resume = education.resume
    if request.method == "POST":
        education.delete()
        return redirect('edit-resume', pk=resume.id)
    return render(request, 'delete_template.html', {'object':education})

# Delete Skill from resume
@login_required(login_url='login')
def deleteSkill(request, pk):
    skill = get_object_or_404(Skill, id=pk)
    resume = skill.resume
    if request.method == "POST":
        skill.delete()
        return redirect('edit-resume', pk=resume.id)
    return render(request, 'delete_template.html', {'object':skill})

# Delete Project from resume
@login_required(login_url='login')
def deleteProject(request, pk):
    project = get_object_or_404(Project, id=pk)
    resume = project.resume
    if request.method == "POST":
        project.delete()
        return redirect('edit-resume', pk=resume.id)
    return render(request, 'delete_template.html', {'object':project})

# Delete Certification from resume
@login_required(login_url='login')
def deleteCertification(request, pk):
    certification = get_object_or_404(Certification, id=pk)
    resume = certification.resume
    if request.method == "POST":
        certification.delete()
        return redirect('edit-resume', pk=resume.id)
    return render(request, 'delete_template.html', {'object':certification})

# Add experience to user resume
@login_required(login_url='login')
def addExperience(request, pk):
    resume = get_object_or_404(Resume, id=pk)
    form = ExperienceForm()
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user.profile # Set the user to the current user
            experience.save()
            # Associate the experience with the resume
            resume.experiences.add(experience)
            # Redirect to the edit resume page
            return redirect('edit-resume', pk=resume.id)
        else:
            print(f"Form errors: {form.errors}")
            
        context = {
            'experience_form': form,
            'resume': resume
        }

    return render(request, 'resume/experience_form.html', context)

# Add education to user resume
@login_required(login_url='login')
def addEducation(request, pk):
    resume = get_object_or_404(Resume, id=pk)
    form = EducationForm()
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user.profile
            # Save the education object
            education.save()
            # Associate the education with the resume
            resume.educations.add(education)
            # Redirect to the edit resume page
            return redirect('edit-resume', pk=resume.id)
        else:
            print(f"Form errors: {form.errors}")
    
    return render(request, 'resume/education_form.html', {'education_form':form, 'resume':resume})

# Add skill to user resume
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
            # Associate the skill with the resume
            resume.skills.add(skill)

            # Redirect to the edit resume page
            return redirect('edit-resume', pk=resume.id)
        else:
            print(f"Form errors: {form.errors}")
    
    return render(request, 'resume/skill_form.html', {'skill_form':form, 'resume':resume})

# Add project to user resume
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
            # Associate the project with the resume
            resume.projects.add(project)

            # Redirect to the edit resume page
            return redirect('edit-resume', pk=resume.id)
        else:
            print(f"Form errors: {form.errors}")
    
    return render(request, 'resume/project_form.html', {'project_form':form, 'resume':resume})

# Add certification to user resume
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
            # Associate the certification with the resume
            resume.certifications.add(certification)

            # Redirect to the edit resume page
            return redirect('edit-resume', pk=resume.id)
        else:
            print(f"Form errors: {form.errors}")
    
    return render(request, 'resume/certification_form.html', {'certification_form':form, 'resume':resume})

# Edit experience
@login_required(login_url='login')
def editExperience(request, pk):
    experience = get_object_or_404(Experience, id=pk)
    form = ExperienceForm(instance=experience)
    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('edit-resume', pk=experience.resume.id)
        else:
            print(f"Form errors: {form.errors}")
    return render(request, 'resume/experience_form.html', {'experience_form':form, 'resume':experience.resume})

# Edit education
@login_required(login_url='login')
def editEducation(request, pk):
    education = get_object_or_404(Education, id=pk)
    form = EducationForm(instance=education)
    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('edit-resume', pk=education.resume.id)
        else:
            print(f"Form errors: {form.errors}")
    return render(request, 'resume/education_form.html', {'education_form':form, 'resume':education.resume})

# Edit skill
@login_required(login_url='login')
def editSkill(request, pk):
    skill = get_object_or_404(Skill, id=pk)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('edit-resume', pk=skill.resume.id)
        else:
            print(f"Form errors: {form.errors}")
    return render(request, 'resume/skill_form.html', {'skill_form':form, 'resume':skill.resume})

# Edit project
@login_required(login_url='login')
def editProject(request, pk):
    project = get_object_or_404(Project, id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('edit-resume', pk=project.resume.id)
        else:
            print(f"Form errors: {form.errors}")
    return render(request, 'resume/project_form.html', {'project_form':form, 'resume':project.resume})

# Edit certification
@login_required(login_url='login')
def editCertification(request, pk):
    certification = get_object_or_404(Certification, id=pk)
    form = CertificationForm(instance=certification)
    if request.method == "POST":
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            return redirect('edit-resume', pk=certification.resume.id)
        else:
            print(f"Form errors: {form.errors}")
    return render(request, 'resume/certification_form.html', {'certification_form':form, 'resume':certification.resume})