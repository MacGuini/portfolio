from django.db.models.deletion import CASCADE
from django.db import models
from accounts.models import Profile


class Resume(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE, related_name='resumes', blank=False, null=False)
    title = models.CharField(max_length=100)
    
    summary = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} - {self.user.username}" 

# Note: Each model below has a ManyToManyField to Resume to allow multiple resumes to share the same entries.
# Note: All fields are optional to facilitate formsets, except the ForeignKey to Profile.

class Experience(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE, related_name='experiences', blank=False, null=False)
    resumes = models.ManyToManyField(Resume, related_name='experiences', blank=True)

    job_title = models.CharField(max_length=100, blank=True, null=True)  # Allow blank and null for formset
    company_name = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0) # Position in the list

    class Meta:
        ordering = ['position', '-is_current', '-start_date']

    def __str__(self):
        return f"{self.job_title} - {self.company_name}" or "Unnamed Experience"


class Education(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE, related_name='educations', blank=False, null=False)
    resumes = models.ManyToManyField(Resume, related_name="educations", blank=True)

    institution_name = models.CharField(max_length=100, blank=True, null=True)
    degree = models.CharField(max_length=100, blank=True, null=True)
    field_of_study = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0) # Position in the list

    class Meta:
        ordering = ['position', '-end_date', '-start_date']

    def __str__(self):
        return f"{self.degree} at {self.institution_name}" or "Unnamed Education"


class Skill(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE, related_name='skills', blank=False, null=False)
    resumes = models.ManyToManyField(Resume, related_name="skills", blank=True)

    name = models.CharField(max_length=100, blank=True, null=True)
    proficiency = models.CharField(max_length=50, blank=True, null=True)
    position = models.PositiveIntegerField(default=0) # Position in the list

    class Meta:
        ordering = ['position', 'name']

    def __str__(self):
        return self.name or "Unnamed Skill"


class Project(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE, related_name='projects', blank=False, null=False)
    resumes = models.ManyToManyField(Resume, related_name='projects', blank=True)

    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0) # Position in the list

    class Meta:
        ordering = ['position', 'title']

    def __str__(self):
        return self.title or "Unnamed Project"


class Certification(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE, related_name='certifications', blank=False, null=False)
    resumes = models.ManyToManyField(Resume, related_name='certifications', blank=True)

    name = models.CharField(max_length=100, blank=True, null=True)
    issuer = models.CharField(max_length=100, blank=True, null=True)
    issue_date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=100, blank=True, null=True)
    credential_url = models.URLField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0) # Position in the list

    class Meta:
        ordering = ['position', 'name']

    def __str__(self):
        return self.name or "Unnamed Certification"

class Award(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE, related_name='awards', blank=False, null=False)
    resumes = models.ManyToManyField(Resume, related_name='awards', blank=True)

    title = models.CharField(max_length=100, blank=True, null=True)
    issuer = models.CharField(max_length=100, blank=True, null=True)
    date_received = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0) # Position in the list

    class Meta:
        ordering = ['position', 'title']

    def __str__(self):
        return self.title or "Unnamed Award"

class Language(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE, related_name='languages', blank=False, null=False)
    resumes = models.ManyToManyField(Resume, related_name='languages', blank=True)

    name = models.CharField(max_length=100, blank=True, null=True)
    proficiency = models.CharField(max_length=50, blank=True, null=True)
    position = models.PositiveIntegerField(default=0) # Position in the list

    class Meta:
        ordering = ['position', 'name']

    def __str__(self):
        return self.name or "Unnamed Language"

class Interest(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE, related_name='interests', blank=False, null=False)
    resumes = models.ManyToManyField(Resume, related_name='interests', blank=True)

    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0) # Position in the list

    class Meta:
        ordering = ['position', 'name']

    def __str__(self):
        return self.name or "Unnamed Interest"

class AdditionalInfo(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE, related_name='additional_infos', blank=False, null=False)
    resumes = models.ManyToManyField(Resume, related_name='additional_infos', blank=True)

    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position', 'title']

    def __str__(self):
        return self.title or "Unnamed Additional Info"