from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.app2_index, name='index'),
    url(r'^simple', views.app2_simple, name='simple'),
    url(r'^log', views.app2_log, name='log'),
    url(r'^childspan', views.app2_child_span, name='childspan')
]