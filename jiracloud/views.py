import pandas as pd
from django.http import HttpResponse
from django.template import loader

from .authentication import *
from deeplearning.main import prediction
from deeplearning.prepare_data import COLUMNS


def index(request):
    template = loader.get_template('jiracloud/index.html')
    project_classified_issue_dict = {}
    project_unclassified_issue_dict = {}
    projects = get_all_projects()
    for project in projects:
        issues = get_all_issues(project.name)
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


def classify_view(request):
    df_test = predict()
    df_train = classify()
    df_predicted = prediction(df_train, df_test)

    issue_list = []
    for i, row in df_predicted.iterrows():
        key = row.issuekey
        print(key)
        pred = row.prediction
        issue = get_one_issue(key)
        issue_list.append((issue, pred))

    print(df_predicted)
    print(issue_list)
    context = {'classified': {'BED': issue_list}}
    template = loader.get_template('jiracloud/classify_template.html')
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


def classify():
    projects = get_all_projects()
    issues_to_classify = []
    for project in projects:
        issues_to_classify = issues_to_classify + filter_classified_issues(get_all_issues(project))

    return build_training_dataframe(issues_to_classify)


def predict():
    projects = get_all_projects()
    issues_to_classify = []
    for project in projects:
        issues_to_classify = issues_to_classify + filter_unclassified_issues(get_all_issues(project))

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
