import os

import fasttext
import jieba
from loguru import logger

from .utils import del_stopwords, load_toutiao_datas, execute_time, del_file


class FastText_Shop():

    def __init__(self, model_name) -> None:
        self.model_name = model_name
        self.model = None
        self.train_data = []  # 传入的数据集

    @execute_time
    def train(self, train_data, model='skipgram'):
        '''

        @param train_data:
        @param model: skipgram，cbow，默认skipgram，cbow。
        @return:
        '''
        try:
            self.train_data = [sublist[:2] for sublist in train_data]  # 以防嵌套列表的长度过多

            self.gen_fasttext_train_data()

            self.model = fasttext.train_supervised(f"{self.model_name}.data", model=model)  # 是训练数据文件的路径

        except Exception as e:
            logger.error(f'train错误消息:{e}')
            raise Exception(e)

    def automatic_optimization_test(self, data=None, k=5):
        if self.model is None:
            self.load()

        valid_src = f"{self.model_name}_test.data"
        if os.path.isfile(valid_src):
            # 如果文件存在
            logger.info(f'automatic_optimization(样本数   精度   召回)-{self.model.test(valid_src)}')
        else:
            logger.info(f"{valid_src} 文件不存在")

    @execute_time
    def automatic_optimization_train(self, data):
        '''
        自动参数训练
        @return:
        '''
        logger.info(f'automatic_optimization训练时间比较长，一般超过5分钟，请耐心等待。。。。')
        input_src, valid_src = self.gen_automatic_optimization_train_data(data)

        self.model = fasttext.train_supervised(input=input_src, autotuneValidationFile=valid_src)
        self.save()

        logger.info(f'automatic_optimization测试信息:(样本数   精度   召回)-{self.model.test(valid_src)}')

    def gen_automatic_optimization_train_data(self, train_data):
        '''

        @param train_data:
        @return:
        '''
        logger.info(f'正在生成fasttext格式训练数据文件。。。')
        feature_text = []  # 训练数据
        try:
            if len(train_data) > 2:

                for label, text in train_data:
                    words = jieba.lcut(text.strip())  # 使用结巴分词对文本进行分词,并转换为列表
                    words = del_stopwords(words)  # 删除停用词
                    # __label__分类1 这是一段中文文本1
                    feature_text.append(f"__label__{label} {' '.join(words)}")

                write_list = "\n".join(feature_text)
                train_list = write_list[:int(len(write_list) / 4)]
                test_list = write_list[int(len(write_list) / 4) + 1:]

                # 生成fasttext格式训练数据文件
                with open(f"{self.model_name}.data", "w", encoding="utf-8") as f:
                    f.write(train_list)  # 将fasttext格式向量写入文件

                # 写入测试文件
                with open(f"{self.model_name}_test.data", "w", encoding="utf-8") as f:
                    f.write(test_list)  # 将fasttext格式向量写入文件
                return f"{self.model_name}.data", f"{self.model_name}_test.data"

        except Exception as e:
            logger.error(f'gen_automatic_optimization_train_data 错误消息:{e}')
            raise Exception(e)

    def gen_fasttext_train_data(self):

        feature_text = []  # 训练数据
        try:
            if len(self.train_data) > 0:

                for label, text in self.train_data:
                    words = jieba.lcut(text.strip())  # 使用结巴分词对文本进行分词,并转换为列表
                    words = del_stopwords(words)  # 删除停用词
                    # __label__分类1 这是一段中文文本1
                    feature_text.append(f"__label__{label} {' '.join(words)}")

                # 生成fasttext格式训练数据文件
                with open(f"{self.model_name}.data", "w", encoding="utf-8") as f:
                    f.write("\n".join(feature_text))  # 将fasttext格式向量写入文件
                return f"{self.model_name}.data"

        except Exception as e:
            logger.error(f'gen_fasttext_train_data 错误消息:{e}')
            raise Exception(e)

    def predict(self, obj, k=1):
        '''

        @param obj:预测的文本对象
        @return: 默认情况下，predict只返回一个标签：概率最高的那个。您也可以通过指定参数k来预测多个标签：
        '''
        seg_list = jieba.cut(obj, cut_all=False)
        seg_list = " ".join(seg_list)
        label = self.model.predict(seg_list, k=k)  # 获取预测标签
        return label

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
        '''
        删除训练过程中产生的各类数据，只保留模型对象
        @return:
        '''
        file_list = [f"{self.model_name}.data", f"{self.model_name}_test.data"]
        for file in file_list:
            del_file(file)

    def clean_all(self):
        file_list = [f"{self.model_name}.model", f"{self.model_name}.data", f"{self.model_name}_test.data",
                     f"{self.model_name}_test.data"]
        for file in file_list:
            del_file(file)


if __name__ == "__main__":
    datas = load_toutiao_datas()
    fs = FastText_Shop('toutiao')
    # fs.load()
    # fs.automatic_optimization_train(datas)
    fs.automatic_optimization_test()
    fs.cleanall()
    # # fs.train(data)
    # # fs.save()

    # print(fs.predict('“照片是假的、视频是P的”，黑海舰队司令的死活居然还有争议？'))