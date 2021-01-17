from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^webservice/', include('webservice.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('account.urls')),

]
