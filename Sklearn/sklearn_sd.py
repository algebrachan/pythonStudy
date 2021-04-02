from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import jieba
# import sklearn


def datasets_demo():
    """
    sklearn 学习使用
    """
    iris = load_iris()
    # print("数据集2:\n", iris)
    # 数据集划分
    x_train, x_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=22)
    print("训练集的特征值x：\n", x_train, x_train.shape)
    print("测试集的特征值x：\n", x_test, x_test.shape)
    print("训练集的特征值y：\n", y_train, y_train.shape)
    print("测试集的特征值y：\n", y_test, y_test.shape)
    return None


def dict_demo():
    """字典特征提取
    """
    data = [
        {'city': '北京', 'temp': 100},
        {'city': '上海', 'temp': 60},
        {'city': '深圳', 'temp': 30},
    ]
    # 1.实例化一个转换器
    transfer = DictVectorizer(sparse=False)
    # 2.调用fit_transform()
    data_new = transfer.fit_transform(data)
    print("data_new\n", data_new)
    print("特征名字\n", transfer.get_feature_names())


def count_demo():
    """文本特征抽取
    """
    data = ["life is short,i like life", "life is too long,i dislike python"]
    transfer = CountVectorizer()
    data_new = transfer.fit_transform(data)
    print("data_new\n", data_new.toarray())
    print("特征名字\n", transfer.get_feature_names())
    return None


def cut_word(text):

    res = " ".join(list(jieba.cut(text)))
    print('res', res)
    return res


def tidif_demo():
    """ 用TF-DIF的方法进行文本抽取
    """
    data = ["西安城北农业局小区在 2009 年之前曾有过物业，", "因为在管理上存在问题，",
            "后经过全体业主大会通过，", "选了 6 名业主成立业委会自行管理。"]
    data_new = []
    for sent in data:
        data_new.append(cut_word(sent))
    transfer = TfidfVectorizer(stop_words=["因为"])
    data_final = transfer.fit_transform(data_new)
    print("data_new\n", data_final.toarray())
    print("特征名字\n", transfer.get_feature_names())


if __name__ == "__main__":
    # datasets_demo()
    # dict_demo()
    # count_demo()
    # cut_word("我爱北京天安门")
    tidif_demo()
