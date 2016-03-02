from django.shortcuts import render ,render_to_response
from monitoring_app.forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, HttpResponse ,HttpRequest
from django.template import RequestContext
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
import json
import subprocess
import sys
import os
import re
import pexpect
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, serializers, viewsets
from .supervision import testpid as tp
from .supervision import testfirewall as tf
from .supervision import testdelay as td
from .supervision import testservices as ts
from .supervision import testroute as tr
from IPython import embed
from .supervision import testdisk as tdis
from .supervision import testvolfile as tv
from .supervision import testcpu as tc
# Create your views here.
def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': "Vous etes la bienvenue"}
    return render_to_response('monitoring_app/index.html', context_dict, context)
def about(request):

    context = RequestContext(request)
    context_dict = {'boldmessage': "Nous sommes ....."}
    return render_to_response('monitoring_app/about.html', context_dict, context)

def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()
    return render_to_response(
            'monitoring_app/register.html',
            {'user_form': user_form, 'registered': registered},
            context)

def user_login(request):

    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user :
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/monitoring_app/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render_to_response('monitoring_app/login.html', {}, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/monitoring_app/')
@login_required
def pid (request) :
    context = RequestContext(request)
    if request.method == 'GET':
        Process_name = request.GET.get('Process name')
        Process_pid = request.POST.get('Process pid')

    return render_to_response(
            'monitoring_app/process1.html',{},context)
# Serializers define the API representation.
def pid_rest(request):
    process_name =  request.GET.get('pidname')
    message = tp.get_pid(process_name)
    i=message.find('{')
    j=message.find('}')+1
    message=message[i:j]
    message= message.replace("'", "\"")
    messages = json.loads(message)
    data = json.dumps(messages)
    return HttpResponse(data, content_type='application/json')
def statusfirew_rest(request):
    message=tf.get_firewall()
    i=message.find('{')
    j=message.find('}')+1
    message=message[i:j]
    message= message.replace("'", "\"")
    messages = json.loads(message)
    data = json.dumps(messages)
    return HttpResponse(data, content_type='application/json')
def defaultroute_rest(request):
    message=tr.get_route()
    i=message.find('{')
    j=message.find('}')+1
    message=message[i:j]
    message= message.replace("'", "\"")
    messages = json.loads(message)
    data = json.dumps(messages)
    return HttpResponse(data, content_type='application/json')
def delay_rest(request):
    message=td.get_delay()
    i=message.find('{')
    j=message.find('}')+1
    message=message[i:j]
    message= message.replace("'", "\"")
    messages = json.loads(message)
    data = json.dumps(messages)
    return HttpResponse(data, content_type='application/json')
def services_rest(request):
    message=ts.get_services()
    i=message.find('{')
    j=message.find('}')+1
    message=message[i:j]
    message = json_acceptable_string = message.replace("'", "\"")
    messages = json.loads(message)
    data = json.dumps(messages)
    return HttpResponse(data, content_type='application/json')

def diskusage_rest(request):
    message=tdis.get_disk()
    i=message.find('{')
    j=message.find('}')+1
    message=message[i:j]
    message= message.replace("'", "\"")
    messages = json.loads(message)
    data = json.dumps(messages)
    return HttpResponse(data, content_type='application/json')
def volfile_rest(request):
    message=tv.get_volfile()
    i=message.find('{')
    j=message.find('}')+1
    message=message[i:j]
    message= message.replace("'", "\"")
    messages = json.loads(message)
    data = json.dumps(messages)
    return HttpResponse(data, content_type='application/json')

def cpu_rest(request):
    message=tc.get_cpu()
    i=message.find('{')
    j=message.find('}')+1
    message=message[i:j]
    message= message.replace("'", "\"")
    messages = json.loads(message)
    data = json.dumps(messages)
    return HttpResponse(data, content_type='application/json')




