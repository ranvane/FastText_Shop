import os
import time

import jieba
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer


def execute_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 执行共用时 {(end_time - start_time)} s.")
        return result

    return wrapper


class TextShop_sklearn:
    def __init__(self, model_name) -> None:
        self.model_name = model_name
        self.svm_model = None
        self.vectorizer = TfidfVectorizer()
        self.stopwords = self.load_stopwords()

    def load_stopwords(self):
        # 加载停用词
        with open("stopwords.txt", "r", encoding="utf-8") as f:
            stopwords = f.read().splitlines()
        return stopwords

    @execute_time
    def train(self, train_src):
        # 将数据转换为适合机器学习的格式
        X = []
        y = []
        for label, text in train_src:
            X.append(" ".join(jieba.cut(text)))
            y.append(label)
        # 使用TF-IDF将文本转换为特征向量

        X_train_transformed = self.vectorizer.fit_transform(X)

        # 使用SVM进行训练
        self.svm_model = svm.SVC()
        self.svm_model.fit(X_train_transformed, y)

    def predict_all(self, text):
        # 进行预测并打印结果
        if self.svm_model is None:
            raise Exception("This model is not usable because svm model is not given")

        X_test_transformed = self.vectorizer.transform(jieba.cut(text))

        predictions = self.svm_model.predict(X_test_transformed)

        print("Predictions: ", predictions)
        return predictions

    def predict(self, text):
        # 进行预测并打印结果
        if self.svm_model is None:
            raise Exception("This model is not usable because svm model is not given")

        X_test_transformed = self.vectorizer.transform(jieba.cut(text))

        predictions = self.svm_model.predict(X_test_transformed)

        print("Predictions: ", predictions[0].strip())
        return predictions[0].strip()

        # y, dec = predict_one(text, self.svm_model)
        # y = self.text_converter.get_class_name(int(y))
        # labels = [
        #     self.text_converter.get_class_name(k)
        #     for k in self.svm_model.label[: self.svm_model.nr_class]
        # ]
        # return GroceryPredictResult(
        #     predicted_y=y, dec_values=dec[: self.svm_model.nr_class], labels=labels
        # )

    def save(self, model_name, force=False):
        if self.svm_model is None:
            raise Exception(
                "This model can not be saved because svm model is not given."
            )
        if os.path.exists(model_name) and force:
            shutil.rmtree(model_name)
        try:
            os.mkdir(model_name)
        except OSError as e:
            raise OSError(e, "Please use force option to overwrite the existing files.")
        self.text_converter.save(model_name + "/converter")
        self.svm_model.save(model_name + "/learner", force)

        with open(model_name + "/id", "w") as fout:
            fout.write(self._hashcode)

    def load(self, model_name):
        try:
            with open(model_name + "/id", "r") as fin:
                self._hashcode = fin.readline().strip()
        except IOError:
            raise ValueError("The given model is invalid.")
        # self.text_converter.load(model_name + "/converter")
        # self.svm_model = LearnerModel(model_name + "/learner")


if __name__ == "__main__":
    data = [
        ("娱乐", "我喜欢看电影"),
        ("天气", "今天天气不错"),
        ("运动", "我喜欢打篮球"),
        ("水果", "我爱吃苹果"),
    ]
    # with open("toutiao_train_data.txt", "r", encoding="utf-8") as f:
    #     datas = f.readlines()
    # data = [(d[0], d[1]) for d in datas]

    shop = TextShop_sklearn("new")
    shop.train(data)
    shop.save()
    # shop.train(data)
    # shop.save()
    # # shop.predict("苹果好大")