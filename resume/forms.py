from django import forms
from .models import Resume, Experience, Education, Skill, Project, Certification

class BaseForm(forms.ModelForm):
    def update_fields(self, fields):
        for field_name, attrs in fields.items():
            self.fields[field_name].widget.attrs.update(attrs)
            self.fields[field_name].label = ''

class ResumeForm(BaseForm):
    class Meta:
        model = Resume
        fields = ['title', 'summary']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_fields({
            'title': {
                'id': 'title',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Give your resume a title'
            },
            'summary': {
                'id': 'summary',
                'class': 'block w-full text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Summarize resume'
            }
        })


class ExperienceForm(BaseForm):
    class Meta:
        model = Experience
        fields = '__all__'
        exclude = ['user', 'position']

    # Defines the resumes field as a ModelMultipleChoiceField with a CheckboxSelectMultiple widget
    resumes = forms.ModelMultipleChoiceField(
        queryset=Resume.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # get user passed from the view
        super().__init__(*args, **kwargs)
        # Check if a user is passed to the form
        if user:
            # Filter resumes by the user passed to the form
            self.fields['resumes'].queryset = Resume.objects.filter(user=user)
        else:
            self.fields['resumes'].queryset = Resume.objects.none()

        self.update_fields({
            'job_title': {
                'id': 'job_title',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Job Title'
            },
            'company_name': {
                'id': 'company_name',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Company Name'
            },
            'start_date': {
                'id': 'start_date',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Start Date',
                'type': 'date'
            },
            'end_date': {
                'id': 'end_date',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'End Date',
                'type': 'date'
            },
            'is_current': {
                'id': 'is_current',
                'class': 'form-check-input my-2 text-gray-800s ',
                'type': 'checkbox'
            },
            'description': {
                'id': 'description',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Description'
            }
        })

        self.fields['is_current'].widget = forms.CheckboxInput(attrs={
            'id': 'is_current',
            'class': 'form-check-input'
        })

        self.fields['is_current'].label = 'Currently Employed?'
        self.fields['resumes'].label = 'Resumes to include this experience in:'


class EducationForm(BaseForm):
    class Meta:
        model = Education
        fields = '__all__'
        exclude = ['user', 'position']

    # Defines the resumes field as a ModelMultipleChoiceField with a CheckboxSelectMultiple widget
    resumes = forms.ModelMultipleChoiceField(
        queryset=Resume.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # get user passed from the view
        super().__init__(*args, **kwargs)
        # Check if a user is passed to the form
        if user:
            # Filter resumes by the user passed to the form
            self.fields['resumes'].queryset = Resume.objects.filter(user=user)
        else:
            self.fields['resumes'].queryset = Resume.objects.none()

        self.update_fields({
            'institution_name': {
                'id': 'institution_name',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Institution Name'
            },
            'degree': {
                'id': 'degree',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Degree'
            },
            'field_of_study': {
                'id': 'field_of_study',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Field of Study'
            },
            'start_date': {
                'id': 'start_date',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Start Date',
                'type': 'date'

            },
            'end_date': {
                'id': 'end_date',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'End Date',
                'type': 'date'
            },
            'description': {
                'id': 'description',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Description'
            }
        })

class SkillForm(BaseForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['user', 'position']

    # Defines the resumes field as a ModelMultipleChoiceField with a CheckboxSelectMultiple widget
    resumes = forms.ModelMultipleChoiceField(
        queryset=Resume.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # get user passed from the view
        super().__init__(*args, **kwargs)

        # Check if a user is passed to the form
        if user:
            # Filter resumes by the user passed to the form
            self.fields['resumes'].queryset = Resume.objects.filter(user=user)
        else:
            self.fields['resumes'].queryset = Resume.objects.none()

        self.update_fields({
            'name': {
                'id': 'name',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Skill Name'
            },
            'proficiency': {
                'id': 'proficiency',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Proficiency'
            }
        })

class ProjectForm(BaseForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['user', 'position']

    # Defines the resumes field as a ModelMultipleChoiceField with a CheckboxSelectMultiple widget
    resumes = forms.ModelMultipleChoiceField(
        queryset=Resume.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # get user passed from the view
        super().__init__(*args, **kwargs)
        # Check if a user is passed to the form
        if user:
            # Filter resumes by the user passed to the form
            self.fields['resumes'].queryset = Resume.objects.filter(user=user)
        else:
            self.fields['resumes'].queryset = Resume.objects.none()

        self.update_fields({
            'title': {
                'id': 'title',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Project Title'
            },
            'description': {
                'id': 'description',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Description'
            },
            'link': {
                'id': 'link',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'https://example.com'
            }
        })

class CertificationForm(BaseForm):
    class Meta:
        model = Certification
        fields = '__all__'
        exclude = ['user', 'position']

    # Defines the resumes field as a ModelMultipleChoiceField with a CheckboxSelectMultiple widget
    resumes = forms.ModelMultipleChoiceField(
        queryset=Resume.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # get user passed from the view
        super(CertificationForm, self).__init__(*args, **kwargs)
        # Check if a user is passed to the form
        if user:
            # Filter resumes by the user passed to the form
            self.fields['resumes'].queryset = Resume.objects.filter(user=user)
        else:
            self.fields['resumes'].queryset = Resume.objects.none()
        self.update_fields({
            'name': {
                'id': 'name',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Certification Name'
            },
            'issuer': {
                'id': 'issuer',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Issuer'
            },
            'issue_date': {
                'id': 'issue_date',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Issue Date',
                'type': 'date'
            },
            'expiration_date': {
                'id': 'expiration_date',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Expiration Date',
                'type': 'date'
            },
            'credential_id': {
                'id': 'credential_id',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Credential ID'
            },
            'credential_url': {
                'id': 'credential_url',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'https://example.com'
            }
        })