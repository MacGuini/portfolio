from django.contrib import admin
from .models import Resume, Experience, Education, Skill, Project, Certification, Award, Language, Interest, AdditionalInfo

# Register your models here.

admin.site.register(Resume)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Certification)
admin.site.register(Award)
admin.site.register(Language)
admin.site.register(Interest)
admin.site.register(AdditionalInfo)