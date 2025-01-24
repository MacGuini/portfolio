from django.urls import path
from . import views

urlpatterns = [
    # Resume URLs
    path('list-resumes/', views.listResumes, name='list-resumes'),
    path('create-resume/', views.createResume, name='create-resume'),
    path('edit-resume/<int:pk>/', views.editResume, name='edit-resume'),
    path('delete-resume/<int:pk>/', views.deleteResume, name='delete-resume'),

    # Experience URLs
    path('list-experiences/<int:pk>/', views.listExperiences, name='list-experiences'),
    path('add-experience/<int:pk>/', views.addExperience, name='add-experience'),
    path('edit-experience/<int:pk>/', views.editExperience, name='edit-experience'),
    path('delete-experience/<int:pk>/', views.deleteExperience, name='delete-experience'),
    path('update-experience-position/', views.update_experience_order, name='update-experience-position'),

    # Education URLs
    path('add-education/<int:pk>/', views.addEducation, name='add-education'),
    path('edit-education/<int:pk>/', views.editEducation, name='edit-education'),
    path('delete-education/<int:pk>/', views.deleteEducation, name='delete-education'),
    path('update-education-position/', views.update_education_order, name='update-education-position'),

    # Skill URLs
    path('add-skill/<int:pk>/', views.addSkill, name='add-skill'),
    path('edit-skill/<int:pk>/', views.editSkill, name='edit-skill'),
    path('delete-skill/<int:pk>/', views.deleteSkill, name='delete-skill'),
    path('update-skill-position/', views.update_skill_order, name='update-skill-position'),

    # Project URLs
    path('add-project/<int:pk>/', views.addProject, name='add-project'),
    path('edit-project/<int:pk>/', views.editProject, name='edit-project'),
    path('delete-project/<int:pk>/', views.deleteProject, name='delete-project'),
    path('update-project-position/', views.update_project_order, name='update-project-position'),

    # Certification URLs
    path('add-certification/<int:pk>/', views.addCertification, name='add-certification'),
    path('edit-certification/<int:pk>/', views.editCertification, name='edit-certification'),
    path('delete-certification/<int:pk>/', views.deleteCertification, name='delete-certification'),
    path('update-certification-position/', views.update_certification_order, name='update-certification-position'),
]