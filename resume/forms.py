from django import forms
from .models import Resume, Experience, Education, Skill, Project, Certification, Award, Language, Interest, AdditionalInfo

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
                'type': 'text'
            },
            'end_date': {
                'id': 'end_date',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'End Date',
                'type': 'text'
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
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Institution Name'
            },
            'degree': {
                'id': 'degree',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Degree'
            },
            'field_of_study': {
                'id': 'field_of_study',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Field of Study'
            },
            'start_date': {
                'id': 'start_date',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Start Date',
                'type': 'text'

            },
            'end_date': {
                'id': 'end_date',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'End Date',
                'type': 'text'
            },
            'description': {
                'id': 'description',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
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
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Skill Name'
            },
            'proficiency': {
                'id': 'proficiency',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
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
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Project Title'
            },
            'description': {
                'id': 'description',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Description'
            },
            'link': {
                'id': 'link',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
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
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Certification Name'
            },
            'issuer': {
                'id': 'issuer',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Issuer'
            },
            'issue_date': {
                'id': 'issue_date',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Issue Date',
                'type': 'text'
            },
            'expiration_date': {
                'id': 'expiration_date',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Expiration Date',
                'type': 'text'
            },
            'credential_id': {
                'id': 'credential_id',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Credential ID'
            },
            'credential_url': {
                'id': 'credential_url',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'https://example.com'
            }
        })

class AwardForm(BaseForm):
    class Meta:
        model = Award
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
        super(AwardForm, self).__init__(*args, **kwargs)
        # Check if a user is passed to the form
        if user:
            # Filter resumes by the user passed to the form
            self.fields['resumes'].queryset = Resume.objects.filter(user=user)
        else:
            self.fields['resumes'].queryset = Resume.objects.none()
        self.update_fields({
            'title': {
                'id': 'title',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Award Title'
            },
            'issuer': {
                'id': 'issuer',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Issuer'
            },
            'date_received': {
                'id': 'date_received',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Date Received',
                'type': 'text'
            },
            'description': {
                'id': 'description',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Description'
            }
        })

class LanguageForm(BaseForm):
    class Meta:
        model = Language
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
        super(LanguageForm, self).__init__(*args, **kwargs)
        # Check if a user is passed to the form
        if user:
            # Filter resumes by the user passed to the form
            self.fields['resumes'].queryset = Resume.objects.filter(user=user)
        else:
            self.fields['resumes'].queryset = Resume.objects.none()
        self.update_fields({
            'name': {
                'id': 'name',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Language Name'
            },
            'proficiency': {
                'id': 'proficiency',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Proficiency'
            }
        })

class InterestForm(BaseForm):
    class Meta:
        model = Interest
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
        super(InterestForm, self).__init__(*args, **kwargs)
        # Check if a user is passed to the form
        if user:
            # Filter resumes by the user passed to the form
            self.fields['resumes'].queryset = Resume.objects.filter(user=user)
        else:
            self.fields['resumes'].queryset = Resume.objects.none()
        self.update_fields({
            'name': {
                'id': 'name',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Interest Name'
            },
            'description': {
                'id': 'description',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Description'
            }
        })

class AdditionalInfoForm(BaseForm):
    class Meta:
        model = AdditionalInfo
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
        super(AdditionalInfoForm, self).__init__(*args, **kwargs)
        # Check if a user is passed to the form
        if user:
            # Filter resumes by the user passed to the form
            self.fields['resumes'].queryset = Resume.objects.filter(user=user)
        else:
            self.fields['resumes'].queryset = Resume.objects.none()
        self.update_fields({
            'title': {
                'id': 'title',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'Title'
            },
            'content': {
                'id': 'content',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-2',
                'placeholder': 'What else would you like to share?'
            }
        })