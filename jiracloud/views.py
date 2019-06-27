from django.http import HttpResponse
from django.template import loader

from .authentication import *


def index(request):
    template = loader.get_template('jiracloud/index.html')
    project_classified_issue_dict = {}
    project_unclassified_issue_dict = {}
    projects = get_all_projects()
    for project in projects:
        issues = get_all_issues(project.name)
        project_classified_issue_dict[project] = filter_classified_issues(issues)
        project_unclassified_issue_dict[project] = filter_unclassified_issues(issues)

    context = {
        'project_classified_issue_dict': project_classified_issue_dict,
        'project_unclassified_issue_dict': project_unclassified_issue_dict,
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
