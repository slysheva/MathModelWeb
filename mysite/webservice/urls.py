from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'webservice'
urlpatterns = [
    url(r'^main/$', views.main_page, name='main'),
    url(r'^answer/$', views.get_result, name='answer'),
    path('model/<model_id>/', views.model, name='model'),
    url(r'^journal/$', views.get_journal, name='journal'),
    path('show_result/<uuid:task_info_id>/', views.show_result, name='show_result'),
    path('delete_record/<uuid:record_id>/', views.delete_journal_record, name='delete_record'),
    path('open_view_access/<uuid:record_id>/', views.open_view_access, name='open_view_access'),
    path('close_view_access/<uuid:record_id>/', views.close_view_access, name='close_view_access')

]
