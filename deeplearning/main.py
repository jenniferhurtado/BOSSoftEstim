from .fast_text_classifier import FastTextClassifier
from .prepare_data import DataPreparation


def fit(df_train):
    # Make Dataset random before start
    df_rand = df_train.sample(df_train.storypoint.count(), random_state=99)

    x_resampled, _ = DataPreparation(df_rand).simple_down_sample()

    # Train
    clf = FastTextClassifier()
    clf.fit(x_resampled)


def prediction(df_test):
    clf = FastTextClassifier()

    # Predict
    testing_set = DataPreparation(df_test).df
    y_pred = clf.predict(testing_set.label_title_desc.values.tolist())
    print(testing_set)
    print(y_pred)

    testing_set['prediction'] = y_pred

    return testing_set
