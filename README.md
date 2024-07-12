FastText_Shop
===========

一个高效易用的短文本分类工具，基于简单包装[FastText](https://fasttext.cc/)项目,使用方法、灵感来自于TextGrocery并且和[TextGrocery](https://github.com/2shou/TextGrocery)基本相同。

FastText使用[结巴分词](https://github.com/fxsjy/jieba)作为默认的分词单元，以支持中文的短文本分类，停用词表使用[stopwords](https://github.com/goto456/stopwords/tree/master)。

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
# 训练
>> fs.train(train_src)

# 数据量足够大的时候可以使用fasttext自动超参数优化训练，训练号的模型会自动保存，不再需要 fs.save()
# FastText的自动调整功能允许您自动找到数据集的最佳超参数。找到最佳超参数对于构建高效模型至关重要，然而，手动搜索最佳超参数是困难的，参数是依赖的，每个参数的效果因数据集而异。
# automatic_optimization训练时间比较长，一般超过5分钟，请耐心等待。。。。
>> fs.automatic_optimization_train(train_src)
# 保存模型
>> fs.save()

# 加载模型（名字和保存的一样）
>> new_fs = FastText_Shop('sample')

>> new_fs.load()

# 预测,默认情况下，predict只返回一个标签：概率最高的那个。您也可以通过指定参数k来预测多个标签
>> new_fs.predict('考生必读：新托福写作考试评分标准')
['education'] [0.50007701]

# 清除训练过程中产生的文件，只保留模型
>> new_fs.clean()
# 清除模型和训练过程中产生的文件，注意：不保留模型
>> new_fs.clean_all()

```

### 使用使用今日头条中文新闻（文本）分类数据集测试：
下载地址：
https://github.com/ranvane/FastText_Shop/blob/main/toutiao/toutiao_data.txt

https://github.com/ranvane/FastText_Shop/blob/main/toutiao/toutiao_test_data.txt

```
# 单项测试
data = load_toutiao_datas(file_dir="/home/xxx/xxx")
fs = FastText_Shop("toutiao")
#先训练
# fs.train(data)
# fs.save()

fs.load()
test_datas = load_toutiao_test_datas(file_dir="/home/xxx/xxx")

for t in test_datas[100:2000]:
    labels, probabilities = fs.predict(t[1])

    print(f"{t[0].strip()} - {t[1].strip()} : {labels[0]}  ")

```
单项测试运行结果：
```
Building prefix dict from the default dictionary ...
Loading model from cache /tmp/jieba.cache
Loading model cost 0.539 seconds.
Prefix dict has been built successfully.
汽车 - 全国最高汽车限速是120公里每小时，为何汽车厂家不把最高速度设置为120公里？ : 汽车
汽车 - 上市3个月就降价，如今已降到8.79万，睿骋CC让长安操碎了心 : 汽车
汽车 - “四脚大怪兽”——福特f650 : 汽车
科技 - 手机只要打开这个功能，手机玩游戏就可以更加流畅，马上去试试 : 科技
科技 - 机器人竟完成了自我觉醒，还创造新物种将要接管地球，细思极恐 : 电竞游戏
科技 - 俞敏洪精彩解说马云 是如何成为首富的 : 科技
科技 - 马云励志演讲 未来三十年的变化 : 科技
科技 - 学编程有哪些好点的网站？ : 科技
科技 - 手机越来越卡，速速关闭微信这三个功能，可以节约大量内存空间！ : 科技
科技 - 关于世界首富-比尔盖茨的12个鲜为人知的秘密！ : 科技
科技 - 科技美学那岩 小米6X游戏后的温度和耗电测试 : 科技
科技 - 说好5年内不上市的小米，为何突然要上市，都递交了申请书？图啥 : 科技
科技 - 微信正在慢慢吞噬着周边的一切-腾讯有点过于强大了 : 科技
科技 - 跨世纪的思维，两个变性哲学家所拍的电影 : 娱乐
科技 - 手机用久了声音小，教你一个方法，就能让手机声音变大好几倍 : 科技
科技 - 国产手机又一黑马：欧洲市场3个月增速999%，市占率直追华为 : 财经
科技 - 原创微信表情第一弹（小小阿圆） : 电竞游戏
科技 - 腾讯游戏称霸全球利润超第二名近2倍，贡献最大的游戏是哪几款？ : 电竞游戏
军事 - 拒绝训练者会直接被处死？这个训练营靠什么存在 : 体育
军事 - 他三枪击毙日本军官，缴获天皇御赐武士刀，有人出20万求购被他拒绝 : 军事
军事 - 中国运20已经入列还需要伊尔76吗？中国这一妙招可谓精妙绝伦 : 军事
军事 - 十年前中国16万大军紧急调动，从空到陆全域机动只为挺进灾区 : 军事
军事 - 《穿越火线》GP神器也能超神 : 电竞游戏
```
### 测试模型在测试样本中取得的准确率
```
data = load_toutiao_datas(file_dir="/home/xxx/xxx")
fs = FastText_Shop("toutiao")
# print(data)

# fs.train(data)
# fs.save()
fs.load()
test_datas = load_toutiao_test_datas(file_dir="/home/xxx/xxx")
gen_fasttext_train_data(test_datas, "test_toutiao")
res = fs.model.test("test_toutiao.data")

print(f"样本数:{res[0]},精度:{res[1]},召回:{res[2]}")

```
测试运行结果：

```
Building prefix dict from the default dictionary ...
Loading model from cache /tmp/jieba.cache
Loading model cost 0.514 seconds.
Prefix dict has been built successfully.
2024-07-13 02:30:17.595 | INFO     | fasttext_shop.utils:gen_fasttext_train_data:121 - 生成fasttext格式训练数据文件成功：test_toutiao.data

样本数:87963,精度:0.8433204870229528,召回:0.8433204870229528
```
安装
----

    $ pip install -U FastText_Shop



FastText与NumPy不兼容>=2.0.0的BUG：
```
return labels, np.array(probs, copy=False)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: Unable to avoid copy while creating an array as requested.
If using `np.array(obj, copy=False)` replace it with `np.asarray(obj)` to allow a copy when needed (no behavior change in NumPy 1.x).
```
发生错误是因为FastText使用np.array和copy=False参数，根据迁移指南，NumPy2.0.0不支持该参数。这使得代码与较新版本的NumPy不兼容。

为了解决不兼容问题，更新了项目的需求，将NumPy的版本限制为小于2.0.0。具体来说，对requirements.txt文件进行了以下更改：

numpy>=1.26.4,<2.0.0


