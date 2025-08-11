from django.urls import path
from . import views
from .views import section_form

urlpatterns = [
    # Resume URLs
    path('dashboard/', views.resumeDashboard, name='resume-dashboard'),
    path('create-resume/', views.createResume, name='create-resume'),
    path('edit-resume/<int:pk>/', views.editResume, name='edit-resume'),
    path('delete-resume/<int:pk>/', views.deleteResume, name='delete-resume'),
    path('view-resume/<str:username>/<int:pk>/', views.viewResume, name='view-resume'),
    path('view-profile-resume/<str:username>/', views.viewProfileResume, name='view-profile-resume'),

    # Experience URLs
    path('delete-experience/<int:pk>/', views.deleteExperience, name='delete-experience'),
    # path('update-experience-position/', views.update_experience_order, name='update-experience-position'),

    # Education URLs
    path('delete-education/<int:pk>/', views.deleteEducation, name='delete-education'),
    # path('update-education-position/', views.update_education_order, name='update-education-position'),

    # Skill URLs
    path('delete-skill/<int:pk>/', views.deleteSkill, name='delete-skill'),
    # path('update-skill-position/', views.update_skill_order, name='update-skill-position'),

    # Project URLs
    path('delete-project/<int:pk>/', views.deleteProject, name='delete-project'),
    # path('update-project-position/', views.update_project_order, name='update-project-position'),

    # Certification URLs
    path('delete-certification/<int:pk>/', views.deleteCertification, name='delete-certification'),
    # path('update-certification-position/', views.update_certification_order, name='update-certification-position'),

    # Award URLs
    path('delete-award/<int:pk>/', views.deleteAward, name='delete-award'),
    # path('update-award-position/', views.update_award_order, name='update-award-position'),

    # Language URLs
    path('delete-language/<int:pk>/', views.deleteLanguage, name='delete-language'),
    # path('update-language-position/', views.update_language_order, name='update-language-position'),

    # Interest URLs
    path('delete-interest/<int:pk>/', views.deleteInterest, name='delete-interest'),
    # path('update-interest-position/', views.update_interest_order, name='update-interest-position'),

    # Additional Info URLs
    path('delete-additional-info/<int:pk>/', views.deleteAdditionalInfo, name='delete-additional-info'),
    # path('update-additional-info-position/', views.update_additional_info_order, name='update-additional-info-position'),

    # Generic add/edit/delete URLs:
    path('add/<str:section>/', section_form, {'action':'add'},    name='add-section'),
    path('<int:resume_pk>/add/<str:section>/', section_form, {'action':'add'},    name='add-section-resume'),
    path('edit/<str:section>/<int:pk>/', section_form, {'action':'edit'},   name='edit-section'),
    path('delete/<str:section>/<int:pk>/', section_form, {'action':'delete'}, name='delete-section'),

    # Print URLs
    path('print/<str:username>/<int:pk>/', views.printResume, name='print-resume'),
]