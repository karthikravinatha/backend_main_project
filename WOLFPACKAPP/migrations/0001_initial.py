# Generated by Django 3.2.7 on 2021-09-17 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='comment_detail',
            fields=[
                ('comment_detail_id', models.IntegerField(primary_key=True, serialize=False)),
                ('comment_id', models.IntegerField(null=True)),
                ('issue_id', models.IntegerField(null=True)),
                ('comments', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Comment_header',
            fields=[
                ('comment_id', models.IntegerField(primary_key=True, serialize=False)),
                ('created_by', models.IntegerField(null=True)),
                ('created_on', models.CharField(max_length=15)),
                ('project_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IssuesDetail',
            fields=[
                ('issue_id', models.IntegerField(primary_key=True, serialize=False)),
                ('issues_idd', models.IntegerField(null=True)),
                ('project_id', models.IntegerField(null=True)),
                ('asignee_id', models.IntegerField(null=True)),
                ('status_id', models.IntegerField(null=True)),
                ('priority', models.CharField(max_length=20)),
                ('target_resolution_date', models.CharField(max_length=10)),
                ('target_resolution_summary', models.CharField(max_length=500)),
                ('created_on', models.CharField(max_length=15)),
                ('created_by', models.IntegerField(null=True)),
                ('comment_id', models.IntegerField(null=True)),
                ('lable_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pissues',
            fields=[
                ('issues_idd', models.IntegerField(primary_key=True, serialize=False)),
                ('issue_type', models.CharField(max_length=24)),
                ('display_name', models.CharField(max_length=100)),
                ('created_on', models.CharField(max_length=15)),
                ('created_by', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectHeader',
            fields=[
                ('project_id', models.IntegerField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=256, null=True)),
                ('created_on', models.CharField(max_length=15)),
                ('created_by', models.IntegerField(null=True)),
                ('start_date', models.CharField(max_length=10)),
                ('end_date', models.CharField(max_length=10)),
                ('managed_by', models.IntegerField(null=True)),
                ('last_modified_by', models.IntegerField(null=True)),
                ('last_modified_on', models.CharField(max_length=15)),
                ('status_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SprintDetail',
            fields=[
                ('sprint_detail_id', models.IntegerField(primary_key=True, serialize=False)),
                ('sprint_id', models.IntegerField(null=True)),
                ('issues_idd', models.IntegerField(null=True)),
                ('discriptions', models.CharField(max_length=1024)),
                ('status_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SprintHeader',
            fields=[
                ('sprint_id', models.IntegerField(primary_key=True, serialize=False)),
                ('project_id', models.IntegerField(null=True)),
                ('sprint_start', models.CharField(max_length=15)),
                ('sprint_end', models.CharField(max_length=15)),
                ('created_on', models.CharField(max_length=15)),
                ('created_by', models.IntegerField(null=True)),
                ('managed_by', models.IntegerField(null=True)),
                ('status_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=245)),
                ('phone_no', models.CharField(max_length=12, null=True, unique=True)),
                ('password', models.CharField(max_length=12, null=True)),
                ('role_id', models.IntegerField(null=True)),
                ('reporting_to', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Watchars',
            fields=[
                ('watcher_id', models.IntegerField(primary_key=True, serialize=False)),
                ('project_id', models.IntegerField(null=True)),
                ('watcher_name', models.CharField(max_length=256)),
                ('Email', models.CharField(max_length=256)),
                ('created_on', models.CharField(max_length=15)),
                ('created_by', models.IntegerField(null=True)),
            ],
        ),
    ]
