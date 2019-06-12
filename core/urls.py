from django.contrib import admin
from django.urls import include, path

from .views import redirect_view

urlpatterns = [
    path('', redirect_view),
    path('jira-connector/', include('django.contrib.auth.urls')),
    path('jira-connector/', include('jira-connector.urls')),
    path('admin/', admin.site.urls),
]
