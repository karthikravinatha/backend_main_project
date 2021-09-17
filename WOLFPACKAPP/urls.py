from django.urls import path,include
from . import views
from . import url_mapping 


urlpatterns = [
    path('auth', views.authenticate, name='authe'),
    path('session', views.check_session, name='check session'),
    
    path('uadd', views.add_user, name='user-add'),
    path('uupdate', views.update_user, name='user-update'),
    path('uget', views.get_user, name='user-get'),

    path('padd', views.project_add, name='project-add'),
    path('pupdate', views.project_update, name='project-update'),
    path('pdelete', views.project_delete, name='project-delete'),
    path('pigetlist', views.get_project_and_issues, name='project-getlist'),

    path('sadd', views.sprint_add, name='sprint-add'),
    path('sdelete', views.sprint_delete, name='sprint-delete'),
    path('sgetlist', views.get_sprint_list, name='sprint-getlist'),

    path('wadd', views.add_watcher, name='add-watchers'),

    path('cadd', views.add_comment, name='comment-add'),
    path('cupdate', views.update_comment, name='comment-update'),
    path('cdelete', views.delete_comment, name='comment-delete'),

    path('dailymail', views.open_issue_mail, name='daily mails'),
]