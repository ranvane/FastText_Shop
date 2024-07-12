import os

CUR_DIR = os.path.dirname(__file__)
g_cnns = [
    [100, "民生故事", "news_story"],
    [101, "文化", "news_culture"],
    [102, "娱乐", "news_entertainment"],
    [103, "体育", "news_sports"],
    [104, "财经", "news_finance"],
    [105, "时政", "nineteenth"],
    [106, "房产", "news_house"],
    [107, "汽车", "news_car"],
    [108, "教育", "news_edu"],
    [109, "科技", "news_tech"],
    [110, "军事", "news_military"],
    [111, "宗教"],
    [112, "旅游", "news_travel"],
    [113, "国际", "news_world"],
    [114, "证券", "stock"],
    [115, "农业", "news_agriculture"],
    [116, "电竞游戏", "news_game"],
]
datas = []
with open(os.path.join(CUR_DIR, "toutiao_cat_data.txt"), "r", encoding="utf-8") as f:
    datas = f.readlines()
print(g_cnns[0][0], g_cnns[0][1])

new_datas = [sublist.split("_!_") for sublist in datas]
new_datas = [(sublist[1], sublist[3]) for sublist in new_datas]
for g in g_cnns:
    # new_datas = [s.replace(f"_!_{g[0]}_!_", f"_!_{g[1]}_!_") for s in datas]
    new_datas = [
        (sublist[0].replace(str(g[0]), g[1]), sublist[1]) for sublist in new_datas
    ]
with open(os.path.join(CUR_DIR, "toutiao_data.txt"), "w", encoding="utf-8") as f:
    for tup in new_datas:
        # 将元组转换为字符串，并用逗号分隔
        line = ",".join(str(x) for x in tup)
        f.write(line + "\n")  # 写入文件，每个元组后添加换行符
