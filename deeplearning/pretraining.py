import subprocess

import pandas as pd

from .prepare_data import DataPreparation
from .fast_text_classifier import FastTextClassifier
from .fast_text_classifier import INPUT_PARAMETER, OUTPUT, EPOCH, WORDNGRAMS, DIM, MINN, MAXN

pretrain_files = ['apache_pretrain.csv',
                  'jira_pretrain.csv',
                  'spring_pretrain.csv',
                  'talendforge_pretrain.csv',
                  'moodle_pretrain.csv',
                  'appcelerator_pretrain.csv',
                  'duraspace_pretrain.csv',
                  'mulesoft_pretrain.csv',
                  'lsstcorp_pretrain.csv']

pretrained = None

for file in pretrain_files:
    df_pretrain = pd.read_csv('./data/pretrained/' + file, usecols=['issuekey', 'title', 'description'])
    if pretrained is not None:
        pretrained = pd.concat([pretrained, df_pretrain])
    else:
        pretrained = df_pretrain

pretrained = pretrained.dropna(how='any')
pretrained['title_desc'] = (pretrained['title'].str.lower() + ' - ' +
                            pretrained['description'].str.lower()).apply(lambda x: DataPreparation.clean_data(str(x)))
outfile = open("./data/issues_pretrain.txt", mode="w", encoding="utf-8")
for line in pretrained.title_desc.values:
    outfile.write(line + '\n')
outfile.close()

mode = 'skipgram'
input_parameter = 'issues_pretrain.txt'
output = 'pretrain_model'
epoch = '50'
word_n_grams = '4'
dim = '300'
minn = '4'
maxn = '6'
lr = '0.05'
subprocess.run([FastTextClassifier.PATH_TO_FASTTEXT,
                mode,
                INPUT_PARAMETER, input_parameter,
                OUTPUT, output,
                EPOCH, epoch,
                WORDNGRAMS, word_n_grams,
                DIM, dim,
                MINN, minn,
                MAXN, maxn,
                '-lr', lr
                ])

