from jira import JIRA

from deeplearning.utils import build_training_dataframe


def authenticate(user):
    profile = user.profile
    #REMOTE_HOST_NAME = 'https://softestim.atlassian.net'
    #authTokens = ('jenniferhurtadopareja@gmail.com', None, 'RTEn84B6mDHlf6kpjuo170D0')

    remote_host_name = profile.remote_host_name
    username = profile.jira_username
    password = profile.jira_password

    jira_client = JIRA(basic_auth=(username, password), server=remote_host_name)
    return jira_client


def get_one_issue(issue_key, user):
    jira_client = authenticate(user)
    issue = jira_client.issue(issue_key)
    return issue


def get_all_issues(project_name, user):
    jira_client = authenticate(user)
    issues = jira_client.search_issues('project="{}"'.format(project_name))
    return issues


def filter_classified_issues(issues):
    return [issue for issue in issues if issue.fields.customfield_10027 is not None]


def filter_unclassified_issues(issues):
    return [issue for issue in issues if issue.fields.customfield_10027 is None]


def get_all_projects(user):
    jira_client = authenticate(user)
    return jira_client.projects()


def get_training_dataframe(user):
    projects = get_all_projects(user)
    issues_to_classify = []
    for project in projects:
        issues_to_classify = issues_to_classify + filter_classified_issues(get_all_issues(project, user))

    return build_training_dataframe(issues_to_classify)
