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
    for project in projects:
        issues = get_all_issues(project.name, user)
        classified = filter_classified_issues(issues)
        if classified:
            project_classified_issue_dict[project] = classified

        unclassified = filter_unclassified_issues(issues)
        if unclassified:
            project_unclassified_issue_dict[project] = unclassified

    context = {
        'project_classified_issue_dict': project_classified_issue_dict,
        'project_unclassified_issue_dict': project_unclassified_issue_dict,
    }
    return HttpResponse(template.render(context, request))


@login_required
def classify_view(request):
    user = request.user
    df_test = predict(user)
    df_train = classify(user)
    df_predicted = prediction(df_train, df_test)

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


def show__one_issue(request):
    user = request.user
    issue = get_one_issue('FED-1', user)
    return HttpResponse(issue.key)


def show_all_issues(request):
    user = request.user
    project_name = 'Front-end developers'
    issues = get_all_issues(project_name, user)
    response = project_name + ' issues: '
    for issue in issues:
        response = response + issue.key + ', '

    return HttpResponse(response)


def classify(user):
    projects = get_all_projects(user)
    issues_to_classify = []
    for project in projects:
        issues_to_classify = issues_to_classify + filter_classified_issues(get_all_issues(project, user))

    return build_training_dataframe(issues_to_classify)


def predict(user):
    projects = get_all_projects(user)
    issues_to_classify = []
    for project in projects:
        issues_to_classify = issues_to_classify + filter_unclassified_issues(get_all_issues(project, user))

    return build_prediction_dataframe(issues_to_classify)


def build_prediction_dataframe(issues_to_classify):
    data = []
    for issue in issues_to_classify:
        data.append([issue.key, issue.fields.summary, issue.fields.description, '', ])

    df = pd.DataFrame(data, columns=COLUMNS)
    return df


def build_training_dataframe(issues_to_train):
    data = []
    for issue in issues_to_train:
        data.append([issue.key, issue.fields.summary, issue.fields.description, issue.fields.customfield_10027, ])

    df = pd.DataFrame(data, columns=COLUMNS)
    df.storypoint = df.storypoint.apply(lambda x: int(x))

    return df
