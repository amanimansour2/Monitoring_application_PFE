from django.shortcuts import get_object_or_404,render_to_response
from django.http import HttpResponse
from django.conf.urls import include,patterns, url
from django.contrib.auth.models import User
from django.core.management import call_command
from monitoring_app import views
from rest_framework import routers, serializers, viewsets
# Serializers define the API representation.

class UserSerializer(serializers.HyperlinkedModelSerializer):
 class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
urlpatterns += patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^down/$', views.down, name='down'),
    url(r'^downwav/$', views.downwav, name='downwav'),
    url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
    url(r'^pid/add_machine.html$', views.add_machine, name='add_machine'),
    url(r'^pid/del_machine/$', views.deletemach, name='deletemach'), 	
    url(r'^pid/del_machine.html$', views.deletemachine, name='deletemachine'), 	
    url(r'^pid/edit_machine/$', views.editmach, name='editmach'), 	
    url(r'^pid/edit_machine.html$', views.editmachine, name='editmachine'), 	
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^pid/$', views.pid, name='pid'),
    url(r'^getpid/$',views.pid_rest, name='pid_rest'),
    url(r'^delay/$',views.delay_rest, name='delay_rest'),
    url(r'^services/$',views.services_rest, name='services_rest'),
    url(r'^statusfirewall/$',views.statusfirew_rest, name='statusfirew_rest'),
    url(r'^regphone/$',views.regphone_rest, name='regphone_rest'),
    url(r'^freeswitchcommunication/$',views.freecommu_rest, name='freecommu_rest'),	
    url(r'^numberconfig/$',views.numberconfig_rest, name='numberconfig_rest'),
    url(r'^makecall/$',views.begincall_rest, name='begincall_rest'),		
    url(r'^numberdelete/$',views.numberdelete_rest, name='numberdelete_rest'),	
    url(r'^numbersoftconfig/$',views.numbersoftconfig_rest, name='numbersoftconfig_rest'),	
    url(r'^numbersoftdelete/$',views.numbersoftdelete_rest, name='numbersoftdelete_rest'),	
    url(r'^statusgeneral/$',views.statusgeneral_rest, name='statusgeneral_rest'),
    url(r'^route/$',views.defaultroute_rest, name='defaultroute_rest'),
    url(r'^pid/edit_machine_DB/$',views.olddata_rest, name='olddata_rest'),
    url(r'^disk/$',views.diskusage_rest, name='diskusage_rest'),
    url(r'^voluminousfile/$',views.volfile_rest, name='volfile_rest'),
    url(r'^cpu/$',views.cpu_rest, name='cpu_rest'),
    url(r'^initialize/$',views.initialize_rest, name='initialize_rest'),
    url(r'^pid/machine/$',views.detail, name='machine_detail'),
    url(r'^pid/FreeSWITCH/$',views.freedetail, name='freeswitch_detail'),
    url(r'^pid/$',views.status, name='status'),
    url(r'^pid/add_machine/$',views.add_machine, name='add_machine'),
    url(r'^reinviteconfig/$',views.reinvite_conf, name='reinvite_conf'),
    url(r'^inviteconfig/$',views.invite_conf, name='invite_conf'),
    url(r'^calltest/$',views.call_test, name='call_test'),
)
    
