# views.py
from django.shortcuts import redirect


def redirect_view(request):
    response = redirect('/jira-connector/login')
    return response
