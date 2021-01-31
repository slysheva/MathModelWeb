from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'webservice'
urlpatterns = [
    url(r'^main/$', views.main_page, name='main'),
    url(r'^answer/$', views.get_result, name='answer'),
    url(r'^model/$', views.model, name='model'),
    url(r'^journal/$', views.get_journal, name='journal'),
    path('show_result/<uuid:task_info_id>/', views.show_result, name='show_result')
]
