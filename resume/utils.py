from django.shortcuts import get_object_or_404
from .models import Resume

def save_section(form, user_profile, resume_pk=None):
    """
    Helper to save any “section” (Experience, Education, Skill, etc.)
    and wire up its many-to-many link to Resume(s).
    
    Args:
      form: bound ModelForm for one section model
      user_profile: request.user.profile (for ownership)
      resume_pk: optional ID of the “current” Resume (auto-link context)
    """
    #  Create or update the instance, but don’t commit M2M yet
    obj = form.save(commit=False)

    #  Enforce ownership: assign the current user’s profile
    obj.user = user_profile
    obj.save() 

    # Handle the form’s 'resumes' many-to-many field, if present
    selected = form.cleaned_data.get('resumes') or []
    if selected:
        obj.resumes.set(selected)

    # If called from within a specific resume (resume_pk) AND
    #    the user didn’t explicitly pick any, auto-link to that resume
    if resume_pk and not selected:
        resume = get_object_or_404(Resume, id=resume_pk, user=user_profile)
        obj.resumes.add(resume)

    # Return the saved object in case the caller needs it
    return obj
