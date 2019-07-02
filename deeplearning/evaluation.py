import pandas as pd


def rebuild_kfold_sets(folds, k, i):

    training_set = None
    testing_set = None

    for j in range(k):
        if i == j:
            testing_set = folds[i]
        elif training_set is not None:
            training_set = pd.concat([training_set, folds[j]])
        else:
            training_set = folds[j]

    return training_set, testing_set


def rebuild_kfold_sets_no_test(folds, k):

    training_set = None

    for j in range(k):
        if training_set is not None:
            training_set = pd.concat([training_set, folds[j]])

        else:
            training_set = folds[j]

    return training_set
