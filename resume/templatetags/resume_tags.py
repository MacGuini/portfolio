from django import template
from django.urls import reverse

register = template.Library()

@register.filter
def dict_get(d, key):
    """Retrieve d[key] safely in templates."""
    return d.get(key)

@register.filter
def get_add_url(section, resume_pk=None):
    """
    Returns the correct 'add' URL for a section.
    - If a resume_pk is provided, it generates a URL to add the section
      to that specific resume.
    - If resume_pk is None, it generates the generic 'add' URL for the dashboard.
    
    Usage in template:
    {% url 'section_name'|get_add_url:resume.id %}  <- For specific resume
    {% url 'section_name'|get_add_url %}            <- For dashboard
    """
    if resume_pk:
        return reverse('add-section-resume', kwargs={'resume_pk': resume_pk, 'section': section})
    else:
        return reverse('add-section', kwargs={'section': section})

# Keep your other filters like get_edit_url if you have them
@register.filter
def get_edit_url(pk, section):
    """
    Returns the URL for the edit view for a given section.
    Usage: {{ object.id|get_edit_url:"section_name" }}
    """
    return reverse('edit-section', kwargs={'pk': pk, 'section': section})