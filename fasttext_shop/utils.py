import os
import time

from loguru import logger


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
    with open("toutiao_data.txt", "r", encoding="utf-8") as f:
        datas = f.readlines()
    return [d.split(",")[:2] for d in datas]


def load_toutiao_test_datas():
    with open("toutiao_test_data.txt", "r", encoding="utf-8") as f:
        datas = f.readlines()
    return [d.split(",")[:2] for d in datas]


def del_stopwords(seg_list):
    """
    删除文本列表中的停用词
    """
    with open("stopwords.txt", "r", encoding="utf-8") as f:
        stopwords = f.readlines()
    stopwords = [word.strip() for word in stopwords]
    stopwords.append(" ")
    # print(stopwords)
    # 对分词结果进行过滤
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


if __name__ == "__main__":
    data = load_toutiao_datas()