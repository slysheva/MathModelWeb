from django.conf.urls import url

from . import views

app_name = 'webservice'
urlpatterns = [
    url(r'tasks/', views.list_tasks, name='tasks'),
    url('answer/', views.get_result, name='answer'),
    url('run_model/', views.solve_task, name='solving')
]
