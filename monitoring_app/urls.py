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
    url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^pid/$', views.pid, name='pid'),
    url(r'^getpid/$',views.pid_rest, name='pid_rest'),
    url(r'^delay/$',views.delay_rest, name='delay_rest'),
    url(r'^services/$',views.services_rest, name='services_rest'),
    url(r'^statusfirewall/$',views.statusfirew_rest, name='statusfirew_rest'),
    url(r'^route/$',views.defaultroute_rest, name='defaultroute_rest'),
    url(r'^disk/$',views.diskusage_rest, name='diskusage_rest'),
    url(r'^voluminousfile/$',views.volfile_rest, name='volfile_rest'),
    url(r'^cpu/$',views.cpu_rest, name='cpu_rest'),
    url(r'^pid/server1.html$',views.server1, name='server1'),
    url(r'^pid/status.html$',views.status, name='status'),

)
    
