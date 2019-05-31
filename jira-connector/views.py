from django.http import HttpResponse
from .authentication import get_one_issue, get_all_issues


def index(request):
    return HttpResponse("Hello, world. You're at the jira index.")


def show__one_issue(request):
    issue = get_one_issue('FED-1')
    return HttpResponse(issue.key)


def show_all_issues(request):
    project_name = 'Front-end developers'
    issues = get_all_issues(project_name)
    response = project_name + ' issues: '
    for issue in issues:
        response = response + issue.key + ', '

    return HttpResponse(response)
