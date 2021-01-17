from django.conf.urls import url

from . import views

app_name = 'webservice'
urlpatterns = [
    url(r'main/$', views.main_page, name='main'),
    url(r'^answer/$', views.get_result, name='answer'),
    url(r'^model/$', views.model, name='model'),
]
