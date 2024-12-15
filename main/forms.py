from django import forms
from .models import Project, Issue, Comment, Resolution, Attachment
from django import forms
from .models import Project
from django.contrib.auth import get_user_model
User = get_user_model()


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'description', 'status', 'start_date', 'end_date', 'members']
        widgets = {
            'project_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'placeholder': 'Enter project name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'placeholder': 'Describe your project'
            }),
            'status': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'type': 'datetime-local',
                'step': 'any',
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'type': 'datetime-local'
            }),
            'members': forms.SelectMultiple(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
            })
        }


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            'title',
            'description',
            'priority',
            'status',
            'type',
            'project',
            'assignees',
            'labels',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'placeholder': 'Enter issue title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'placeholder': 'Describe the issue in detail',
                'rows': 4
            }),
            'priority': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
            }),
            'status': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
            }),
            'type': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
            }),
            'project': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
            }),
            'assignees': forms.SelectMultiple(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
            }),
            'labels': forms.SelectMultiple(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Add help texts
        self.fields['title'].help_text = 'Give your issue a clear, descriptive title'
        self.fields['description'].help_text = 'Provide detailed information about the issue'
        self.fields['type'].help_text = 'Select the type of issue'
        self.fields['priority'].help_text = 'Set the importance level of this issue'
        self.fields['assignees'].help_text = 'Select team members to work on this issue'
        self.fields['labels'].help_text = 'Add labels to categorize this issue'

        # Customize labels
        self.fields['assignees'].label = 'Assign To'
        
        # Set initial values for new issues
        if not self.instance.pk:
            self.fields['status'].initial = 'OPEN'
            self.fields['priority'].initial = 'MEDIUM'

        # Filter projects and assignees based on user permissions
        if user and not user.is_superuser:
            # Filter projects where user is a member
            self.fields['project'].queryset = self.fields['project'].queryset.filter(
                members=user
            )
            
            # If a project is already selected, filter assignees to project members
            if self.instance.project_id:
                self.fields['assignees'].queryset = self.instance.project.members.all()
            elif 'project' in self.data:
                try:
                    project_id = int(self.data.get('project'))
                    project = Project.objects.get(id=project_id)
                    self.fields['assignees'].queryset = project.members.all()
                except (ValueError, Project.DoesNotExist):
                    self.fields['assignees'].queryset = User.objects.none()
            else:
                self.fields['assignees'].queryset = User.objects.none()

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 3:
                raise forms.ValidationError("Title must be at least 3 characters long")
            if len(title) > 200:
                raise forms.ValidationError("Title must be less than 200 characters")
        return title

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        assignees = cleaned_data.get('assignees')

        # Validation rules
        if status == 'CLOSED' and not assignees:
            raise forms.ValidationError({
                'assignees': "An issue must have at least one assignee before it can be closed"
            })
            
        if status == 'IN_PROGRESS' and not assignees:
            raise forms.ValidationError({
                'assignees': "An issue must have at least one assignee when in progress"
            })

        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ResolutionForm(forms.ModelForm):
    class Meta:
        model = Resolution
        fields = ['description']

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file', 'description']
