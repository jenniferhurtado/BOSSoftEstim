from django.contrib import admin
from django.urls import include, path

from .views import redirect_view

urlpatterns = [
    path('', redirect_view),
    path('jiracloud/', include('django.contrib.auth.urls')),
    path('jiracloud/', include('jiracloud.urls')),
    path('admin/', admin.site.urls),
]
