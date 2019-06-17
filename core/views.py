# views.py
from django.shortcuts import redirect


def redirect_view(request):
    response = redirect('/jiracloud/login')
    return response
