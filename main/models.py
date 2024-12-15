from django.db import models
from django.conf import settings
from django.utils import timezone

class Project(models.Model):
    """Project model for managing software projects"""
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('ON_HOLD', 'On Hold'),
        ('CANCELLED', 'Cancelled'),
    ]

    project_name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name

class Label(models.Model):
    """Label model for categorizing issues"""
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
    color = models.CharField(max_length=7, default="#000000")  # Hex color code

    def __str__(self):
        return self.name

class Issue(models.Model):
    """Issue model for tracking problems, tasks, and feature requests"""
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]
    
    TYPE_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature Request'),
        ('TASK', 'Task'),
        ('IMPROVEMENT', 'Improvement'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Relationships
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_issues')
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_issues')
    labels = models.ManyToManyField(Label, related_name='issues', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

class Comment(models.Model):
    """Comment model for issues"""
    content = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.issue.title}"

class Resolution(models.Model):
    """Resolution model for resolved issues"""
    description = models.TextField()
    issue = models.OneToOneField(Issue, on_delete=models.CASCADE, related_name='resolution')
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resolutions')
    resolved_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resolution for {self.issue.title}"

class Attachment(models.Model):
    """Attachment model for issue attachments"""
    file = models.FileField(upload_to='issue_attachments/')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='attachments')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attachments')
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Attachment for {self.issue.title}"
