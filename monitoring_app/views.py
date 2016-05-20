# -*- coding: utf-8 -*-
from django.shortcuts import render ,render_to_response
from monitoring_app.models import UserProfile,Machine,Call
from monitoring_app.forms import UserForm,MachineForm,CallForm
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
import requests
import re
import pexpect
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, serializers, viewsets  
from .supervision import testconfcall as tnumconf
from .supervision import testdeletnumber as tnumdel
from .supervision import testconfsoftcall as tnumsoftconf
from .supervision import testdeletsoftnumber as tnumsoftdel
from .supervision import testpid as tp
from .supervision import testspeech as tcall
from .supervision import testfirewall as tf
from .supervision import testdelay as td
from .supervision import testservices as ts
from .supervision import testfreeconnect as tcommu
from .supervision import testroute as tr
from .supervision import statusmachine as tg
from .supervision import initialize as tinit
from .supervision import testcallwithscenarioinvite as tconfiginvite
from .supervision import testcallwithscenarioreinvite as tconfigreinvite
from .supervision import testcallscenario as ttest
from IPython import embed
from .supervision import testdisk as tdis
from .supervision import testvolfile as tv
from .supervision import testcpu as tc
import os.path
from .supervision import testregphone as treg
# Create your views here.
def down(request):
    file_path='/home/amani/projet/test.pcap'
    my_file = open(file_path,'rb').read()
    return HttpResponse(my_file, content_type = "application/vnd.tcpdump.pcap") 
def downwav(request):
    my_file = open(path,'rb').read()
    return HttpResponse(my_file, content_type = "audio/x-wav") 	
def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': "Vous etes la bienvenue"}
    return render_to_response('monitoring_app/index.html', context_dict, context)
def detail(request):
    context = RequestContext(request)
    global machine_id
    if request.method == 'GET': 
        machine_id = request.GET.get('machine_id')
    return render_to_response('monitoring_app/pid/machine.html',data(), context)
def freedetail(request):
    context = RequestContext(request)
    global machine_id
    if request.method == 'GET': 
        machine_id = request.GET.get('machine_id')
    return render_to_response('monitoring_app/pid/freeswitch.html',data(), context)

def data ():
    machine = Machine.objects.all()
    call = Call.objects.all()
    data = {
    "machine_detail" : machine
    }
    return data
	
def olddata_rest (request):
    d={}
    oldname =  request.GET.get('oldname')
    machine = Machine.objects.get(name=oldname)
    d['username']=machine.username
    d['address']=machine.address
    d['password']=machine.password
    d['Prefix_freeswitch']=machine.Prefix_freeswitch
    print d
    data = json.dumps(d)
    return HttpResponse(data, content_type='application/json')
def status(request):
    context = RequestContext(request)
    return render_to_response('monitoring_app/pid/status.html',data(), context)
def about(request):

    context = RequestContext(request)
    context_dict = {'boldmessage': "Nous sommes ....."}
    return render_to_response('monitoring_app/about.html', context_dict, context)
def add_machine(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        machine_form = MachineForm(data=request.POST)
        if machine_form.is_valid():
            machine = machine_form.save()
            machine.save()
            registered = True
        else:
            print machine_form.errors

    else:
        machine_form = MachineForm()
    return render_to_response(
            'monitoring_app/pid/add_machine.html',
            dict({'machine_form': machine_form, 'registered': registered}.items()+data().items()),
            context)
def deletemachine(request):
    namee=request.GET.get("namemachine")
    print namee
    return render_to_response('monitoring_app/pid/del_machine.html',data(),{})
def deletemach(request):
    namee=request.GET.get("namemachine")
    machine=Machine.objects.get(name=namee)
    machine.delete()
    return HttpResponse('done')
def editmachine(request):
    return render_to_response('monitoring_app/pid/edit_machine.html',data(),{})
def editmach(request):
    oldname=request.GET.get("oldname")
    newname=request.GET.get("newname")
    newaddress=request.GET.get("newaddress")
    newpassword=request.GET.get("newpassword")
    newprefix=request.GET.get("newprefix")
    newusername=request.GET.get("newusername")
    machine=Machine.objects.get(name=oldname)
    machine.name=newname
    machine.address=newaddress
    machine.password=newpassword
    machine.username=newusername
    machine.Prefix_freeswitch=newprefix
    machine.save()
    return HttpResponse('done')
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
    print "in pid view"
    #machine = Machine.objects.all()
    context = RequestContext(request)
    if request.method == 'GET':
        Process_name = request.GET.get('Process name')
    return render_to_response(
            'monitoring_app/status.html',data(),context)
# Serializers define the API representation.
def pid_rest(request):
    process_name =  request.GET.get('pidname')
    message = tp.get_pid(process_name,machine_id)
    i=message.find('{')
    j=message.find('}')+1
    message=message[i:j]
    message= message.replace("'", "\"")
    messages = json.loads(message)
    data = json.dumps(messages)
    return HttpResponse(data, content_type='application/json')
def statusfirew_rest(request):
    fire = tf.get_firewall(machine_id)
    data = json.dumps({"firewall":fire})
    return HttpResponse(data, content_type='application/json')
def statusgeneral_rest(request):
    machine_id1 = request.GET.get('id')
    status = tg.get_statuss(machine_id1)
    data = json.dumps({"status":status})
    return HttpResponse(data, content_type='application/json')
def defaultroute_rest(request):
    route = tr.get_route(machine_id)
    data = json.dumps({"route":route})
    return HttpResponse(data, content_type='application/json')
def delay_rest(request):
    delay = td.get_delay(machine_id)
    data = json.dumps({"delay":delay})
    return HttpResponse(data, content_type='application/json')
def services_rest(request):
    dhcpstatus,dnsstatus,freestatus,ntpstatus = ts.get_services(machine_id)
    data = json.dumps({"dhcpstatus":dhcpstatus,"dnsstatus":dnsstatus,"freestatus":freestatus,"ntpstatus":ntpstatus})
    return HttpResponse(data, content_type='application/json')
def diskusage_rest(request):
    disk = tdis.get_disk(machine_id)
    data = json.dumps({"disk":disk})
    return HttpResponse(data, content_type='application/json')
def volfile_rest(request):
    volfile = tv.get_volfile(machine_id)
    data = json.dumps({"volfile":volfile})
    return HttpResponse(data, content_type='application/json')
def cpu_rest(request):
    cpu = tc.get_cpu(machine_id)
    data = json.dumps({"cpu":cpu})
    return HttpResponse(data, content_type='application/json')
def regphone_rest(request):
    phone = treg.get_regphone(machine_id)
    data = json.dumps({"phone":phone})
    return HttpResponse(data, content_type='application/json')
def freecommu_rest(request):
    status=tcommu.get_freecommu(machine_id)
    data = json.dumps({"stat":status})
    return HttpResponse(data, content_type='application/json')
def begincall_rest(request):
    time1 =  request.GET.get('time1')
    status=tcall.get_begincall(time1,machine_id)
    data = json.dumps({"wavname":status})
    global path
    path=str(status).replace(" ","")
    return HttpResponse(data, content_type='application/json')
def numberconfig_rest(request):
    number =  request.GET.get('number')
    codec =  request.GET.get('codec')
    file =  request.GET.get('file')
    status=tnumconf.get_confnumber(number,codec,file,machine_id)
    data = json.dumps({"statnumber":status})
    return HttpResponse(data, content_type='application/json')
def numberdelete_rest(request):
    number1 =  request.GET.get('numbertodelete')
    status1=tnumdel.get_delnumber(number1,machine_id)
    data = json.dumps({"delnumber":status1})
    return HttpResponse(data, content_type='application/json')
def numbersoftconfig_rest(request):
    number =  request.GET.get('number')
    scenario =  request.GET.get('scenario')
    adphone =  request.GET.get('adphone')
    dtmf =  request.GET.get('dtmf')
    selecteddd =  request.GET.get('selecteddd')
    status=tnumsoftconf.get_confsoftnumber(number,scenario,machine_id,adphone,dtmf,selecteddd)
    data = json.dumps({"statnumber":status})
    return HttpResponse(data, content_type='application/json')
def invite_conf(request):
    numsrc =  request.GET.get('numsrc')
    numdest =  request.GET.get('numdest')
    scenarioinvite =  request.GET.get('scenarioinvite')
    addphone=request.GET.get('addphone')
    checked=request.GET.get('checked')
    dure=request.GET.get('dure')
    interface=request.GET.get('interface')
    status=tconfiginvite.get_confcall(numsrc,numdest,scenarioinvite,machine_id,addphone,dure,interface,checked)
    data = json.dumps({"statcall":status})
    return HttpResponse(data, content_type='application/json')
def reinvite_conf(request):
    numclient =  request.GET.get('numclient')
    addclient =  request.GET.get('addclient')
    scenarioreinvite =  request.GET.get('scenarioreinvite')
    checked=request.GET.get('checked')
    dure=request.GET.get('dure')
    interface=request.GET.get('interface')
    status=tconfigreinvite.get_confcall1(numclient,addclient,scenarioreinvite,machine_id,dure,interface,checked)
    data = json.dumps({"statcall":status})
    return HttpResponse(data, content_type='application/json')
def call_test(request):
    checked=request.GET.get('checked')
    dure=request.GET.get('dure')
    interface=request.GET.get('interface')
    status=ttest.get_testcall(machine_id,dure,interface,checked)
    data = json.dumps({"testscenarioo":status})
    return HttpResponse(data, content_type='application/json')
def numbersoftdelete_rest(request):
    number1 =  request.GET.get('numbertodelete')
    status1=tnumsoftdel.get_delsoftnumber(number1,machine_id)
    data = json.dumps({"delnumber":status1})
    return HttpResponse(data, content_type='application/json')
def initialize_rest(request):
    status1=tinit.get_initialize(machine_id)
    data = json.dumps({"initialisation":status1})
    return HttpResponse(data, content_type='application/json')

