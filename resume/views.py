import json
from django.apps import apps
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect # Keep for your AJAX views
from django.urls import reverse # For safer redirects

from .utils import save_section
from .models import Resume, Experience, Education, Skill, Project, Certification
from .forms import (
    ResumeForm, EducationForm, ExperienceForm, SkillForm, ProjectForm, CertificationForm
)


# map the URL-friendly name to model, form & template
SECTION_MAP = {
    'experience': {
        'model':  'resume.Experience',
        'form':    ExperienceForm,
        'template':'resume/section_form.html',
    },
    'education': {
        'model':   'resume.Education',
        'form':     EducationForm,
        'template': 'resume/section_form.html',
    },
    'skill': {
        'model':   'resume.Skill',
        'form':     SkillForm,
        'template': 'resume/section_form.html',
    },
    'project': {
        'model':   'resume.Project',
        'form':     ProjectForm,
        'template': 'resume/section_form.html',
    },
    'certification': {
        'model':   'resume.Certification',
        'form':     CertificationForm,
        'template': 'resume/section_form.html',
    },
}

@login_required(login_url='login')
def section_form(request, section, resume_pk=None, pk=None, action='add'):
    """
    action: 'add', 'edit' or 'delete'
    section: one of the keys in SECTION_MAP
    resume_pk: for context when adding
    pk: the item‐id when editing/deleting
    """
    cfg = SECTION_MAP.get(section)
    if not cfg:
        raise Http404("Unknown section")

    Model    = apps.get_model(cfg['model'])
    FormClass= cfg['form']
    tpl      = cfg['template']
    user_prof= request.user.profile

    # fetch instance for edit/delete
    instance = None
    if action in ('edit','delete'):
        instance = get_object_or_404(Model, id=pk, user=user_prof)

    if request.method == 'POST':
        form = FormClass(request.POST, instance=instance, user=user_prof)
        if form.is_valid():
            if action == 'delete':
                instance.delete()
            else:
                save_section(form, user_prof, resume_pk)
                target = (reverse('edit-resume', args=[resume_pk])
                          if resume_pk else reverse('resume-dashboard'))
                return redirect(target)
    else:
        form = FormClass(instance=instance, user=user_prof)

    return render(request, 'resume/section_form.html', {
        'form':        form,
        'button_icon': {'add':'+','edit':'✎','delete':'🗑'}[action],
        'button_label': {'add':'Add','edit':'Save','delete':'Delete'}[action] + ' ' + section.title(),
        'action_url':  (reverse(f"{'add' if action=='add' else action}-section",
                          args=[resume_pk, section]) if resume_pk else
                        reverse(f"{action}-section", args=[section, pk])),
    })

@login_required(login_url='login')
def resumeDashboard(request):
    # Fetches and displays resumes belonging to the currently logged-in user's profile.
    current_user_profile = request.user.profile
    resumes = Resume.objects.filter(user=current_user_profile)
    creatorProfile = request.user.profile
    experiences = Experience.objects.filter(user=current_user_profile)
    educations = Education.objects.filter(user=current_user_profile)
    skills = Skill.objects.filter(user=current_user_profile)
    projects = Project.objects.filter(user=current_user_profile)
    certifications = Certification.objects.filter(user=current_user_profile)


    experience_add_form = ExperienceForm(user=current_user_profile)
    education_add_form = EducationForm(user=current_user_profile)
    skill_add_form = SkillForm(user=current_user_profile)
    project_add_form = ProjectForm(user=current_user_profile)
    certification_add_form = CertificationForm(user=current_user_profile)

    # Prepare an "edit" form for each instance
    experience_edit_forms = {
        exp.id: ExperienceForm(instance=exp, user=current_user_profile)
        for exp in experiences
    }
    education_edit_forms = {
        edu.id: EducationForm(instance=edu, user=current_user_profile)
        for edu in educations
    }
    skill_edit_forms = {
        skill.id: SkillForm(instance=skill, user=current_user_profile)
        for skill in skills
    }
    project_edit_forms = {
        proj.id: ProjectForm(instance=proj, user=current_user_profile)
        for proj in projects
    }
    certification_edit_forms = {
        cert.id: CertificationForm(instance=cert, user=current_user_profile)
        for cert in certifications
    }

     # Add these forms to the context

    context = {
        'resumes': resumes,
        'creatorProfile': creatorProfile,
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
        'experience_add_form': experience_add_form,
        'education_add_form': education_add_form,
        'skill_add_form': skill_add_form,
        'project_add_form': project_add_form,
        'certification_add_form': certification_add_form,
        'experience_edit_forms': experience_edit_forms,
        'education_edit_forms': education_edit_forms,
        'skill_edit_forms': skill_edit_forms,
        'project_edit_forms': project_edit_forms,
        'certification_edit_forms': certification_edit_forms,

    }
    return render(request, 'resume/resume_dashboard.html', context)

@login_required(login_url='login')
def createResume(request):
    # Handles the creation of a new resume.
    current_user_profile = request.user.profile
    if request.method == "POST":
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = current_user_profile # Assign ownership to the current user's profile
            resume.save() # Save the resume instance to get an ID
            # If ResumeForm had ManyToMany fields, you would call form.save_m2m() here
            return redirect('edit-resume', pk=resume.id)
    else:
        form = ResumeForm()
    return render(request, 'resume/create_resume.html', {'form': form})

@login_required(login_url='login')
def editResume(request, pk):
    # Handles editing of an existing resume
    # Similar to resumeDashboard, but scoped to one Resume.
    # 'pk' is the ID of the Resume being edited.
    current_user_profile = request.user.profile
    # Ensure the resume belongs to the current user
    resume = get_object_or_404(Resume, id=pk, user=current_user_profile)

    if request.method == "POST":
        # This POST request is for updating the main Resume object itself
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('edit-resume', pk=resume.id) # Redirect back to the same edit page
    else:
        form = ResumeForm(instance=resume) # For GET request, pre-fill with resume instance

    # Initialize forms for related sections, passing the user profile for context
    # This allows these forms to correctly list the user's other resumes if they have such a field.
    experience_form = ExperienceForm(user=current_user_profile)
    education_form = EducationForm(user=current_user_profile)
    skill_form = SkillForm(user=current_user_profile)
    project_form = ProjectForm(user=current_user_profile)
    certification_form = CertificationForm(user=current_user_profile)
    
    # Fetch related items for display
    experiences = resume.experiences.all()
    educations = resume.educations.all()
    skills = resume.skills.all()
    projects = resume.projects.all()
    certifications = resume.certifications.all()
    
    context = {
        'form': form, # Form for editing the Resume model
        'resume': resume,
        'resume_id': pk, # Same as resume.id, for convenience in template
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
    # Handles deletion of a resume.
    current_user_profile = request.user.profile
    # Ensure the user can only delete their own resumes
    resume = get_object_or_404(Resume, id=pk, user=current_user_profile)
    if request.method == "POST":
        resume.delete()
        return redirect('resume-dashboard') # Redirect to the list of resumes
    return render(request, 'delete_template.html', {'object': resume})

# === Experience Views ===

# addExperience is a more general view that allows adding experiences without being tied to a specific resume.
@login_required(login_url='login')
def addExperience(request):
    # Adds a new experience, not tied to a specific resume.
    current_user_profile = request.user.profile

    if request.method == "POST":
        form = ExperienceForm(request.POST, user=current_user_profile)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = current_user_profile # Assign ownership
            experience.save()
            # Handle M2M 'resumes' association from form's cleaned_data
            selected_resume_objects = form.cleaned_data.get('resumes', [])
            if selected_resume_objects:
                experience.resumes.set(selected_resume_objects)
            # If no resumes selected in form, it won't be associated with any resumes
            return redirect('resume-dashboard') # Redirect to resume dashboard or another page
    else: # GET request
        form = ExperienceForm(user=current_user_profile) # Pass user for resume choices
    return render(request, 'resume/add_experience.html', {'experience_form': form})

# addExperience is a more general view that allows adding experiences without being tied to a specific resume.
@login_required(login_url='login')
def addExperienceFromResume(request, pk):
    # Adds a new experience, potentially associating it with one or more resumes.
    # 'pk' is the ID of the primary resume this experience is being added in context of.
    current_user_profile = request.user.profile
    # Ensure the context resume belongs to the current user
    resume_context = get_object_or_404(Resume, id=pk, user=current_user_profile)

    if request.method == "POST":
        form = ExperienceForm(request.POST, user=current_user_profile)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = current_user_profile # Assign ownership
            experience.save() # Save the experience object to get an ID

            # Handle association with selected resumes
            # form.cleaned_data['resumes'] should contain valid Resume instances if form is ModelForm
            # and resumes field is set up correctly and validated.
            selected_resume_objects = form.cleaned_data.get('resumes', [])
            if selected_resume_objects:
                experience.resumes.set(selected_resume_objects) # Use set() for M2M assignment
            elif resume_context: # If no resumes selected in form, associate with the context resume
                experience.resumes.add(resume_context)
            # If you want to ensure it's always added to resume_context regardless of selection:
            # experience.resumes.add(resume_context) # Add this line after .set() or .add() if needed

            return redirect('edit-resume', pk=resume_context.id)
    else: # GET request
        # Initialize the form, passing user profile to populate resume choices
        form = ExperienceForm(user=current_user_profile)
        
    return render(request, 'resume/add_experience_from_resume.html', {'experience_form': form, 'resume': resume_context})

@login_required(login_url='login')
def editExperience(request, pk):
    # Edits an existing experience. 'pk' is the ID of the Experience object.
    current_user_profile = request.user.profile
    # Ensure the experience being edited belongs to the current user
    experience_instance = get_object_or_404(Experience, id=pk, user=current_user_profile)

    if request.method == "POST":
        # Pass instance for editing and user profile for resume choices
        form = ExperienceForm(request.POST, instance=experience_instance, user=current_user_profile)
        if form.is_valid():
            form.save() # ModelForm's save() handles M2M if 'resumes' field is part of the form
            
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url: # TODO: Validate next_url to prevent open redirect vulnerabilities
                return redirect(next_url)
            else:
                # default redirect if 'next' is not provided
                primary_resume = experience_instance.resumes.first()

                if primary_resume:
                    return redirect('edit-resume', pk=primary_resume.id)
                return redirect(reverse('resume-dashboard')) # Fallback to a general page
    else: # GET request
        # Pre-fill form with experience data and provide user profile for resume choices
        form = ExperienceForm(instance=experience_instance, user=current_user_profile)
        
    context = {
        'experience_form': form,
        'experience': experience_instance
    }
    return render(request, 'resume/edit_experience.html', context)

@login_required(login_url='login')
def deleteExperience(request, pk):
    # Handles deletion of an experience.
    current_user_profile = request.user.profile
    # Ensure the user can only delete their own experiences
    experience = get_object_or_404(Experience, id=pk, user=current_user_profile)
    
    # Determine redirect URL (e.g., back to the resume it was part of)
    # This assumes 'next' is passed, or defaults to a generic resume edit page if not.
    # You might want a more robust way to determine the redirect, e.g., based on experience.resumes.
    primary_resume = experience.resumes.first()
    default_redirect_url = reverse('resume-dashboard') # Default if no associated resume or next
    if primary_resume:
        default_redirect_url = reverse('edit-resume', kwargs={'pk': primary_resume.id})
        
    next_url = request.GET.get('next', default_redirect_url)

    if request.method == "POST":
        experience.delete()
        return redirect(next_url)
        
    return render(request, 'delete_template.html', {'object': experience, 'next_url': next_url})

@login_required(login_url='login')
def listExperiences(request, pk):
    # This view seems to list experiences FOR a specific resume and allows adding a new one to IT.
    current_user_profile = request.user.profile
    # Ensure the resume context belongs to the current user
    resume_context = get_object_or_404(Resume, id=pk, user=current_user_profile)
    
    # Experiences listed are those owned by the user who owns the resume_context
    # (which should be current_user_profile due to the check above)
    # And further filtered to only those associated with this specific resume_context
    experiences = resume_context.experiences.filter(user=current_user_profile).order_by('position')

    if request.method == "POST":
        # Form for adding a NEW experience directly to this resume_context
        experience_form = ExperienceForm(request.POST, user=current_user_profile)
        if experience_form.is_valid():
            experience = experience_form.save(commit=False)
            experience.user = current_user_profile # Assign ownership
            experience.save() # Save to get ID
            experience.resumes.add(resume_context) # Associate with this specific resume
            # If 'resumes' was a field in this form, handle other selections too:
            # selected_resume_objects = experience_form.cleaned_data.get('resumes', [])
            # for res in selected_resume_objects:
            #    experience.resumes.add(res) # Ensures all selected are added

            return redirect('list-experiences', pk=pk) # Redirect back to this list
    else: # GET request
        experience_form = ExperienceForm(user=current_user_profile)
        
    context = {
        'experiences': experiences,
        'experience_form': experience_form,
        'resume': resume_context, # Pass resume for context (e.g., displaying its title)
        'resume_id': pk # For URLs or other logic in template
    }
    return render(request, 'resume/list_experiences.html', context)

# === Education Views ===
# Applying similar logic as Experience views

# addEducation is a more general view that allows adding education without being tied to a specific resume.
@login_required(login_url='login')
def addEducation(request):
    # Adds a new education, not tied to a specific resume.
    current_user_profile = request.user.profile

    if request.method == "POST":
        form = EducationForm(request.POST, user=current_user_profile)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = current_user_profile
            education.save()
            # Handle M2M 'resumes' association from form's cleaned_data
            selected_resume_objects = form.cleaned_data.get('resumes', [])
            if selected_resume_objects:
                education.resumes.set(selected_resume_objects)
            # If no resumes selected in form, it won't be associated with any resumes
            return redirect('resume-dashboard') # Redirect to resume dashboard or another page
    else: # GET request
        form = EducationForm(user=current_user_profile) # Pass user for resume choices
    return render(request, 'resume/add_education.html', {'education_form': form})

# addEducationFromResume is exclusive to the 'edit-resume' functionality, allowing users to add education while editing a specific resume.# This view must pass a 'pk' to link it to the resume the user is currently editing
@login_required(login_url='login')
def addEducationFromResume(request, pk):
    # Adds a new education item, potentially associating it with one or more resumes.
    # 'pk' is the ID of the primary resume this education is being added in context of.
    current_user_profile = request.user.profile
    resume_context = get_object_or_404(Resume, id=pk, user=current_user_profile)

    if request.method == "POST":
        form = EducationForm(request.POST, user=current_user_profile)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = current_user_profile
            education.save()

            selected_resume_objects = form.cleaned_data.get('resumes', [])
            if selected_resume_objects:
                education.resumes.set(selected_resume_objects)
            elif resume_context: # If no resumes selected in form, associate with the context resume
                education.resumes.add(resume_context)
            # Optional: education.resumes.add(resume_context) # To always add to current context

            return redirect('edit-resume', pk=resume_context.id)
    else: # GET request
        form = EducationForm(user=current_user_profile)
        
    return render(request, 'resume/add_education_from_resume.html', {'education_form': form, 'resume': resume_context})

@login_required(login_url='login')
def editEducation(request, pk):
    # Edits an existing education item. 'pk' is the ID of the Education object.
    current_user_profile = request.user.profile
    # Ensure the education being edited belongs to the current user
    education_instance = get_object_or_404(Education, id=pk, user=current_user_profile)

    if request.method == "POST":
        # Pass instance for editing and user profile for resume choices
        form = EducationForm(request.POST, instance=education_instance, user=current_user_profile)

        if form.is_valid():
            form.save() # ModelForm's save() handles M2M if 'resumes' field is part of the form
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url: # TODO: Validate next_url
                return redirect(next_url)
            else:
                primary_resume = education_instance.resumes.first()
                if primary_resume:
                    return redirect('edit-resume', pk=primary_resume.id)
                return redirect(reverse('resume-dashboard'))
    else: # GET request
        form = EducationForm(instance=education_instance, user=current_user_profile)
        
    context = {
        'education_form': form,
        'education': education_instance
    }
    return render(request, 'resume/edit_education.html', context)

@login_required(login_url='login')
def deleteEducation(request, pk):
    # Handles deletion of an education item.
    current_user_profile = request.user.profile
    education = get_object_or_404(Education, id=pk, user=current_user_profile)
    
    primary_resume = education.resumes.first()
    default_redirect_url = reverse('resume-dashboard')
    if primary_resume:
        default_redirect_url = reverse('edit-resume', kwargs={'pk': primary_resume.id})
    next_url = request.GET.get('next', default_redirect_url)

    if request.method == "POST":
        education.delete()
        return redirect(next_url)
        
    return render(request, 'delete_template.html', {'object': education, 'next_url': next_url})

# === Skill Views ===

# addSkill is a more general view that allows adding skills without being tied to a specific resume.
@login_required(login_url='login')
def addSkill(request):
    # Adds a new skill, not tied to a specific resume.
    current_user_profile = request.user.profile

    if request.method == "POST":
        form = SkillForm(request.POST, user=current_user_profile)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = current_user_profile
            skill.save() # Save skill to get an ID
            # Handle M2M 'resumes' association from form's cleaned_data
            selected_resume_objects = form.cleaned_data.get('resumes', [])
            if selected_resume_objects:
                skill.resumes.set(selected_resume_objects)
            # If no resumes selected in form, it won't be associated with any resumes
            return redirect('resume-dashboard') # Redirect to resume dashboard or another page
    else: # GET request
        form = SkillForm(user=current_user_profile) # Pass user for resume choices
    return render(request, 'resume/add_skill.html', {'skill_form': form})


# addSkillFromResume is exclusive to the 'edit-resume' functionality, allowing users to add skills while editing a specific resume.
# This view must pass a 'pk' to link it to the resume the user is currently editing.
@login_required(login_url='login')
def addSkillFromResume(request, pk):
    # Adds a new skill, potentially associating it with one or more resumes.
    # 'pk' is the ID of the primary resume this skill is being added in context of.
    current_user_profile = request.user.profile
    resume_context = get_object_or_404(Resume, id=pk, user=current_user_profile)

    if request.method == "POST":
        form = SkillForm(request.POST, user=current_user_profile) # Pass user for resume choices
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = current_user_profile # Assign ownership
            skill.save() # Save skill to get an ID

            # Handle M2M 'resumes' association from form's cleaned_data
            selected_resume_objects = form.cleaned_data.get('resumes', [])
            if selected_resume_objects:
                skill.resumes.set(selected_resume_objects)
            elif resume_context: # If no resumes selected in form, associate with the context resume
                skill.resumes.add(resume_context)
            # Optional: skill.resumes.add(resume_context) # To always add to current context

            return redirect('edit-resume', pk=resume_context.id)
    else: # GET request
        form = SkillForm(user=current_user_profile) # Pass user for resume choices
        
    return render(request, 'resume/add_skill_from_resume.html', {'skill_form': form, 'resume': resume_context})

@login_required(login_url='login')
def editSkill(request, pk):
    # Edits an existing skill. 'pk' is the ID of the Skill object.
    current_user_profile = request.user.profile
    skill_instance = get_object_or_404(Skill, id=pk, user=current_user_profile) # Secure fetch

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill_instance, user=current_user_profile) # Pass instance and user
        if form.is_valid():
            form.save() # ModelForm's save handles M2M
            
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url: # TODO: Validate next_url
                return redirect(next_url)
            else:
                primary_resume = skill_instance.resumes.first()
                if primary_resume:
                    return redirect('edit-resume', pk=primary_resume.id)
                return redirect(reverse('resume-dashboard')) 
    else: # GET request
        form = SkillForm(instance=skill_instance, user=current_user_profile) # Pass instance and user
        
    context = {
        'skill_form': form,
        'skill': skill_instance
    }
    return render(request, 'resume/edit_skill.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    # Handles deletion of a skill.
    current_user_profile = request.user.profile
    skill = get_object_or_404(Skill, id=pk, user=current_user_profile) # Secure fetch
    
    primary_resume = skill.resumes.first()
    default_redirect_url = reverse('resume-dashboard')
    if primary_resume:
        default_redirect_url = reverse('edit-resume', kwargs={'pk': primary_resume.id})
    next_url = request.GET.get('next', default_redirect_url)

    if request.method == "POST":
        skill.delete()
        return redirect(next_url)
        
    return render(request, 'delete_template.html', {'object': skill, 'next_url': next_url})

# === Project Views ===
# Assuming Project model has 'user' (FK to Profile) and 'resumes' (M2M to Resume)
# Assuming ProjectForm is like ExperienceForm

@login_required(login_url='login')
def addProject(request, pk):
    # Adds a new project, potentially associating it with one or more resumes.
    # 'pk' is the ID of the primary resume this project is being added in context of.
    current_user_profile = request.user.profile
    resume_context = get_object_or_404(Resume, id=pk, user=current_user_profile)

    if request.method == "POST":
        form = ProjectForm(request.POST, user=current_user_profile)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user_profile
            project.save()

            selected_resume_objects = form.cleaned_data.get('resumes', [])
            if selected_resume_objects:
                project.resumes.set(selected_resume_objects)
            elif resume_context:
                project.resumes.add(resume_context)
            # Optional: project.resumes.add(resume_context)

            return redirect('edit-resume', pk=resume_context.id)
    else: # GET request
        form = ProjectForm(user=current_user_profile)
        
    return render(request, 'resume/project_form.html', {'project_form': form, 'resume': resume_context})

@login_required(login_url='login')
def editProject(request, pk):
    # Edits an existing project. 'pk' is the ID of the Project object.
    current_user_profile = request.user.profile
    project_instance = get_object_or_404(Project, id=pk, user=current_user_profile)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project_instance, user=current_user_profile)
        if form.is_valid():
            form.save()
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url: # TODO: Validate next_url
                return redirect(next_url)
            else:
                primary_resume = project_instance.resumes.first()
                if primary_resume:
                    return redirect('edit-resume', pk=primary_resume.id)
                return redirect(reverse('resume-dashboard'))
    else: # GET request
        form = ProjectForm(instance=project_instance, user=current_user_profile)
        
    context = {
        'project_form': form,
        'project': project_instance
    }
    return render(request, 'resume/edit_project.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):
    # Handles deletion of a project.
    current_user_profile = request.user.profile
    project = get_object_or_404(Project, id=pk, user=current_user_profile)
    
    primary_resume = project.resumes.first()
    default_redirect_url = reverse('resume-dashboard')
    if primary_resume:
        default_redirect_url = reverse('edit-resume', kwargs={'pk': primary_resume.id})
    next_url = request.GET.get('next', default_redirect_url)

    if request.method == "POST":
        project.delete()
        return redirect(next_url)
        
    return render(request, 'delete_template.html', {'object': project, 'next_url': next_url})

# === Certification Views ===
# Assuming Certification model has 'user' (FK to Profile) and 'resumes' (M2M to Resume)
# Assuming CertificationForm is like ExperienceForm

@login_required(login_url='login')
def addCertification(request, pk):
    # Adds a new certification, potentially associating it with one or more resumes.
    # 'pk' is the ID of the primary resume this certification is being added in context of.
    current_user_profile = request.user.profile
    resume_context = get_object_or_404(Resume, id=pk, user=current_user_profile)

    if request.method == "POST":
        form = CertificationForm(request.POST, user=current_user_profile)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.user = current_user_profile
            certification.save()

            selected_resume_objects = form.cleaned_data.get('resumes', [])
            if selected_resume_objects:
                certification.resumes.set(selected_resume_objects)
            elif resume_context:
                certification.resumes.add(resume_context)
            # Optional: certification.resumes.add(resume_context)

            return redirect('edit-resume', pk=resume_context.id)
    else: # GET request
        form = CertificationForm(user=current_user_profile)
        
    return render(request, 'resume/certification_form.html', {'certification_form': form, 'resume': resume_context})

@login_required(login_url='login')
def editCertification(request, pk):
    # Edits an existing certification. 'pk' is the ID of the Certification object.
    current_user_profile = request.user.profile
    certification_instance = get_object_or_404(Certification, id=pk, user=current_user_profile)

    if request.method == "POST":
        form = CertificationForm(request.POST, instance=certification_instance, user=current_user_profile)
        if form.is_valid():
            form.save()
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url: # TODO: Validate next_url
                return redirect(next_url)
            else:
                primary_resume = certification_instance.resumes.first()
                if primary_resume:
                    return redirect('edit-resume', pk=primary_resume.id)
                return redirect(reverse('resume-dashboard'))
    else: # GET request
        form = CertificationForm(instance=certification_instance, user=current_user_profile)
        
    context = {
        'certification_form': form,
        'certification': certification_instance
    }
    return render(request, 'resume/edit_certification.html', context)

@login_required(login_url='login')
def deleteCertification(request, pk):
    # Handles deletion of a certification.
    current_user_profile = request.user.profile
    certification = get_object_or_404(Certification, id=pk, user=current_user_profile)
    
    primary_resume = certification.resumes.first()
    default_redirect_url = reverse('resume-dashboard')
    if primary_resume:
        default_redirect_url = reverse('edit-resume', kwargs={'pk': primary_resume.id})
    next_url = request.GET.get('next', default_redirect_url)

    if request.method == "POST":
        certification.delete()
        return redirect(next_url)
        
    return render(request, 'delete_template.html', {'object': certification, 'next_url': next_url})

# === Update Order Views ===
# These views update item positions. They should also ensure users can only reorder their own items.
# The current implementation Experience.objects.get(id=item['id']) is insecure.

@csrf_protect
@login_required(login_url='login') # Add login_required
def update_experience_order(request):
    # Updates the display order of experiences.
    if request.method == "POST":
        current_user_profile = request.user.profile # Get current user's profile
        try:
            data = json.loads(request.body)
            for item_data in data['order']: # Renamed 'item' to 'item_data' to avoid conflict
                # Securely fetch the experience, ensuring it belongs to the current user
                experience = get_object_or_404(Experience, id=item_data['id'], user=current_user_profile)
                experience.position = item_data['position']
                experience.save()
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e: # Catch other potential errors
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405) # Method Not Allowed

@csrf_protect
@login_required(login_url='login')
def update_education_order(request):
    # Updates the display order of education items.
    if request.method == "POST":
        current_user_profile = request.user.profile
        try:
            data = json.loads(request.body)
            for item_data in data['order']:
                education = get_object_or_404(Education, id=item_data['id'], user=current_user_profile)
                education.position = item_data['position']
                education.save()
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_protect
@login_required(login_url='login')
def update_skill_order(request):
    # Updates the display order of skills.
    if request.method == "POST":
        current_user_profile = request.user.profile
        try:
            data = json.loads(request.body)
            for item_data in data['order']:
                skill = get_object_or_404(Skill, id=item_data['id'], user=current_user_profile)
                skill.position = item_data['position']
                skill.save()
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_protect
@login_required(login_url='login')
def update_project_order(request):
    # Updates the display order of projects.
    if request.method == "POST":
        current_user_profile = request.user.profile
        try:
            data = json.loads(request.body)
            for item_data in data['order']:
                project = get_object_or_404(Project, id=item_data['id'], user=current_user_profile)
                project.position = item_data['position']
                project.save()
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_protect
@login_required(login_url='login')
def update_certification_order(request):
    # Updates the display order of certifications.
    if request.method == "POST":
        current_user_profile = request.user.profile
        try:
            data = json.loads(request.body)
            for item_data in data['order']:
                certification = get_object_or_404(Certification, id=item_data['id'], user=current_user_profile)
                certification.position = item_data['position']
                certification.save()
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)