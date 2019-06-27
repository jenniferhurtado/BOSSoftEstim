from jira import JIRA


def authenticate():
    REMOTE_HOST_NAME = 'https://softestim.atlassian.net'
    authTokens = ('jenniferhurtadopareja@gmail.com', None, 'RTEn84B6mDHlf6kpjuo170D0')
    username = authTokens[0]
    password = authTokens[2]

    jira_client = JIRA(basic_auth=(username, password), server=REMOTE_HOST_NAME)
    return jira_client


def get_one_issue(issue_key):
    jira_client = authenticate()
    issue = jira_client.issue(issue_key)
    return issue


def get_all_issues(project_name):
    jira_client = authenticate()
    issues = jira_client.search_issues('project="{}"'.format(project_name))
    return issues


def filter_classified_issues(issues):
    return [issue for issue in issues if issue.fields.customfield_10027 is not None]


def filter_unclassified_issues(issues):
    return [issue for issue in issues if issue.fields.customfield_10027 is None]


def get_all_projects():
    jira_client = authenticate()
    return jira_client.projects()
