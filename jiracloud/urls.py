from django.urls import path

from . import views

urlpatterns = [
    #path('', views.show_all_issues, name='show_all_issues'),
    path('', views.index, name='index'),
    path('classify_view', views.classify_view, name='classify_view'),
]
