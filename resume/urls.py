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
]