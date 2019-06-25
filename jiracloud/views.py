from django.http import HttpResponse
from django.template import loader

from .authentication import get_all_issues, get_one_issue


def index(request):
    template = loader.get_template('jiracloud/index.html')
    issues = get_all_issues('Front-end developers')
    context = {
        'issues': issues,
    }
    return HttpResponse(template.render(context, request))


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
