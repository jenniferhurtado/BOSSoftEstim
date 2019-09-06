from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from deeplearning.main import prediction
from deeplearning.utils import build_prediction_dataframe
from .jira_connector import *


@login_required
def index(request):
    template = loader.get_template('jiracloud/index.html')
    project_classified_issue_dict = {}
    project_unclassified_issue_dict = {}
    user = request.user
    custom_field = user.profile.storypoint_name_field
    projects = get_all_projects(user)
    dict_unclassified = {}
    for project in projects:
        issues = get_all_issues(project.name, user)
        classified = filter_classified_issues(issues, custom_field)
        if classified:
            project_classified_issue_dict[project] = classified

        unclassified = filter_unclassified_issues(issues, custom_field)
        if unclassified:
            project_unclassified_issue_dict[project] = unclassified
            for issue in unclassified:
                dict_unclassified[issue.key] = {'summary': issue.fields.summary, 'description': issue.fields.description}

    request.session['list_unclassified'] = dict_unclassified

    context = {
        'project_classified_issue_dict': project_classified_issue_dict,
        'project_unclassified_issue_dict': project_unclassified_issue_dict,
        'custom_field': custom_field,
    }
    return HttpResponse(template.render(context, request))


@login_required
def classify_view(request):
    user = request.user
    custom_field = user.profile.storypoint_name_field
    df_test = build_prediction_dataframe(request.session['list_unclassified'])
    df_predicted = prediction(df_test)

    issues_dict = {}
    for i, row in df_predicted.iterrows():
        key = row.issuekey
        pred = row.prediction
        issue = get_one_issue(key, user)
        issue.update(fields={custom_field: pred})

        project = issue.fields.project
        if project in issues_dict:
            issues_dict[project].append((issue, pred))
        else:
            issues_dict[project] = [(issue, pred)]

    context = {'classified': issues_dict}
    template = loader.get_template('jiracloud/classify_template.html')
    return HttpResponse(template.render(context, request))
