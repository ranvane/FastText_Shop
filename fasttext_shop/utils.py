import os
import time
import jieba
from functools import lru_cache
from loguru import logger

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CUR_DIR = os.path.dirname(__file__)


def execute_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        # print(f"函数 {func.__name__} 执行共用时 {(end_time - start_time)} s.")
        logger.info(f"函数 {func.__name__} 执行共用时 {(end_time - start_time)} s.")
        return result

    return wrapper


def load_toutiao_datas():
    with open(
        os.path.join(BASE_DIR, "toutiao", "toutiao_data.txt"), "r", encoding="utf-8"
    ) as f:
        datas = f.readlines()
    return [d.split(",")[:2] for d in datas]


def load_toutiao_test_datas():
    with open(
        os.path.join(BASE_DIR, "toutiao", "toutiao_test_data.txt"),
        "r",
        encoding="utf-8",
    ) as f:

        datas = f.readlines()
    return [d.split(",")[:2] for d in datas]


@lru_cache(maxsize=None)
def load_stopwords():
    """
    加载停用词
    """
    with open(os.path.join(CUR_DIR, "stopwords.txt"), "r", encoding="utf-8") as f:
        stopwords = f.readlines()
    stopwords = [word.strip() for word in stopwords]
    stopwords.append(" ")
    return stopwords


def del_stopwords(seg_list):
    """
    删除文本列表中的停用词
    """

    stopwords = load_stopwords()
    filtered_seg_list = [seg for seg in seg_list if seg not in stopwords]
    return filtered_seg_list


def del_file(file_path):
    # 检查文件是否存在
    if os.path.isfile(file_path):
        # 如果文件存在，删除它
        os.remove(file_path)
        logger.info(f"删除：{file_path} ！")
    else:
        logger.info(f"{file_path} 文件不存在！或者已删除？")


def gen_fasttext_train_data(train_data, model_name, base_dir=None):
    """
    生成FastText格式的训练数据文件

    参数：
    train_data (list): 训练数据，列表中的元素是元组，元组的第一个元素是标签，第二个元素是文本内容
    model_name (str): 模型名称，用于生成文件名

    返回：
    str: 生成的FastText格式训练数据文件的文件名

    异常：
    如果在处理过程中发生任何错误，将记录错误日志并抛出异常
    """
    feature_text = []  # 初始化用于存储训练数据的列表
    try:
        if len(train_data) > 0:  # 检查训练数据是否为空
            logger.info("正在生成fasttext格式训练数据文件。。。")
            for label, text in train_data:  # 遍历训练数据中的每个样本
                words = jieba.lcut(
                    text.strip()
                )  # 使用jieba分词对文本进行分词，并转换为列表

                words = del_stopwords(words)  # 删除停用词
                # __label__ 标签 这是一段中文文本
                feature_text.append(f"__label__{label} {' '.join(words)}")
            if base_dir:
                _model_name = os.path.join(base_dir, f"{model_name}.data")
            else:
                _model_name = f"{model_name}.data"
            # 生成FastText格式训练数据文件
            with open(_model_name, "w", encoding="utf-8") as f:
                f.write("\n".join(feature_text))  # 将FastText格式向量写入文件
            logger.info(f"生成fasttext格式训练数据文件成功：{model_name}.data")
            return f"{model_name}.data"  # 返回生成的文件名

    except Exception as e:
        logger.error(
            f"utils gen_fasttext_train_data 错误消息:{model_name} - {e}"
        )  # 记录错误日志
        raise Exception(e)  # 抛出异常


if __name__ == "__main__":
    data = load_toutiao_datas()
