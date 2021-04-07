import datetime
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression,SGDRegressor,Ridge
from sklearn.metrics import mean_squared_error
import joblib

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
    print("正规方程-权重系数为:\n",estimator.coef_)
    print("正规方程-偏置为:\n",estimator.intercept_) # y = ax+b 中的b 为偏置
    # 6.模型评估
    y_predict = estimator.predict(x_test)
    print("预测房价:\n",y_predict)
    error = mean_squared_error(y_test,y_predict) # 均方误差
    print("正规方程-均方误差为:\n",error)


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
    estimator = SGDRegressor(learning_rate="constant", eta0=0.01,max_iter=100000)
    estimator.fit(x_train,y_train)

    # 5.得出模型
    print("梯度下降-权重系数为:\n",estimator.coef_)
    print("梯度下降-偏置为:\n",estimator.intercept_)
    # 6.模型评估
    y_predict = estimator.predict(x_test)
    print("预测房价:\n",y_predict)
    error = mean_squared_error(y_test,y_predict) # 均方误差
    print("梯度下降-均方误差为:\n",error)

    return None

def linear3():
    """
    岭回归对波士顿房价进行预测
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

    # # 4.预估器
    # estimator = Ridge(max_iter=10000,alpha=0.5)
    # estimator.fit(x_train,y_train)

    # # 保存模型
    # joblib.dump(estimator,"my_ridge.pkl")
    # 加载模型
    estimator = joblib.load("my_ridge.pkl")

    # 5.得出模型
    print("岭回归-权重系数为:\n",estimator.coef_)
    print("岭回归-偏置为:\n",estimator.intercept_)
    # 6.模型评估
    y_predict = estimator.predict(x_test)
    print("预测房价:\n",y_predict)
    error = mean_squared_error(y_test,y_predict) # 均方误差
    print("岭回归-均方误差为:\n",error)

    return None

if __name__ =="__main__":
    start = datetime.datetime.now()
    # linear1()
    # linear2()
    linear3()
    end = datetime.datetime.now()
    print("使用时间",end-start)