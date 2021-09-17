from django.http import HttpRequest, HttpResponse
from WOLFPACKAPP.Base.helper import ResponseObject
from django.core.serializers.json import DjangoJSONEncoder
import json


class Base_Controller:
    def __init__(self,request):
        pass

    def convert_to_dict(obj):
        return obj.__dict__    


    def send_response(self, response_object, http_status=200):        
        json_object = json.dumps(response_object)
        return HttpResponse(json_object)

    # def send_response(self, response_object, response_message="Success", http_status=200):
    #     obj = ResponseObject(response_message, response_object, http_status)
    #     json_object = json.dumps(obj, indent=2, cls=DjangoJSONEncoder)
    #     return HttpResponse(json_object)
        # , content_type='application/json', status=http_status)


