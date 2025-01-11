from django.urls import path
from . import views

urlpatterns = [
    path('list-resumes/', views.listResumes, name='list-resumes'),
    path('create-resume/', views.createResume, name='create-resume'),
    path('edit-resume/<int:pk>/', views.editResume, name='edit-resume'),
    path('delete-resume/<int:pk>/', views.deleteResume, name='delete-resume'),
    path('delete-experience/<int:pk>/', views.deleteExperience, name='delete-experience'),
    path('delete-education/<int:pk>/', views.deleteEducation, name='delete-education'),
    path('delete-skill/<int:pk>/', views.deleteSkill, name='delete-skill'),
    path('delete-project/<int:pk>/', views.deleteProject, name='delete-project'),
    path('delete-certification/<int:pk>/', views.deleteCertification, name='delete-certification'),
    path('add-experience/<int:pk>/', views.addExperience, name='add-experience'),
    path('add-education/<int:pk>/', views.addEducation, name='add-education'),
    path('add-skill/<int:pk>/', views.addSkill, name='add-skill'),
    path('add-project/<int:pk>/', views.addProject, name='add-project'),
    path('add-certification/<int:pk>/', views.addCertification, name='add-certification'),
    path('update-experience-position/', views.update_experience_order, name='update-experience-position'),
    path('update-education-position/', views.update_education_order, name='update-education-position'),
    path('update-skill-position/', views.update_skill_order, name='update-skill-position'),
    path('update-project-position/', views.update_project_order, name='update-project-position'),
    path('update-certification-position/', views.update_certification_order, name='update-certification-position'),
    path('edit-experience/<int:pk>/', views.editExperience, name='edit-experience'),
    path('edit-education/<int:pk>/', views.editEducation, name='edit-education'),
    path('edit-skill/<int:pk>/', views.editSkill, name='edit-skill'),
    path('edit-project/<int:pk>/', views.editProject, name='edit-project'),
    path('edit-certification/<int:pk>/', views.editCertification, name='edit-certification'),
]