from django.http import HttpResponse, HttpRequest
from django.db import connections
# from googleapiclient.discovery import build
# from google.oauth2 import service_account
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from enum import Enum
from WOLFPACKAPP.Base.helper import RequestConfig,EmailHelper
from WOLFPACKAPP.models import Users
from WOLFPACKAPP.models import ProjectHeader
from WOLFPACKAPP.models import IssuesDetail
from WOLFPACKAPP.models import SprintHeader
from WOLFPACKAPP.models import SprintDetail
from WOLFPACKAPP.models import Comment_header
from WOLFPACKAPP.models import comment_detail
from WOLFPACKAPP.models import Watchars
from WOLFPACKAPP.Base.base_controller import Base_Controller
from django.http import JsonResponse
from WOLFPACKAPP.Base.helper import ResponseObject
from django.core.serializers.json import DjangoJSONEncoder
from WOLFPACKAPP.Base.helper import JWTManager
from datetime import datetime, timezone, timedelta


#this is for authentication
def authenticate(request:HttpRequest):
    if request.method == "GET":
        params = {"phone_no":request.GET.get("phone_no",0),
                "password":request.GET.get("password")}
        cursor = connections['default'].cursor()
        cursor.execute(
            "SELECT user_id,name,email,phone_no,role_id,reporting_to from WOLFPACKAPP_users WHERE phone_no=%s AND password=%s",
            [params['phone_no'],params['password']])
        data = cursor.fetchall()
        s = {
            "user_id":data[0][0],
            "name":data[0][1],
            "email":data[0][2],
            "phone_no":data[0][3],
            "role_id":data[0][4],
            "reporting_to":data[0][5]
        }
        cur = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        expire = datetime.strptime(cur, '%Y-%m-%d %H:%M:%S') + timedelta(hours=4)
        s['expires_on'] = str(expire)
        s['checksum'] = JWTManager.get_checksum(s)
        print(s)
        token = JWTManager.generate_token(s)
        print(token)
        token_dict = {"token": str(token), "data": s}
        return send_response(token_dict)                       


def check_session(request: HttpRequest):
    try:
        if request.method != "OPTIONS":
            if 'HTTP_AUTHORIZATION' in request.META:
                token_payload = JWTManager.decode_token(
                    request.META['HTTP_AUTHORIZATION'].replace("Bearer ", ''))

                # Check the checksum
                cp_token_val = dict(token_payload)
                cp_token_val.pop("checksum")

                cs = JWTManager.get_checksum(cp_token_val)

                if token_payload.get("checksum") != cs:
                    raise PermissionError()

                # Check whether the token is expired
                expire_str = token_payload.get("expires_on")
                cur = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                datetime_obj = datetime.strptime(expire_str, '%Y-%m-%d %H:%M:%S')

                if datetime.strptime(cur, '%Y-%m-%d %H:%M:%S') > datetime_obj:
                    raise PermissionError()                    
            else:
                raise PermissionError()
    except Exception as ex:
        raise ex

def get_cursor(db_type='W'):
    if db_type == 'W':
        cursor = connections['default'].cursor()
        return cursor

def send_response(response_object, response_message="Success", http_status=200):
    obj = ResponseObject(response_message, response_object, http_status)
    json_object = json.dumps(obj, default=convert_to_dict, indent=2, cls=DjangoJSONEncoder)
    return HttpResponse(json_object, content_type='application/json', status=http_status)

def convert_to_dict(obj):
    return obj.__dict__

def add_user(request: HttpRequest):
        check_session(request)
        user_object: Users = Users()
        user_dict = json.loads(request.POST.get("user_object"))
        temp = {}
        user_object.name = user_dict.get("name")
        user_object.email = user_dict.get("email")
        user_object.phone_no = user_dict.get("phone_no")
        user_object.password = user_dict.get("password")
        user_object.role_id = user_dict.get("role_id")
        user_object.reporting_to = user_dict.get("reporting_to")
        user_object.created_on = user_dict.get("created_on")
        user_object.created_by = user_dict.get("created_by")
        try:
            cursor = connections['default'].cursor()
            s = cursor.execute(
                "INSERT INTO WOLFPACKAPP_users(name,email,phone_no,password,role_id,reporting_to,created_on,created_by) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                [user_object.name, user_object.email, user_object.phone_no, user_object.password, user_object.role_id,
                 user_object.reporting_to, user_object.created_on, user_object.created_by])
                        
            temp["name"] = user_object.name
            temp["email"] = user_object.email
            temp["phone_no"] = user_object.phone_no
            temp["password"] = user_object.password
            temp["role_id"] = user_object.role_id
            temp["reporting_to"] = user_object.reporting_to
            temp["created_on"] = user_object.created_on
            temp["created_by"] = user_object.created_by
            # temp["id"] = list(id)
        except Exception as ex:
            raise ex
        id = Users.objects.latest('user_id')
        temp["user_id"] = id.user_id
        return send_response(temp)

def update_user(request:HttpRequest):
    check_session(request)
    user_object: Users = Users()
    user_dict = json.loads(request.POST.get("user_object"))
    temp = {}
    user_object.user_id = user_dict.get("user_id")
    user_object.name = user_dict.get("name")
    user_object.email = user_dict.get("email")
    # user_object.phone_no = user_dict.get("phone_no")
    # user_object.password = user_dict.get("password")
    user_object.role_id = user_dict.get("role_id")
    user_object.reporting_to = user_dict.get("reporting_to")
    user_object.created_on = user_dict.get("created_on")
    user_object.created_by = user_dict.get("created_by")
    try:
        cursor = connections['default'].cursor()
        s = cursor.execute(
            "UPDATE WOLFPACKAPP_users SET name=%s,email=%s,role_id=%s,reporting_to=%s,created_on=%s,created_by=%s WHERE user_id=%s",
            [user_object.name, user_object.email, user_object.role_id,
                user_object.reporting_to, user_object.created_on, user_object.created_by, user_object.user_id])        
        temp["user_id"] = user_object.user_id
        temp["name"] = user_object.name
        temp["email"] = user_object.email
        # temp["phone_no"] = user_object.phone_no
        # temp["password"] = user_object.password
        temp["role_id"] = user_object.role_id
        temp["reporting_to"] = user_object.reporting_to
        temp["created_on"] = user_object.created_on
        temp["created_by"] = user_object.created_by
    except Exception as ex:
        raise ex
    return send_response(temp)

def get_user(request:HttpRequest):
    check_session(request)
    if request.method == "GET":
        user_object: Users = Users()
        params = {"id":request.GET.get("id","")}
        temp = []
        # print(params['id'])
        try:
            cursor = connections['default'].cursor()
            # date_format(Invoice_Date, '%d/%m/%Y')
            cursor.execute(
                "SELECT user_id,name,email,phone_no,password,role_id,reporting_to,'created_on',created_by FROM wolfpackapp_users")
                # [user_object.name, user_object.email, user_object.role_id,
                #     user_object.reporting_to, user_object.created_on, user_object.created_by, user_object.user_id])        
            s = cursor.fetchall()
            for each_data in s:                
                data = {}
                data["user_id"] = each_data[0]
                data["name"] = each_data[1]
                data["email"] = each_data[2]
                data["phone_no"] = each_data[3]
                data["password"] = each_data[4]
                data["role_id"] = each_data[5]
                data["reporting_to"] = each_data[6]
                data["created_on"] = each_data[7]
                data["created_by"] = each_data[8]
                temp.append(data)
        except Exception as ex:
            raise ex
    return send_response(temp)


def project_add(request:HttpRequest):
    check_session(request)
    project_object: ProjectHeader = ProjectHeader()
    temp = {}
    project_dict = json.loads(request.POST.get("project_object"))
    project_object.project_name = project_dict.get("project_name")
    project_object.created_by = project_dict.get("created_by")
    project_object.created_on = project_dict.get("created_on")
    project_object.start_date = project_dict.get("start_date")
    project_object.end_date = project_dict.get("end_date")
    project_object.managed_by = project_dict.get("managed_by")
    project_object.last_modified_by = project_dict.get("last_modified_by")
    project_object.last_modified_on = project_dict.get("last_modified_on")
    project_object.status_id = project_dict.get("status_id")
    try:
        cursor = connections['default'].cursor()
        s = cursor.execute(
        "INSERT INTO WOLFPACKAPP_projectheader(project_name,created_by,created_on,start_date,end_date,managed_by,last_modified_by,last_modified_on,status_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        [project_object.project_name,
        project_object.created_by,
        project_object.created_on,
        project_object.start_date,
        project_object.end_date,    
        project_object.managed_by,
        project_object.last_modified_by,
        project_object.last_modified_on,
        project_object.status_id])
        id = ProjectHeader.objects.latest('project_id')

        issues = project_dict.get("issues")
        issue_detail = []
        if len(issues) > 0:
            if issues is not None:
                for each in issues:
                    cursor = connections['default'].cursor()
                    s = cursor.execute(
                    "INSERT INTO WOLFPACKAPP_issuesdetail(issues_idd,project_id,asignee_id,status_id,priority,target_resolution_date,target_resolution_summary,created_on,created_by,comment_id,lable_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [each["issues_idd"],id.project_id,each['asignee_id'],each['status_id'],each['priority'],
                    each['target_resolution_date'],each['target_resolution_summary'],
                    each['created_on'],each['created_by'],each['comment_id'],each['label_id']])
                    issue_detail.append(each)
        temp["project_name"] = project_object.project_name
        temp["created_by"] = project_object.created_by
        temp["created_on"] = project_object.created_on
        temp["start_date"] = project_object.start_date
        temp["end_date"] = project_object.end_date
        temp["managed_by"] = project_object.managed_by
        temp["last_modified_by"] = project_object.last_modified_by
        temp["last_modified_on"] = project_object.last_modified_on
        temp["status_id"] = project_object.status_id
        temp['project_id'] = id.project_id
        temp['issues'] = issue_detail
    except Exception as ex:
        raise ex
    return send_response(temp)

def project_update(request:HttpRequest):
    check_session(request)
    project_object: ProjectHeader = ProjectHeader()
    temp = {}
    project_dict = json.loads(request.POST.get("project_object"))
    project_object.project_id = project_dict.get("project_id")
    project_object.project_name = project_dict.get("project_name")
    project_object.created_by = project_dict.get("created_by")
    project_object.created_on = project_dict.get("created_on")
    project_object.start_date = project_dict.get("start_date")
    project_object.end_date = project_dict.get("end_date")
    project_object.managed_by = project_dict.get("managed_by")
    project_object.last_modified_by = project_dict.get("last_modified_by")
    project_object.last_modified_on = project_dict.get("last_modified_on")
    project_object.status_id = project_dict.get("status_id")
    try:
        cursor = connections['default'].cursor()
        s = cursor.execute(
        "UPDATE WOLFPACKAPP_projectheader SET project_name=%s,created_by=%s,created_on=%s,start_date=%s,end_date=%s,managed_by=%s,last_modified_by=%s,last_modified_on=%s,status_id=%s WHERE project_id=%s",
        [project_object.project_name,
        project_object.created_by,
        project_object.created_on,
        project_object.start_date,
        project_object.end_date,    
        project_object.managed_by,
        project_object.last_modified_by,
        project_object.last_modified_on,
        project_object.status_id,
        project_object.project_id])

        
        issues = project_dict.get("issues")
        issue_detail = []
        if len(issues) > 0:            
            for each in issues:
                print("1staa")
                cursor = connections['default'].cursor()
                cursor.execute(
                "UPDATE WOLFPACKAPP_issuesdetail SET issues_idd=%s,asignee_id=%s,status_id=%s,lable_id=%s WHERE issue_id=%s AND project_id=%s",
                [each["issues_idd"],
                each['asignee_id'],
                each['status_id'],
                each['label_id'],
                each['issue_id'],
                project_object.project_id])
                
                issue_detail.append(each)
        temp["project_id"] = project_object.project_id
        temp["project_name"] = project_object.project_name
        temp["created_by"] = project_object.created_by
        temp["created_on"] = project_object.created_on
        temp["start_date"] = project_object.start_date
        temp["end_date"] = project_object.end_date
        temp["managed_by"] = project_object.managed_by
        temp["last_modified_by"] = project_object.last_modified_by
        temp["last_modified_on"] = project_object.last_modified_on
        temp["status_id"] = project_object.status_id
        temp['project_id'] = project_object.project_id
        temp['issues'] = issue_detail
    except Exception as ex:
        raise ex
    return send_response(temp)

def project_delete(request:HttpRequest):
    check_session(request)
    project_object: ProjectHeader = ProjectHeader()    
    temp = {}
    project_dict = json.loads(request.POST.get("project_object"))
    project_object.project_id = project_dict.get("project_id")
    is_delete_project = project_dict.get("is_delete_project")
    issues = project_dict.get("issues")
    issue_detail = []
    # issue_object: IssuesDetail = IssuesDetail()
    if issues is not None:
        if len(issues) > 0:
            for each in issues:
                if each['issue_id'] is not None:
                    # issues["issue_id"] = each['issue_id']
                    try:
                        cursor = connections['default'].cursor()
                        s = cursor.execute(
                        "DELETE FROM WOLFPACKAPP_issuesdetail WHERE issue_id=%s AND project_id=%s",
                        [each['issue_id'],project_object.project_id])
                    except Exception as ex:
                        raise ex
                else:
                    try:
                        cursor = connections['default'].cursor()
                        s = cursor.execute(
                        "DELETE FROM WOLFPACKAPP_issuesdetail WHERE project_id=%s",
                        [project_object.project_id])
                        cursor.execute(
                        "DELETE FROM WOLFPACKAPP_issuesheader WHERE project_id=%s",
                        [project_object.project_id])
                    except Exception as ex:
                        raise ex                
                issue_detail.append(each)
    if is_delete_project == 1:
        try:
            cursor = connections['default'].cursor()
            s = cursor.execute(
            "DELETE FROM WOLFPACKAPP_projectheader WHERE project_id=%s",
            [project_object.project_id])
        except Exception as ex:
            raise ex
    temp['project_id'] = project_object.project_id
    temp['issues'] = issue_detail
    return send_response(temp)

def get_project_and_issues(request:HttpRequest):
    check_session(request)
    if request.method == "GET":
        params = {"project_id":request.GET.get("project_id",0)}
        temp = []
        pid = int(params['project_id'])
        try:
            if pid == 0:
                cursor = connections['default'].cursor()
                cursor.execute(
                "SELECT project_id,project_name,created_on,created_by,start_date,end_date,managed_by,last_modified_by,last_modified_on,status_id FROM WOLFPACKAPP_projectheader")
                s = cursor.fetchall()
                for each in s:
                    data = {}
                    data["project_id"] = each[0]
                    data["project_name"] = each[1]
                    data["created_by"] = each[2]
                    data["created_on"] = each[3]
                    data["start_date"] = each[4]
                    data["end_date"] = each[5]
                    data["managed_by"] = each[6]
                    data["last_modified_by"] = each[7]
                    data["last_modified_on"] = each[8]
                    data["status_id"] = each[9]

                    cursor.execute(
                        "SELECT issue_id,project_id,asignee_id,status_id,priority,target_resolution_date,target_resolution_summary,created_on,created_by,comment_id,lable_id FROM WOLFPACKAPP_issuesdetail WHERE project_id=%s",
                        [each[0]])
                    s = cursor.fetchall()
                    issue_list = []
                    issue_dict = {}
                    for each_issue in s:                        
                        issue_dict['issue_id'] = each_issue[0]
                        issue_dict['project_id'] = each_issue[1]
                        issue_dict['asignee_id'] = each_issue[2]
                        issue_dict['status_id'] = each_issue[3]
                        issue_dict['priority'] = each_issue[4]
                        issue_dict['target_resolution_date'] = each_issue[5]
                        issue_dict['target_resolution_summary'] = each_issue[6]
                        issue_dict['created_on'] = each_issue[7]
                        issue_dict['created_by'] = each_issue[8]
                        issue_dict['comment_id'] = each_issue[9]
                        issue_dict['lable_id'] = each_issue[10]
                        issue_list.append(issue_dict)
                    data['issues'] = issue_list
                    temp.append(data)
            else:
                cursor = connections['default'].cursor()
                cursor.execute(
                "SELECT project_id,project_name,created_on,created_by,start_date,end_date,managed_by,last_modified_by,last_modified_on,status_id FROM WOLFPACKAPP_projectheader WHERE project_id=%s",
                [pid])
                s = cursor.fetchall()
                for each in s:
                    data = {}
                    data["project_id"] = each[0]
                    data["project_name"] = each[1]
                    data["created_by"] = each[2]
                    data["created_on"] = each[3]
                    data["start_date"] = each[4]
                    data["end_date"] = each[5]
                    data["managed_by"] = each[6]
                    data["last_modified_by"] = each[7]
                    data["last_modified_on"] = each[8]
                    data["status_id"] = each[9]

                    cursor.execute(
                        "SELECT issue_id,project_id,asignee_id,status_id,priority,target_resolution_date,target_resolution_summary,created_on,created_by,comment_id,lable_id FROM WOLFPACKAPP_issuesdetail WHERE project_id=%s",
                        [each[0]])
                    s = cursor.fetchall()
                    issue_list = []
                    issue_dict = {}
                    for each_issue in s:                        
                        issue_dict['issue_id'] = each_issue[0]
                        issue_dict['project_id'] = each_issue[1]
                        issue_dict['asignee_id'] = each_issue[2]
                        issue_dict['status_id'] = each_issue[3]
                        issue_dict['priority'] = each_issue[4]
                        issue_dict['target_resolution_date'] = each_issue[5]
                        issue_dict['target_resolution_summary'] = each_issue[6]
                        issue_dict['created_on'] = each_issue[7]
                        issue_dict['created_by'] = each_issue[8]
                        issue_dict['comment_id'] = each_issue[9]
                        issue_dict['lable_id'] = each_issue[10]
                        issue_list.append(issue_dict)
                    data['issues'] = issue_list
                    temp.append(data)
        except Exception as ex:
            raise ex
    return send_response(temp)


def sprint_add(request:HttpRequest):
    check_session(request)
    sprint_object: SprintHeader = SprintDetail()
    temp = {}
    sprint_header_dict = json.loads(request.POST.get("sprint_object"))
    sprint_object.project_id = sprint_header_dict.get("project_id")
    sprint_object.sprint_start = sprint_header_dict.get("sprint_start")
    sprint_object.sprint_end = sprint_header_dict.get("sprint_end")
    sprint_object.created_on = sprint_header_dict.get("created_on")
    sprint_object.created_by = sprint_header_dict.get("created_by")
    sprint_object.managed_by = sprint_header_dict.get("managed_by")
    sprint_object.status_id = sprint_header_dict.get("status_id")
    try:
        cursor = connections['default'].cursor()
        s = cursor.execute(
        "INSERT INTO WOLFPACKAPP_sprintheader(project_id,sprint_start,sprint_end,created_on,created_by,managed_by,status_id) VALUES(%s,%s,%s,%s,%s,%s,%s)",
        [sprint_object.project_id,
        sprint_object.sprint_start,
        sprint_object.sprint_end,
        sprint_object.created_on,
        sprint_object.created_by,    
        sprint_object.managed_by,
        sprint_object.status_id])
        print("aaa")
        id = SprintHeader.objects.latest('sprint_id')
        print(type(id))

        sprint_issues = sprint_header_dict.get("detail")
        issue_detail = []
        if len(sprint_issues) > 0:
            if sprint_issues is not None:
                for each in sprint_issues:
                    cursor = connections['default'].cursor()
                    s = cursor.execute(
                    "INSERT INTO WOLFPACKAPP_sprintdetail(sprint_id,issues_idd,discriptions,status_id) VALUES(%s,%s,%s,%s)",
                    [id.sprint_id,each['issues_idd'],each['discriptions'],each['status_id']])
                    issue_detail.append(each)
        print("aaaaa")
        temp["project_id"] = sprint_object.project_id
        temp["sprint_start"] = sprint_object.sprint_start
        temp["sprint_end"] = sprint_object.sprint_end
        temp["created_on"] = sprint_object.created_on
        temp["created_by"] = sprint_object.created_by
        temp["managed_by"] = sprint_object.managed_by
        temp['sprint_id'] = id.sprint_id
        temp['sprint_issues'] = issue_detail
    except Exception as ex:
        raise ex
    return send_response(temp)


def sprint_delete(request:HttpRequest):
    check_session(request)
    sprint_object: SprintHeader = SprintHeader()    
    temp = {}
    sprint_dict = json.loads(request.POST.get("sprint_object"))
    sprint_object.project_id = sprint_dict.get("sprint_id")
    is_delete_sprint = sprint_dict.get("is_delete_sprint")
    sprint_issues = sprint_dict.get("detail")
    issue_detail = []
    # issue_object: IssuesDetail = IssuesDetail()
    if sprint_issues is not None:
        if len(sprint_issues) > 0:
            for each in sprint_issues:
                if each['sprint_detail_id'] is not None:
                    # issue_object.issue_id = each['issue_id']
                    try:
                        cursor = connections['default'].cursor()
                        s = cursor.execute(
                        "DELETE FROM WOLFPACKAPP_sprintdetail WHERE sprint_detail_id=%s AND sprint_id=%s",
                        [each['sprint_detail_id'],sprint_object.project_id])
                    except Exception as ex:
                        raise ex
                else:
                    try:
                        cursor = connections['default'].cursor()
                        s = cursor.execute(
                        "DELETE FROM WOLFPACKAPP_sprintdetail WHERE sprint_id=%s",
                        [sprint_object.sprint_id])
                    except Exception as ex:
                        raise ex                
                issue_detail.append(each)
    if is_delete_sprint == 1:
        try:
            cursor = connections['default'].cursor()
            s = cursor.execute(
            "DELETE FROM WOLFPACKAPP_sprintheader WHERE sprint_id=%s",
            [sprint_object.sprint_id])
        except Exception as ex:
            raise ex
    temp['project_id'] = sprint_object.project_id
    temp['issues'] = issue_detail
    return send_response(temp)

def get_sprint_list(request:HttpRequest):
    pass

def add_comment(request:HttpRequest):
    check_session(request)
    comment_object: Comment_header = Comment_header()
    temp = {}
    comment_dict = json.loads(request.POST.get("project_object"))
    comment_object.created_on = comment_dict.get("created_on")
    comment_object.created_by = comment_dict.get("created_by")
    comment_object.project_id = comment_dict.get("project_id")
    try:
        cursor = connections['default'].cursor()
        cursor = connections['default'].cursor()
        s = cursor.execute(
        "INSERT INTO WOLFPACKAPP_comment_header(created_on,created_by,project_id) VALUES(%s,%s,%s)",
        [comment_object.created_on,
        comment_object.created_by,
        comment_object.project_id])

        id = ProjectHeader.objects.latest('project_id')

        detail = comment_dict.get("detail")
        issue_detail = []
        if len(detail) > 0:
            if detail is not None:
                for each in detail:
                    cursor = connections['default'].cursor()
                    s = cursor.execute(
                    "INSERT INTO WOLFPACKAPP_comment_detail(comment_id,issue_id,comments) VALUES(%s,%s,%s)",
                    [id.comment_id,each['issue_id'],each['comments']])
                    issue_detail.append(each)
        temp["created_by"] = comment_object.created_by
        temp["created_on"] = comment_object.created_on
        temp["project_id"] = comment_object.project_id
        temp["comment_id"] = id.comment_id
        temp['detail'] = issue_detail
    except Exception as ex:
        raise ex
    return send_response(temp)

def update_comment(request:HttpRequest):
    check_session(request)
    comment_object: Comment_header = Comment_header()
    temp = {}
    comment_dict = json.loads(request.POST.get("project_object"))
    comment_object.comment_id = comment_dict.get("comment_id")
    # comment_object.created_on = comment_dict.get("created_on")
    # comment_object.created_by = comment_dict.get("created_by")
    # comment_object.project_id = comment_dict.get("project_id")
    try:        
        detail = comment_dict.get("detail")
        issue_detail = []
        if len(detail) > 0:
            if detail is not None:
                for each in detail:
                    cursor = connections['default'].cursor()
                    s = cursor.execute(
                    "UPDATE WOLFPACKAPP_comment_detail SET comments=%s WHERE comment_id=%s AND project_id=%s",
                    [each['comments'],comment_object.comment_id,each['project_id']])
                    issue_detail.append(each)
        temp["comment_id"] = comment_object.comment_id
        temp['detail'] = issue_detail
    except Exception as ex:
        raise ex
    return send_response(temp)

def delete_comment(request:HttpRequest):
    check_session(request)
    comment_object: Comment_header = Comment_header()    
    temp = {}
    comment_dict = json.loads(request.POST.get("comment_object"))
    comment_object.project_id = comment_dict.get("comment_id")
    is_delete_sprint = comment_dict.get("is_delete_comment")
    detail = comment_dict.get("detail")
    issue_detail = []
    # issue_object: IssuesDetail = IssuesDetail()
    if detail is not None:
        if len(detail) > 0:
            for each in detail:
                if each['comment_detail_id'] is not None:
                    # issue_object.issue_id = each['issue_id']
                    try:
                        cursor = connections['default'].cursor()
                        s = cursor.execute(
                        "DELETE FROM WOLFPACKAPP_comment_detail WHERE comment_detail_id=%s AND comment_id=%s",
                        [each['comment_detail_id'],comment_object.comment_id])
                    except Exception as ex:
                        raise ex
                else:
                    try:
                        cursor = connections['default'].cursor()
                        s = cursor.execute(
                        "DELETE FROM WOLFPACKAPP_comment_detail WHERE comment_id=%s",
                        [comment_object.comment_id])
                    except Exception as ex:
                        raise ex                
                issue_detail.append(each)
    if is_delete_sprint == 1:
        try:
            cursor = connections['default'].cursor()
            s = cursor.execute(
            "DELETE FROM WOLFPACKAPP_comment_header WHERE comment_id=%s",
            [comment_object.comment_id])
        except Exception as ex:
            raise ex
    temp['comment_id'] = comment_object.comment_id
    temp['issues'] = issue_detail
    return send_response(temp)

def add_watcher(request: HttpRequest):
    check_session(request)
    watcher_object: Watchars = Watchars()
    user_dict = json.loads(request.POST.get("watcher_object"))
    temp = {}
    watcher_object.project_id = user_dict.get("project_id")
    watcher_object.watcher_name = user_dict.get("watcher_name")
    watcher_object.Email = user_dict.get("Email")
    watcher_object.created_on = user_dict.get("created_on")
    watcher_object.created_by = user_dict.get("created_by")
    try:
        cursor = connections['default'].cursor()
        s = cursor.execute(
            "INSERT INTO WOLFPACKAPP_watchars(project_id,watcher_name,Email,created_on,created_by) VALUES(%s,%s,%s,%s,%s)",
            [watcher_object.project_id,watcher_object.watcher_name,watcher_object.Email,
            watcher_object.created_on,watcher_object.created_by])
                    
        temp["project_id"] = watcher_object.project_id
        temp["watcher_name"] = watcher_object.watcher_name  
        temp["Email"] = watcher_object.Email
        temp["created_on"] = watcher_object.created_on
        temp["created_by"] = watcher_object.created_by
        # temp["id"] = list(id)
    except Exception as ex:
        raise ex
    id = Watchars.objects.latest('watcher_id')
    temp["user_id"] = id.watcher_id
    return send_response(temp)

def get_watchers(request:HttpRequest):
    check_session(request)
    if request.method == "GET":
        watcher_object: Watchars = Watchars()
        params = {"id":request.GET.get("id","")}
        temp = []
        # print(params['id'])
        try:
            cursor = connections['default'].cursor()
            # date_format(Invoice_Date, '%d/%m/%Y')
            cursor.execute(
                "SELECT watcher_id,project_id,watcher_name,Email,created_on,created_by FROM WOLFPACKAPP_watchars")        
            s = cursor.fetchall()
            for each_data in s:                
                data = {}
                data["watcher_id"] = each_data[0]
                data["project_id"] = each_data[1]
                data["watcher_name"] = each_data[2]
                data["Email"] = each_data[3]
                data["created_on"] = each_data[4]
                data["created_by"] = each_data[5]
                temp.append(data)
        except Exception as ex:
            raise ex
    return send_response(temp)

def send_html_email(email_subject, email_body, email_recipients):
    host = "smtp.gmail.com"
    from_email = "karthikravinathadatascience@gmail.com"
    password = "Kar@8835"
    port = 587
    smtp = smtplib.SMTP(host= host, port= port)
    smtp.starttls()
    smtp.login(from_email, password)

    msg = MIMEMultipart()

    msg['From'] = from_email
    msg['To'] = email_recipients#"karthikravinatha@gmail.com"
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_body, 'html'))    

    re = smtp.send_message(msg)
    return re

def open_issue_mail(request:HttpRequest):
    name = ""
    recepients = []
    cursor = connections['default'].cursor()
    cursor.execute(
                "SELECT asignee_id FROM WOLFPACKAPP_issuesdetail where issues_idd = 1")        
    s = cursor.fetchall()
    user_id = None
    for i in s:
        i = str(i)
        user_id = i.replace(",","")
        user_id = user_id[1]

        cursor.execute(
                    "SELECT name,email FROM WOLFPACKAPP_users where user_id = %s",[user_id])        
        s = cursor.fetchall()
        for j in s:
            recepients.append(str(j[1]))
            name.join(j[0]+",")
            # print(j[1])
    print(recepients)

    res = []
    for i in recepients:
        body = "<html><body><h1>HELLO</h1><h5>you have an open issue take a look<h5></body></html>"
        # # recepient = str(s.email)
        subject = "OPEN ISSUE"
        a = send_html_email(subject,body,i)
        res.append(a)
    return send_response(a)
                

    





    
    


                        


# Create your views here.