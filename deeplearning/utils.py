import pandas as pd

COLUMNS = ['issuekey', 'title', 'description', 'storypoint']


def invert_dictionary(dictionary):
    new_dict = {}
    for key in dictionary:
        value = dictionary[key]
        if value in new_dict:
            new_dict[value].append(key)
        else:
            new_dict[value] = [key]
    return new_dict


def build_training_dataframe(issues, custom_field):
    data = []
    for issue in issues:
        data.append([issue.key, issue.fields.summary, issue.fields.description, getattr(issue.fields, custom_field), ])

    df = pd.DataFrame(data, columns=COLUMNS)
    df.storypoint = df.storypoint.apply(lambda x: int(x))

    return df


def build_prediction_dataframe(issues):
    data = []
    for issue_key in issues:
        data.append([issue_key, issues[issue_key]['summary'], issues[issue_key]['description'], '', ])

    df = pd.DataFrame(data, columns=COLUMNS)
    return df
