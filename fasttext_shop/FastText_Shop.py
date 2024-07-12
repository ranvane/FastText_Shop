import os

import fasttext
import jieba
from loguru import logger

from .utils import (
    del_stopwords,
    load_toutiao_datas,
    execute_time,
    del_file,
    gen_fasttext_train_data,
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CUR_DIR = os.path.dirname(__file__)


class FastText_Shop:

    def __init__(self, model_name) -> None:
        self.model_name = model_name
        self.model = None
        self.train_data = []  # 传入的数据集

    @execute_time
    def train(self, train_data):
        """

        @param train_data:
        @param model:
        @return:
        """
        try:
            self.train_data = [
                sublist[:2] for sublist in train_data
            ]  # 以防嵌套列表的长度过多

            self.gen_fasttext_train_data()

            self.model = fasttext.train_supervised(
                input=f"{self.model_name}.data"
            )  # input是训练数据文件的路径

        except Exception as e:
            logger.error(f"train错误消息:{e}")
            raise Exception(e)

    @execute_time
    def automatic_optimization_train(self, data):
        """
        自动参数训练

        这个函数的目的是使用FastText模型进行自动参数训练。它接受一个数据集作为输入，并生成用于训练和验证的数据源。训练过程完成后，它将保存模型，并打印出测试信息，包括样本数、精度和召回率。

        参数:
        data (list): 训练数据，列表中的每个元素是一个元组，包含标签和文本内容。

        返回:
        None

        异常:
        如果在处理过程中发生任何错误，将记录错误日志并抛出异常。
        """
        logger.info(
            "automatic_optimization训练时间比较长，一般超过5分钟，请耐心等待。。。。"
        )
        # 获取训练数据
        input_src, valid_src = self.gen_automatic_optimization_train_data(data)
        # 开始训练
        self.model = fasttext.train_supervised(
            input=input_src, autotuneValidationFile=valid_src
        )
        # 保存模型
        self.save()

        logger.info(
            f"automatic_optimization测试信息:(样本数   精度   召回)-{self.model.test(valid_src)}"
        )

    def gen_automatic_optimization_train_data(self, train_data):
        """
        生成FastText格式的训练数据文件，用于自动优化训练

        参数:
        train_data (list): 训练数据，列表中的元素是元组，元组的第一个元素是标签，第二个元素是文本内容

        返回:
        tuple: 包含两个文件名的元组，第一个文件名为训练数据文件，第二个文件名为测试数据文件

        异常:
        如果在处理过程中发生任何错误，将记录错误日志并抛出异常
        """

        try:
            if len(train_data) > 4:

                train_list = train_data[: int(len(train_data) / 4)]
                test_list = train_data[int(len(train_data) / 4) + 1 :]

                # 生成fasttext格式训练数据文件
                gen_fasttext_train_data(train_list, self.model_name)

                # 写入测试文件
                gen_fasttext_train_data(test_list, f"{self.model_name}_test")

                return f"{self.model_name}.data", f"{self.model_name}_test.data"

        except Exception as e:
            logger.error(f"gen_automatic_optimization_train_data 错误消息:{e}")

    def gen_fasttext_train_data(self):

        try:
            if len(self.train_data) > 0:

                return gen_fasttext_train_data(self.train_data, self.model_name)

        except Exception as e:
            logger.error(f"gen_fasttext_train_data 错误消息:{e}")
            raise Exception(e)

    def predict(self, obj, k=1):
        """

        @param obj:预测的文本对象
        @return: 默认情况下，predict只返回一个标签：概率最高的那个。您也可以通过指定参数k来预测多个标签：
        """
        seg_list = jieba.cut(obj.strip(), cut_all=False)

        seg_str = "  ".join(del_stopwords(seg_list))
        # print(seg_str)

        labels, probabilities = self.model.predict(seg_str, k=k)  # 获取预测标签

        labels = [label.replace("__label__", "") for label in labels]

        return labels, probabilities

    def save(self, force=False):
        """
        保存模型
        """
        if self.model is None:
            raise Exception("模型为空，请先训练模型！")
        try:
            # 保存模型对象到文件
            self.model.save_model(f"{self.model_name}.model")

        except Exception as e:
            raise Exception(f"保存FastText模型失败：{e}")

    def load(self):
        """
        加载模型
        """
        try:
            # 加载模型对象到文件
            self.model = fasttext.load_model(f"{self.model_name}.model")

        except Exception as e:
            logger(f"加载FastText模型失败：{e}")
            # raise Exception(f"加载FastText模型失败：{e}")

    def clean(self):
        """
        删除训练过程中产生的各类数据，只保留模型对象
        @return:
        """
        file_list = [f"{self.model_name}.data", f"{self.model_name}_test.data"]
        for file in file_list:
            del_file(file)

    def clean_all(self):
        file_list = [
            f"{self.model_name}.model",
            f"{self.model_name}.data",
            f"{self.model_name}_test.data",
            f"{self.model_name}_test.data",
        ]
        for file in file_list:
            del_file(file)


if __name__ == "__main__":
    datas = load_toutiao_datas()
    fs = FastText_Shop("toutiao")
    # fs.load()
    # fs.automatic_optimization_train(datas)
    fs.automatic_optimization_test()
    fs.cleanall()
    # # fs.train(data)
    # # fs.save()

    # print(fs.predict('“照片是假的、视频是P的”，黑海舰队司令的死活居然还有争议？'))
