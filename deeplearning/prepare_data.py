from collections import Counter

import pandas as pd
from nltk.corpus import stopwords
from .utils import invert_dictionary

# Define some known html tokens that appear in the data to be removed later
HTML_TOKENS = ['{html}', '<div>', '<pre>', '<p>', '</div>', '</pre>', '</p>']
COLUMNS = ['issuekey', 'title', 'description', 'storypoint']


class DataPreparationFromFile:
    def __init__(self, path, columns):
        """
        path = 'data/datasets/appceleratorstudio.csv'
        columns = ['issuekey', 'title', 'description', 'storypoint']
        :param path:
        :param columns:
        """
        # Read the data
        df = pd.read_csv(path, usecols=columns)

        # Check for null or empty values in the dataset
        # df.isnull().sum() TODO: Add this information in the logs

        # remove any entry that is not complete
        df = df.dropna(how='any')

        # Visualisation
        # df.head() TODO: Add this information in the logs
        # df.storypoint.describe() TODO: Add this information in the logs

        # df.groupby('storypoint').size() TODO: Add this information in the logs

        df.loc[df.storypoint <= 2, 'storypoint'] = 0  # small
        df.loc[(df.storypoint > 2) & (df.storypoint <= 5), 'storypoint'] = 1  # medium
        df.loc[df.storypoint > 5, 'storypoint'] = 2  # big

        # df.groupby('storypoint').size() TODO: Add this information in the logs

        # Concatenation of the title and description columns, in lower case
        df['title_desc'] = df['title'].str.lower() + ' - ' + df['description'].str.lower()

        # Contains the number of points with a specific prefix for it to
        # be recognized as the labeled information (class), in lower case
        df['label_title_desc'] = \
            df['storypoint'].apply(lambda x: self.format_fast_text_classifier(x)) + \
            df['title_desc'].apply(lambda x: self.clean_data(str(x)))

        # Since we were removing some empty entries, we will re-index
        # our dataset to fix it and have continuous indices again
        df = df.reset_index(drop=True)

        self.df = df

    def get_data_frame(self):
        return self.df

    # Clean operation
    # Remove english stop words and html tokens
    @staticmethod
    def clean_data(text):
        result = ''

        for w in HTML_TOKENS:
            text = text.replace(w, '')

        text_words = text.split()

        resultwords = [word for word in text_words if word not in stopwords.words('english')]

        if len(resultwords) > 0:
            result = ' '.join(resultwords)
        else:
            print('Empty transformation for: ' + text)

        return result

    @staticmethod
    def format_fast_text_classifier(label):
        return "__label__" + str(label) + " "

    @staticmethod
    def simple_over_sample(_xtrain, _ytrain):
        xtrain = list(_xtrain)
        ytrain = list(_ytrain)

        samples_counter = Counter(ytrain)
        max_samples = sorted(samples_counter.values(), reverse=True)[0]
        for sc in samples_counter:
            init_samples = samples_counter[sc]
            samples_to_add = max_samples - init_samples
            if samples_to_add > 0:
                # collect indices to oversample for the current class
                index = list()
                for i in range(len(ytrain)):
                    if ytrain[i] == sc:
                        index.append(i)
                # select samples to copy for the current class
                copy_from = [xtrain[i] for i in index]
                index_copy = 0
                for i in range(samples_to_add):
                    xtrain.append(copy_from[index_copy % len(copy_from)])
                    ytrain.append(sc)
                    index_copy += 1
        return xtrain, ytrain

    @staticmethod
    def simple_down_sample(df):
        storypoints_occurrences_dict = df.groupby('storypoint').size().to_dict()
        occurrences_storypoints_dict = invert_dictionary(storypoints_occurrences_dict)
        min_samples = min(occurrences_storypoints_dict)
        new_dataframe = pd.DataFrame(columns=df.columns.to_list())
        for size in occurrences_storypoints_dict:
            if size > min_samples:
                for storypoint in occurrences_storypoints_dict[size]:
                    rows_by_storypoint = df.loc[df['storypoint'] == storypoint]
                    rows_by_storypoint = rows_by_storypoint.sample(min_samples)
                    new_dataframe = pd.concat([new_dataframe, rows_by_storypoint])

        new_dataframe.reset_index(drop=True)
        return new_dataframe.label_title_desc.values.tolist(), new_dataframe.storypoint.values.tolist()


class DataPreparation:
    def __init__(self, df):

        # Remove any entry that is not complete
        df = df.dropna(how='any')

        # Concatenation of the title and description columns, in lower case
        df['title_desc'] = df['title'].str.lower() + ' - ' + df['description'].str.lower()

        # Contains the number of points with a specific prefix for it to
        # be recognized as the labeled information (class), in lower case
        df['label_title_desc'] = \
            df['storypoint'].apply(lambda x: self.format_fast_text_classifier(x)) + \
            df['title_desc'].apply(lambda x: self.clean_data(str(x)))

        # Since we were removing some empty entries, we will re-index
        # our dataset to fix it and have continuous indices again
        df = df.reset_index(drop=True)

        self.df = df

    def get_data_frame(self):
        return self.df

    # Clean operation
    # Remove english stop words and html tokens
    @staticmethod
    def clean_data(text):
        result = ''

        for w in HTML_TOKENS:
            text = text.replace(w, '')

        text_words = text.split()

        result_words = [word for word in text_words if word not in stopwords.words('english')]

        if len(result_words) > 0:
            result = ' '.join(result_words)
        else:
            print('Empty transformation for: ' + text)

        return result

    @staticmethod
    def format_fast_text_classifier(label):
        return "__label__" + str(label) + " "

    @staticmethod
    def simple_over_sample(_xtrain, _ytrain):
        xtrain = list(_xtrain)
        ytrain = list(_ytrain)

        samples_counter = Counter(ytrain)
        max_samples = sorted(samples_counter.values(), reverse=True)[0]
        for sc in samples_counter:
            init_samples = samples_counter[sc]
            samples_to_add = max_samples - init_samples
            if samples_to_add > 0:
                # collect indices to oversample for the current class
                index = list()
                for i in range(len(ytrain)):
                    if ytrain[i] == sc:
                        index.append(i)
                # select samples to copy for the current class
                copy_from = [xtrain[i] for i in index]
                index_copy = 0
                for i in range(samples_to_add):
                    xtrain.append(copy_from[index_copy % len(copy_from)])
                    ytrain.append(sc)
                    index_copy += 1
        return xtrain, ytrain

    def simple_down_sample(self):
        df = self.df
        storypoints_occurrences_dict = df.groupby('storypoint').size().to_dict()
        occurrences_storypoints_dict = invert_dictionary(storypoints_occurrences_dict)
        min_samples = min(occurrences_storypoints_dict)
        new_dataframe = pd.DataFrame(columns=df.columns.to_list())
        for size in occurrences_storypoints_dict:
            if size >= min_samples:
                for storypoint in occurrences_storypoints_dict[size]:
                    rows_by_storypoint = df.loc[df['storypoint'] == storypoint]
                    rows_by_storypoint = rows_by_storypoint.sample(min_samples)
                    new_dataframe = pd.concat([new_dataframe, rows_by_storypoint])

        new_dataframe.reset_index(drop=True)
        return new_dataframe.label_title_desc.values.tolist(), new_dataframe.storypoint.values.tolist()
