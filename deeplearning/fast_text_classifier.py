import uuid
import subprocess

INPUT_PARAMETER = '-input'
OUTPUT = '-output'
EPOCH = '-epoch'
WORDNGRAMS = '-wordNgrams'
DIM = '-dim'
MINN = '-minn'
MAXN = '-maxn'
PRETRAINED = '-pretrainedVectors'


class FastTextClassifier:
    PATH_TO_FASTTEXT = "static/fasttext"
    rand = ""
    inputFileName = ""
    outputFileName = ""
    testFileName = ""

    def __init__(self):
        self.rand = str(uuid.uuid4())
        self.inputFileName = "issues_train.txt"
        self.outputFileName = "supervised_classifier_model"
        self.testFileName = "issues_test.txt"

    def fit(self, xtrain):
        outfile = open(self.inputFileName, mode="w", encoding="utf-8")
        for i in range(len(xtrain)):
            # line = "__label__" + str(ytrain[i]) + " " + xtrain[i]
            line = xtrain[i]
            outfile.write(line + '\n')
        outfile.close()
        mode = 'supervised'
        input_parameter = self.inputFileName
        output = self.outputFileName
        epoch = '1'
        word_n_grams = '4'
        dim = '10'
        minn = '4'
        maxn = '6'
        pretrained = './data/pretrained/pretrain_model.vec'
        subprocess.run([self.PATH_TO_FASTTEXT,
                        mode,
                        INPUT_PARAMETER, input_parameter,
                        OUTPUT, output,
                        EPOCH, epoch,
                        WORDNGRAMS, word_n_grams,
                        DIM, dim,
                        MINN, minn,
                        MAXN, maxn,
                        PRETRAINED, pretrained
                        ])

    def predict(self, xtest):
        # save test file
        outfile = open(self.testFileName, mode="w", encoding="utf-8")
        for i in range(len(xtest)):
            outfile.write(xtest[i] + '\n')
        outfile.close()
        # get predictions
        mode = 'predict'
        p1 = subprocess.Popen([self.PATH_TO_FASTTEXT, mode, self.outputFileName + ".bin", self.testFileName],
                              stdout=subprocess.PIPE)
        output_lines = p1.communicate()[0].decode("utf-8").split("\n")
        test_pred = [int(p.replace('__label__', '')) for p in output_lines if p != '']
        return test_pred
