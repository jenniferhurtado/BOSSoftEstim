import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from deeplearning.main import prediction
from deeplearning.prepare_data import COLUMNS
from .jira_connector import *


@login_required
def index(request):
    template = loader.get_template('jiracloud/index.html')
    project_classified_issue_dict = {}
    project_unclassified_issue_dict = {}
    user = request.user
    projects = get_all_projects(user)
    dict_unclassified = {}
    for project in projects:
        issues = get_all_issues(project.name, user)
        classified = filter_classified_issues(issues)
        if classified:
            project_classified_issue_dict[project] = classified

        unclassified = filter_unclassified_issues(issues)
        if unclassified:
            project_unclassified_issue_dict[project] = unclassified
            for issue in unclassified:
                dict_unclassified[issue.key] = {'summary': issue.fields.summary, 'description': issue.fields.description}

    request.session['list_unclassified'] = dict_unclassified

    context = {
        'project_classified_issue_dict': project_classified_issue_dict,
        'project_unclassified_issue_dict': project_unclassified_issue_dict,
    }
    return HttpResponse(template.render(context, request))


@login_required
def classify_view(request):
    user = request.user
    df_test = build_prediction_dataframe_from_dict(request.session['list_unclassified'])
    df_predicted = prediction(df_test)

    issues_dict = {}
    for i, row in df_predicted.iterrows():
        key = row.issuekey
        pred = row.prediction
        issue = get_one_issue(key, user)
        issue.update(fields={'customfield_10027': pred})

        project = issue.fields.project
        if project in issues_dict:
            issues_dict[project].append((issue, pred))
        else:
            issues_dict[project] = [(issue, pred)]

    context = {'classified': issues_dict}
    template = loader.get_template('jiracloud/classify_template.html')
    return HttpResponse(template.render(context, request))


def build_prediction_dataframe_from_dict(issues_to_classify):
    data = []
    for issue_key in issues_to_classify:
        data.append([issue_key, issues_to_classify[issue_key]['summary'], issues_to_classify[issue_key]['description'], '', ])

    df = pd.DataFrame(data, columns=COLUMNS)
    return df


