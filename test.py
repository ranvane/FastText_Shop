from fasttext_shop import FastText_Shop
from fasttext_shop.utils import (
    load_toutiao_datas,
    load_toutiao_test_datas,
    execute_time,
    gen_fasttext_train_data,
)
import pytest


# 测试正常情况
def test_gen_fasttext_train_data_normal():
    train_data = [("label1", "这是一段中文文本"), ("label2", "这是另一段中文文本")]
    model_name = "test_model"
    result = gen_fasttext_train_data(train_data, model_name)
    assert os.path.exists(f"{model_name}.data")


# 测试训练数据为空
def test_gen_fasttext_train_data_empty_train_data():
    train_data = []
    model_name = "test_model"
    with pytest.raises(Exception):
        gen_fasttext_train_data(train_data, model_name)


# 测试异常情况
def test_gen_fasttext_train_data_exception():
    train_data = [("label1", "")]
    model_name = "test_model"
    with pytest.raises(Exception):
        gen_fasttext_train_data(train_data, model_name)


def test1():
    fs = FastText_Shop("sample")
    train_src = [
        ("education", "名师指导托福语法技巧：名词的复数形式"),
        ("education", "中国高考成绩海外认可 是“狼来了”吗？"),
        ("sports", "图文：法网孟菲尔斯苦战进16强 孟菲尔斯怒吼"),
        ("sports", "四川丹棱举行全国长距登山挑战赛 近万人参与"),
    ]
    fs.train(train_src)
    fs.save()
    new_fs = FastText_Shop("sample")
    new_fs.load()
    labels, probabilities = new_fs.predict("松江女排小将在这场全市青少年比赛上收获银牌")
    print(labels, probabilities)
    new_fs.clean_all()  # 清理数据


def test_toutiao_1():

    data = load_toutiao_datas()
    test_datas = load_toutiao_test_datas()
    fs = FastText_Shop("toutiao")

    # fs.train(data)
    # fs.save()
    fs.load()

    for t in test_datas[100:2000]:
        labels, probabilities = fs.predict(t[1])

        print(f"{t[0].strip()} - {t[1].strip()} : {labels[0]}  ")


def test_toutiao_2():

    data = load_toutiao_datas()
    fs = FastText_Shop("toutiao")

    # fs.train(data)
    # fs.save()
    fs.load()
    test_datas = load_toutiao_test_datas()
    gen_fasttext_train_data(test_datas, "test_toutiao")
    res = fs.model.test("test_toutiao.data")
    print(res)
    print(f"样本数:{res[0]},精度:{res[1]},召回:{res[2]}")


def toutiao_automatic_optimization_train():
    data = load_toutiao_datas()
    test_datas = load_toutiao_test_datas()
    fs = FastText_Shop("toutiao")
    fs.automatic_optimization_train(test_datas)


def test_clean():
    model = ["sample", "toutiao", "test_toutiao"]
    for m in model:
        fs = FastText_Shop(m)
        fs.clean_all()


if __name__ == "__main__":
    test1()
