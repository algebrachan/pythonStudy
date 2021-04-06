import datetime
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression,SGDRegressor

def linear1():
    """
    正规方程的优化方法对波士顿房价进行预测
    """
    # 1.获取数据
    boston = load_boston()
    print("特征数量:\n",boston.data.shape)
    # 2.划分数据集
    x_train,x_test,y_train,y_test = train_test_split(boston.data,boston.target,random_state=22)
    # 3.标准化
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    # 4.预估器
    estimator = LinearRegression()
    estimator.fit(x_train,y_train)

    # 5.得出模型
    print("正规方程 权重系数为:\n",estimator.coef_)
    print("偏置为:\n",estimator.intercept_) # y = ax+b 中的b 为偏置
    # 6.模型评估

    return None

def linear2():
    """
    梯度下降的优化方法对波士顿房价进行预测
    """
    # 1.获取数据
    boston = load_boston()
    print("特征数量:\n",boston.data.shape)
    # 2.划分数据集
    x_train,x_test,y_train,y_test = train_test_split(boston.data,boston.target,random_state=22)
    # 3.标准化
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    # 4.预估器
    estimator = SGDRegressor()
    estimator.fit(x_train,y_train)

    # 5.得出模型
    print("梯度下降 权重系数为:\n",estimator.coef_)
    print("偏置为:\n",estimator.intercept_)
    # 6.模型评估

    return None

if __name__ =="__main__":
    start = datetime.datetime.now()
    linear1()
    linear2()
    end = datetime.datetime.now()
    print("使用时间",end-start)