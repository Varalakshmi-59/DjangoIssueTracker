from django.contrib import admin
from .models import Project, Issue, Comment, Resolution, Label, Attachment

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Resolution)
admin.site.register(Label)
admin.site.register(Attachment)
