FastText_Shop
===========

一个高效易用的短文本分类工具，基于简单包装[FastText](https://fasttext.cc/)项目
,使用方法、灵感来自于TextGrocery并且和[TextGrocery](https://github.com/2shou/TextGrocery)基本相同。

FastText使用[结巴分词](https://github.com/fxsjy/jieba)
作为默认的分词单元，以支持中文的短文本分类，停用词表使用[stopwords](https://github.com/goto456/stopwords/tree/master)。

性能
----
使用今日头条中文新闻（文本）分类数据集 [toutiao-text-classfication-dataset](https://github.com/BenDerPan/toutiao-text-classfication-dataset)

    数据规模：
    
    共382688条，分布于15个分类中。
    
    采集时间： 2018年05月

分类器：automatic_optimization ，准确率：83% ，计算时间：超过5分钟（fasttext automatic_optimization 特性）


示例代码
-------

```python
>> from fasttext_shop import FastText_Shop
# 新开张一个fasttext_shop，别忘了取名！
>> fs = FastText_Shop('sample')
# 训练文本可以用列表传入
>> train_src = [
    ('education', '名师指导托福语法技巧：名词的复数形式'),
    ('education', '中国高考成绩海外认可 是“狼来了”吗？'),
    ('sports', '图文：法网孟菲尔斯苦战进16强 孟菲尔斯怒吼'),
    ('sports', '四川丹棱举行全国长距登山挑战赛 近万人参与')
]
# 训练，可选参数model='skipgram'或者model='cbow'，默认skipgram。
>> fs.train(train_src, model='skipgram')

# 保存模型[use_poetry_upload2pypi  .md](..%2Franvane_hugo_blog%2Fcontent%2Fpost%2F%C8%D5%B3%A3%2Fuse_poetry_upload2pypi%20%20.md)
>> fs.save()

# 加载模型（名字和保存的一样）
>> new_fs = FastText_Shop('sample')

>> new_fs.load()

# 预测,默认情况下，predict只返回一个标签：概率最高的那个。您也可以通过指定参数k来预测多个标签
>> new_fs.predict('考生必读：新托福写作考试评分标准')
education

# 使用fasttext自动超参数优化训练，训练号的模型会自动保存，不再需要 new_fs.save()
# FastText的自动调整功能允许您自动找到数据集的最佳超参数。找到最佳超参数对于构建高效模型至关重要，然而，手动搜索最佳超参数是困难的，参数是依赖的，每个参数的效果因数据集而异。
# automatic_optimization训练时间比较长，一般超过5分钟，请耐心等待。。。。
>> new_fs.automatic_optimization_train(train_src)

# 预测
>> new_fs.predict('考生必读：新托福写作考试评分标准')
education

# 清除训练过程中产生的文件，只保留模型
>> new_fs.clean()
# 清除模型和训练过程中产生的文件，注意：不保留模型
>> new_fs.clean_all()


```

安装
----

    $ pip install FastText_Shop

> 如果Windows下安装失败，请在http://www.lfd.uci.edu/~gohlke/pythonlibs/  下载fasttext的包。