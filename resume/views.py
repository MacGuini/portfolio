import json
from django.apps import apps
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect # Keep for your AJAX views
from django.urls import reverse # For safer redirects
from accounts.models import Profile
from .utils import save_section
from .models import Resume, Experience, Education, Skill, Project, Certification, Award, Language, Interest, AdditionalInfo
from .forms import (
    ResumeForm, EducationForm, ExperienceForm, SkillForm, ProjectForm, CertificationForm, AwardForm, LanguageForm, InterestForm, AdditionalInfoForm
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
    'award': {
        'model':   'resume.Award',
        'form':     AwardForm,
        'template': 'resume/section_form.html',
    },
    'language': {
        'model':   'resume.Language',
        'form':     LanguageForm,
        'template': 'resume/section_form.html',
    },
    'interest': {
        'model':   'resume.Interest',
        'form':     InterestForm,
        'template': 'resume/section_form.html',
    },
    'additionalinfo': {
        'model':   'resume.AdditionalInfo',
        'form':     AdditionalInfoForm,
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
                print("*********\nInside section_form() form.is_valid() block\nForm Data:", form.cleaned_data, "Form Errors:", form.errors, "Instance:", instance)

                # Save the section, passing the resume_pk if provided
                # This allows the form to handle both adding to a specific resume or the dashboard
                # If resume_pk is None, it will save to the dashboard context.
                # If resume_pk is provided, it will save to that specific resume.
                # The save_section utility function handles the logic of saving the section.
                checked_pk = request.POST.get("resume_pk") or resume_pk
                save_section(form, user_prof, checked_pk)
                target = (reverse('edit-resume', args=[checked_pk])
                          if checked_pk else reverse('resume-dashboard'))
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

def viewResume(request, pk, username):
    # This view is for viewing a specific resume by its ID and the username of the profile that owns it.
   
    profile = get_object_or_404(Profile, username=username)
    resume = get_object_or_404(Resume, id=pk, user=profile)
    experiences = resume.experiences.all()
    educations = resume.educations.all()
    skills = resume.skills.all()
    projects = resume.projects.all()
    certifications = resume.certifications.all()
    awards = resume.awards.all()
    languages = resume.languages.all()
    additional_infos = resume.additionalinfo_set.all()
    context = {
        'resume': resume,
        'username': username,
        'creatorProfile': profile,
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
        'awards': awards,
        'languages': languages,
        'additional_infos': additional_infos,
    }
    return render(request, 'resume/view_resume.html', context)

def viewProfileResume(request, username):
    # This view is for viewing a resume by the username of the profile that owns it.
    # All of this profile's resume data will be displayed. Not just one specific resume.
    # This is meant as a digital resume for potential employers. There will be no CRUD functionality here.
    profile = get_object_or_404(Profile, username=username)
    experiences = Experience.objects.filter(user=profile)
    educations = Education.objects.filter(user=profile)
    skills = Skill.objects.filter(user=profile)
    projects = Project.objects.filter(user=profile)
    certifications = Certification.objects.filter(user=profile)
    awards = Award.objects.filter(user=profile)
    languages = Language.objects.filter(user=profile)
    additional_infos = AdditionalInfo.objects.filter(user=profile)

    resumes = Resume.objects.filter(user=profile)
    context = {
        'creatorProfile': profile,
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
        'awards': awards,
        'languages': languages,
        'additional_infos': additional_infos,
        'resumes':resumes,
    }
    return render(request, 'resume/view_profile_resume.html', context)


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
    awards = Award.objects.filter(user=current_user_profile)
    languages = Language.objects.filter(user=current_user_profile)
    additional_infos = AdditionalInfo.objects.filter(user=current_user_profile)


    experience_add_form = ExperienceForm(user=current_user_profile)
    education_add_form = EducationForm(user=current_user_profile)
    skill_add_form = SkillForm(user=current_user_profile)
    project_add_form = ProjectForm(user=current_user_profile)
    certification_add_form = CertificationForm(user=current_user_profile)
    award_add_form = AwardForm(user=current_user_profile)
    language_add_form = LanguageForm(user=current_user_profile)
    additional_info_add_form = AdditionalInfoForm(user=current_user_profile)


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
    award_edit_forms = {
        award.id: AwardForm(instance=award, user=current_user_profile)
        for award in awards
    }
    language_edit_forms = {
        lang.id: LanguageForm(instance=lang, user=current_user_profile)
        for lang in languages
    }
    additional_info_edit_forms = {
        info.id: AdditionalInfoForm(instance=info, user=current_user_profile)
        for info in additional_infos
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
        'awards': awards,
        'languages': languages,
        'additional_infos': additional_infos,
        'experience_add_form': experience_add_form,
        'education_add_form': education_add_form,
        'skill_add_form': skill_add_form,
        'project_add_form': project_add_form,
        'certification_add_form': certification_add_form,
        'award_add_form': award_add_form,
        'language_add_form': language_add_form,
        'additional_info_add_form': additional_info_add_form,
        'experience_edit_forms': experience_edit_forms,
        'education_edit_forms': education_edit_forms,
        'skill_edit_forms': skill_edit_forms,
        'project_edit_forms': project_edit_forms,
        'certification_edit_forms': certification_edit_forms,
        'award_edit_forms': award_edit_forms,
        'language_edit_forms': language_edit_forms,
        'additional_info_edit_forms': additional_info_edit_forms,
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
        # Debugging variables
        print("********\nInside editResume() if request.method == 'POST' block\nResume ID:", resume.id, "User Profile ID:", current_user_profile.id, "Request Data:", request.POST, "Request Method:", request.method, "User Profile:", current_user_profile, "pk:", pk)
        # This POST request is for updating the main Resume object itself
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            print("*********\nInside form.is_valid() block\nForm Data:", form.cleaned_data, "Form Errors:", form.errors, "Instance:", resume)
            form.save()
            return redirect('edit-resume', pk=resume.id) # Redirect back to the same edit page
    else:
        form = ResumeForm(instance=resume) # For GET request, pre-fill with resume instance

    # Initialize forms for related sections, passing the user profile for context
    # This allows these forms to correctly list the user's other resumes if they have such a field.
    experience_add_form = ExperienceForm(user=current_user_profile)
    education_add_form = EducationForm(user=current_user_profile)
    skill_add_form = SkillForm(user=current_user_profile)
    project_add_form = ProjectForm(user=current_user_profile)
    certification_add_form = CertificationForm(user=current_user_profile)
    award_add_form = AwardForm(user=current_user_profile)
    language_add_form = LanguageForm(user=current_user_profile)
    additional_info_add_form = AdditionalInfoForm(user=current_user_profile)
    
    # Fetch related items for display
    experiences = resume.experiences.all()
    educations = resume.educations.all()
    skills = resume.skills.all()
    projects = resume.projects.all()
    certifications = resume.certifications.all()
    awards = resume.awards.all()
    languages = resume.languages.all()
    additional_infos = resume.additionalinfo_set.all()

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
    award_edit_forms = {
        award.id: AwardForm(instance=award, user=current_user_profile)
        for award in awards
    }
    language_edit_forms = {
        lang.id: LanguageForm(instance=lang, user=current_user_profile)
        for lang in languages
    }
    additional_info_edit_forms = {
        info.id: AdditionalInfoForm(instance=info, user=current_user_profile)
        for info in additional_infos
    }
    
    context = {
        'form': form, # Form for editing the Resume model
        'resume': resume,
        'resume_id': pk, # Same as resume.id, for convenience in template
        'experience_add_form': experience_add_form,
        'education_add_form': education_add_form,
        'skill_add_form': skill_add_form,
        'project_add_form': project_add_form,
        'certification_add_form': certification_add_form,
        'award_add_form': award_add_form,
        'language_add_form': language_add_form,
        'additional_info_add_form': additional_info_add_form,
        'experience_edit_forms': experience_edit_forms,
        'education_edit_forms': education_edit_forms,
        'skill_edit_forms': skill_edit_forms,
        'project_edit_forms': project_edit_forms,
        'certification_edit_forms': certification_edit_forms,
        'award_edit_forms': award_edit_forms,
        'language_edit_forms': language_edit_forms,
        'additional_info_edit_forms': additional_info_edit_forms,
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
        'awards': awards,
        'languages': languages,
        'additional_infos': additional_infos,
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

# === Education Views ===

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

# === Print Functions ===

# Public view to print a resume as long as the link is valid to allow sharing with potential employers.
# No login is required to view the print version. Future security measures will be added later on to ensure that only those with the link can view it such as a token or password.
def printResume(request, pk, username):
    # Handles printing of a resume.
    profile = get_object_or_404(Profile, username=username)
    resume = get_object_or_404(Resume, id=pk, user=profile)
    if not resume:
        raise Http404("Resume not found")
    else:

        # Fetch related items for display
        experiences = resume.experiences.all()
        educations = resume.educations.all()
        skills = resume.skills.all()
        projects = resume.projects.all()
        certifications = resume.certifications.all()
   
        context = {
            'resume': resume,
            'experiences': experiences,
            'educations': educations,
            'skills': skills,
            'projects': projects,
            'certifications': certifications,
            'creatorProfile': profile,  # Pass the profile for context
        }
    return render(request, 'resume/print_resume.html', context)
# This view renders a printable version of the resume, including all related sections.