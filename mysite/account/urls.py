from django.conf.urls import url
from django.contrib import auth
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # post views
    # url(r'^login/$', views.user_login, name='login'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^logout-then-login/$', auth_views.logout_then_login, name='logout_then_login'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^password-change/$', auth_views.PasswordChangeView.as_view(), name='password_change'),
    url(r'^password-change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    url(r'^password-reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password-reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^password-reset/complete/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^register/$', views.register, name='register'),

]
