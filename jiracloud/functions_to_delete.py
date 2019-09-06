import pandas as pd
from django.http import HttpResponse

from deeplearning.utils import COLUMNS
from .views import filter_classified_issues, filter_unclassified_issues, get_all_issues, get_all_projects, get_one_issue


def predict(user):
    projects = get_all_projects(user)
    custom_field = user.profile.storypoint_name_field
    issues_to_classify = []
    for project in projects:
        issues_to_classify = issues_to_classify + filter_unclassified_issues(get_all_issues(project, user), custom_field)

    return build_prediction_dataframe(issues_to_classify)


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
    custom_field = user.profile.storypoint_name_field
    for project in projects:
        issues_to_classify = issues_to_classify + filter_classified_issues(get_all_issues(project, user), custom_field)

    return build_training_dataframe(issues_to_classify, custom_field)


def build_training_dataframe(issues_to_train, custom_field):
    data = []
    for issue in issues_to_train:
        data.append([issue.key, issue.fields.summary, issue.fields.description, getattr(issue.fields, custom_field), ])

    df = pd.DataFrame(data, columns=COLUMNS)
    df.storypoint = df.storypoint.apply(lambda x: int(x))

    return df


def build_prediction_dataframe(issues_to_classify):
    data = []
    for issue in issues_to_classify:
        data.append([issue.key, issue.fields.summary, issue.fields.description, '', ])

    df = pd.DataFrame(data, columns=COLUMNS)
    return df
