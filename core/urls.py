from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('jira-connector.urls')),
    path('jira-connector/', include('jira-connector.urls')),
    path('admin/', admin.site.urls),
]
