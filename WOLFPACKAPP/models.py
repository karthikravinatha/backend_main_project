from django.db import models
from datetime import datetime

from django.db.models.base import Model
from django.db.models.fields import EmailField
# Create your models here.

class Users(models.Model):
    user_id = models.IntegerField(primary_key=True,)
    name = models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=245)
    phone_no = models.CharField(max_length=12,null=True,unique=True)
    password = models.CharField(max_length=12,null=True)
    role_id = models.IntegerField(null=True)
    reporting_to = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    # input_formats=["%d %b %Y %H:%M:%S %Z"]
    created_by = models.IntegerField(null=False)

    def __str__(self):
        return self.name

class ProjectHeader(models.Model):
    project_id = models.IntegerField(primary_key=True)
    project_name = models.CharField(max_length=256,null=True)
    created_on = models.CharField(max_length=15)
    created_by = models.IntegerField(null=True)
    start_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)
    managed_by = models.IntegerField(null=True)
    last_modified_by = models.IntegerField(null=True)
    last_modified_on = models.CharField(max_length=15)
    status_id = models.IntegerField(default=0)

    def __str__(self):
        return self.project_name

class IssuesDetail(models.Model):
    issue_id = models.IntegerField(primary_key=True)
    issues_idd = models.IntegerField(null=True)
    project_id = models.IntegerField(null=True)
    asignee_id = models.IntegerField(null=True)
    status_id = models.IntegerField(null=True)
    priority = models.CharField(max_length=20)
    target_resolution_date = models.CharField(max_length=10)
    target_resolution_summary = models.CharField(max_length=500)
    created_on = models.CharField(max_length=15)
    created_by = models.IntegerField(null=True)
    comment_id = models.IntegerField(null=True)
    lable_id = models.IntegerField(null=True)

    def __init__(self):
        return self.issue_id

class SprintHeader(models.Model):
    sprint_id = models.IntegerField(primary_key=True)
    project_id = models.IntegerField(null=True)
    sprint_start = models.CharField(max_length=15)
    sprint_end = models.CharField(max_length=15)
    created_on = models.CharField(max_length=15)
    created_by = models.IntegerField(null=True)
    managed_by = models.IntegerField(null=True)
    status_id = models.IntegerField(null=True)

    # def __init__(self):
    #     return self.project_id

class SprintDetail(models.Model):
    sprint_detail_id = models.IntegerField(primary_key=True)
    sprint_id = models.IntegerField(null=True)
    issues_idd = models.IntegerField(null=True)
    discriptions = models.CharField(max_length=1024)
    status_id = models.IntegerField(null=True)

    def __int__(self):
        return self.sprint_detail_id

class Comment_header(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    created_by = models.IntegerField(null=True)
    created_on = models.CharField(max_length=15)
    project_id = models.IntegerField(null=True)

class comment_detail(models.Model):
    comment_detail_id = models.IntegerField(primary_key=True)
    comment_id = models.IntegerField(null=True)
    issue_id = models.IntegerField(null=True)
    comments = models.CharField(max_length=1024)

class Watchars(models.Model):
    watcher_id = models.IntegerField(primary_key=True)
    project_id = models.IntegerField(null=True)
    watcher_name = models.CharField(max_length=256)
    Email = models.CharField(max_length=256)
    created_on = models.CharField(max_length=15)
    created_by = models.IntegerField(null=True)

    def __int__(self):
        return self.watcher_id

class Pissues(models.Model):
    issues_idd = models.IntegerField(primary_key=True)
    issue_type = models.CharField(max_length=24)
    display_name = models.CharField(max_length=100)
    created_on = models.CharField(max_length=15)
    created_by = models.IntegerField(null=True)

    def __int__(self):
        return self.issues_idd

