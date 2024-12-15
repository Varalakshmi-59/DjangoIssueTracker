from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Project, Issue, Comment, Resolution, Attachment
from .forms import (
    ProjectForm, 
    IssueForm, 
    CommentForm, 
    ResolutionForm, 
    AttachmentForm
)

@login_required(login_url="users:login")
def home(request):
    print(f"\nVisiting home page\n")
    user_projects = Project.objects.filter(members=request.user).order_by('-updated_at')[:5]
    assigned_issues = Issue.objects.filter(assignees=request.user).order_by('-updated_at')[:5]
    
    stats = {
        'total_projects': user_projects.count(),
        'open_issues': Issue.objects.filter(assignees=request.user, status='OPEN').count(),
        'in_progress': Issue.objects.filter(assignees=request.user, status='IN_PROGRESS').count(),
        'resolved': Issue.objects.filter(assignees=request.user, status='RESOLVED').count(),
    }
    
    context = {
        'user_projects': user_projects,
        'assigned_issues': assigned_issues,
        'stats': stats,
    }
    return render(request, 'main/home.html', context)

# Project Views
@login_required(login_url="users:login")
def project_list(request):
    """Display list of all projects with filtering"""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    projects = Project.objects.filter(members=request.user)
    
    if search_query:
        projects = projects.filter(
            Q(project_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    projects = projects.annotate(
        open_issues=Count('issues', filter=Q(issues__status='OPEN')),
        total_issues=Count('issues')
    ).order_by('-updated_at')
    
    paginator = Paginator(projects, 10)
    page = request.GET.get('page', 1)
    projects = paginator.get_page(page)
    
    context = {
        'projects': projects,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': Project.STATUS_CHOICES,
    }
    return render(request, 'main/project_list.html', context)

@login_required(login_url="users:login")
def project_detail(request, pk):
    """Display project details and associated issues"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.user not in project.members.all():
        messages.error(request, "You don't have access to this project.")
        return redirect('main:project-list')
    
    issues = project.issues.all()
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    type_filter = request.GET.get('type')
    
    if status_filter:
        issues = issues.filter(status=status_filter)
    if priority_filter:
        issues = issues.filter(priority=priority_filter)
    if type_filter:
        issues = issues.filter(type=type_filter)
    
    context = {
        'project': project,
        'issues': issues,
        'status_choices': Issue.STATUS_CHOICES,
        'priority_choices': Issue.PRIORITY_CHOICES,
        'type_choices': Issue.TYPE_CHOICES,
    }
    return render(request, 'main/project_detail.html', context)

@login_required(login_url="users:login")
def project_create(request):
    """Create a new project"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            project.members.add(request.user)
            form.save_m2m()
            messages.success(request, 'Project created successfully.')
            return redirect('main:project-detail', pk=project.pk)
    else:
        form = ProjectForm()
    
    return render(request, 'main/project_form.html', {
        'form': form,
        'title': 'Create Project'
    })

@login_required(login_url="users:login")
def project_update(request, pk):
    """Update existing project"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.user not in project.members.all():
        messages.error(request, "You don't have permission to edit this project.")
        return redirect('main:project-list')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('main:project-detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'main/project_form.html', {
        'form': form,
        'title': 'Update Project',
        'project': project
    })
    
@login_required(login_url="users:login")
def project_delete(request, pk):
    """Update existing project"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.user not in project.members.all():
        messages.error(request, "You don't have permission to edit this project.")
        return redirect('main:project-list')
    
    project_title= project.project_name
    project.delete()
    messages.success(request, f'Project {project_title} deleted successfully.')
    
    return redirect('main:project-list')

# Issue Views
@login_required(login_url="users:login")
def issue_list(request):
    """Display list of all issues with filtering"""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    
    issues = Issue.objects.filter(
        Q(project__members=request.user) |
        Q(assignees=request.user)
    ).distinct()
    
    if search_query:
        issues = issues.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if status_filter:
        issues = issues.filter(status=status_filter)
    if priority_filter:
        issues = issues.filter(priority=priority_filter)
    
    issues = issues.order_by('-updated_at')
    paginator = Paginator(issues, 10)
    page = request.GET.get('page', 1)
    issues = paginator.get_page(page)
    
    context = {
        'issues': issues,
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'status_choices': Issue.STATUS_CHOICES,
        'priority_choices': Issue.PRIORITY_CHOICES,
    }
    return render(request, 'main/issue_list.html', context)

@login_required(login_url="users:login")
def issue_detail(request, pk):
    """Display issue details, comments, and attachments"""
    issue = get_object_or_404(Issue, pk=pk)
    
    if request.user not in issue.project.members.all():
        messages.error(request, "You don't have access to this issue.")
        return redirect('main:issue-list')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        attachment_form = AttachmentForm(request.POST, request.FILES)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.issue = issue
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('main:issue-detail', pk=pk)
            
        if attachment_form.is_valid():
            attachment = attachment_form.save(commit=False)
            attachment.issue = issue
            attachment.uploaded_by = request.user
            attachment.save()
            messages.success(request, 'Attachment uploaded successfully.')
            return redirect('main:issue-detail', pk=pk)
    else:
        comment_form = CommentForm()
        attachment_form = AttachmentForm()
    
    context = {
        'issue': issue,
        'comments': issue.comments.all().order_by('-created_at'),
        'attachments': issue.attachments.all(),
        'comment_form': comment_form,
        'attachment_form': attachment_form,
    }
    return render(request, 'main/issue_detail.html', context)

@login_required(login_url="users:login")
def issue_create(request, project_pk=None):
    """Create a new issue"""
    project = None
    if project_pk:
        project = get_object_or_404(Project, pk=project_pk)
        if request.user not in project.members.all():
            messages.error(request, "You don't have access to this project.")
            return redirect('main:project-list')
    
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            if project:
                issue.project = project
            issue.creator = request.user
            issue.save()
            form.save_m2m()
            messages.success(request, 'Issue created successfully.')
            return redirect('main:issue-detail', pk=issue.pk)
    else:
        form = IssueForm(initial={'project': project} if project else {})
    
    return render(request, 'main/issue_form.html', {
        'form': form,
        'title': 'Create Issue',
        'project': project
    })

@login_required(login_url="users:login")
def issue_update(request, pk):
    """Update existing issue"""
    issue = get_object_or_404(Issue, pk=pk)
    
    if request.user not in issue.project.members.all():
        messages.error(request, "You don't have permission to edit this issue.")
        return redirect('main:issue-list')
    
    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            messages.success(request, 'Issue updated successfully.')
            return redirect('main:issue-detail', pk=issue.pk)
    else:
        form = IssueForm(instance=issue)
    
    return render(request, 'main/issue_form.html', {
        'form': form,
        'title': 'Update Issue',
        'issue': issue
    })

@login_required(login_url="users:login")
def issue_delete(request, pk):
    """Delete existing issue"""
    issue = get_object_or_404(Issue, pk=pk)
    
    if request.user not in issue.project.members.all():
        messages.error(request, "You don't have permission to edit this issue.")
        return redirect('main:issue-list')
    
    issue_title = issue.title
    issue.delete()
    messages.success(request, f"Issue '{issue_title}' deleted successfully.")
    
    return redirect('main:issue-list')

# API Endpoints
@login_required(login_url="users:login")
def update_issue_status(request, pk):
    """API endpoint to update issue status"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    issue = get_object_or_404(Issue, pk=pk)
    if request.user not in issue.project.members.all():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    new_status = request.POST.get('status')
    if new_status not in dict(Issue.STATUS_CHOICES):
        return JsonResponse({'error': 'Invalid status'}, status=400)
    
    issue.status = new_status
    issue.save()
    
    return JsonResponse({
        'success': True,
        'status': issue.get_status_display()
    })

@login_required
def add_issue_comment(request, pk):
    """
    Add a comment to an issue
    """
    if request.method != 'POST':
        return HttpResponseForbidden()
    
    issue = get_object_or_404(Issue, pk=pk)
    
    # Check if user has permission to comment on this issue
    if not issue.project.members.filter(id=request.user.id).exists():
        messages.error(request, "You don't have permission to comment on this issue.")
        return HttpResponseForbidden()
    
    content = request.POST.get('content', '').strip()
    
    if content:
        # Create the comment
        comment = Comment.objects.create(
            issue=issue,
            author=request.user,
            content=content
        )
        
        # Optional: Send notification to issue assignees and creator
        # notify_issue_update(issue, request.user, 'comment')
        
        messages.success(request, 'Comment added successfully.')
    else:
        messages.error(request, 'Comment cannot be empty.')
    
    # Redirect back to the issue detail page
    return redirect('main:issue-detail', pk=issue.pk)


@login_required(login_url="users:login")
@require_POST
def delete_comment(request, pk):
    """Delete a comment"""
    comment = get_object_or_404(Comment, pk=pk)
    
    if comment.author != request.users:
        messages.error(request, "You don't have permission to delete this comment.")
        return redirect('main:issue-detail', pk=comment.issue.pk)
    
    comment.delete()
    messages.success(request, 'Comment deleted successfully.')
    return redirect('main:issue-detail', pk=comment.issue.pk)
