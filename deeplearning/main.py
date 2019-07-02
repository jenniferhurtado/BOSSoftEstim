from .evaluation import *
from .fast_text_classifier import FastTextClassifier
from .prepare_data import DataPreparation


def predict_and_accuracy(df):
    # K-folds cross validation
    # K=5 or K=10 are generally used.
    # Note that the overall execution time increases linearly with k
    k = 5

    # Define the classes for the classifier
    classes = ['0', '1', '2']

    # Make Dataset random before start
    df_rand = df.sample(df.storypoint.count(), random_state=99)

    # Number of examples in each fold
    fsamples = int(df_rand.storypoint.count() / k)

    # Fill folds (obs: last folder could contain less than fsamples datapoints)
    folds = list()
    for i in range(k):
        folds.append(df_rand.iloc[i * fsamples: (i + 1) * fsamples])

    # Init
    sum_overall_accuracy = 0
    total_predictions = 0

    # Repeat k times and average results
    for i in range(k):

        # 1 - Build new training and testing set for iteration i
        training_set, testing_set = rebuild_kfold_sets(folds, k, i)
        y_true = testing_set.storypoint.tolist()

        # 2 - Oversample (ONLY TRAINING DATA)
        # X_resampled, y_resampled = DataPreparation.simple_over_sample(training_set.label_title_desc.values.tolist(),
        #                                                              training_set.storypoint.values.tolist())
        # 2 - Downsample (ONLY TRAINING DATA)
        # TODO: why are we using y_resampled for?
        X_resampled, y_resampled = DataPreparation.simple_down_sample(training_set)

        # 3 - train
        clf = FastTextClassifier()
        clf.fit(X_resampled)

        # 4 - Predict
        y_pred = clf.predict(testing_set.label_title_desc.values.tolist())

        # 3 - Update Overall Accuracy
        for num_pred in range(len(y_pred)):
            if y_pred[num_pred] == y_true[num_pred]:
                sum_overall_accuracy += 1
            total_predictions += 1


def prediction(df_train, df_test):
    # K-folds cross validation
    k = 3

    # Make Dataset random before start
    df_rand = df_train.sample(df_train.storypoint.count(), random_state=99)

    # Number of examples in each fold
    samples = int(df_rand.storypoint.count() / k)

    # Fill folds (obs: last folder could contain less than samples datapoints)
    folds = list()
    for i in range(k):
        folds.append(df_rand.iloc[i * samples: (i + 1) * samples])

    # Repeat k times and average results
    for i in range(k):

        # 1 - Build new training
        training_set = rebuild_kfold_sets_no_test(folds, k)

        x_resampled, y_resampled = DataPreparation(training_set).simple_down_sample()

        # 3 - Train
        clf = FastTextClassifier()
        clf.fit(x_resampled)

        # 4 - Predict
        testing_set = DataPreparation(df_test).df
        y_pred = clf.predict(testing_set.label_title_desc.values.tolist())
        testing_set['prediction'] = y_pred

        return testing_set
