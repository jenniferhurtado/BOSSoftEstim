from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('jira.urls')),
    path('jira/', include('jira.urls')),
    path('admin/', admin.site.urls),
]
