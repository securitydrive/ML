import sklearn.preprocessing as pp
from sklearn import decomposition
from sklearn import cluster
import numpy as np
from road.database import DataBase


def load_data(car_id):
    """
    根据用户id取数据
    :param car_id:
    :return: 返回从数据库中取出的数据
    """
    sql = 'SELECT long, lat, car_speed, car_acc FROM `app_data_store` WHERE car_id = ' + car_id
    db = DataBase()
    cur, connect = db.connect_db()
    return db.query_data_set(cur=cur, query=sql)


def transforms(data):
    """
    :param data:
    :return:
    """
    scare = pp.MinMaxScaler(feature_range=(0, 1))
    return scare.fit_transform(data)


def data_pca(data, stand):
    pca = decomposition.PCA()
    pca.fit(data)
    data_weight = np.where(pca.explained_variance_ > stand, pca.explained_variance_, 0)
    return [i for i in range(len(data_weight)) if data_weight[i] == 0]


def k_means_cluster(data_set):
    k_means = cluster.KMeans(n_clusters=2)
    k_means.fit(data_set)
    return k_means.labels_


def result(car_id):
    """

    :param car_id:
    :return:
    """
    query_res = load_data(car_id)

    """
    你们自己处理的数据转换
    """

    location = np.array([query_res['long'].values, query_res['lat'].values]).astype("float64").transpose()
    data = query_res[['car_speed', 'car_acc']]
    data = transforms(data)

    feature_label = data_pca(data=data, stand=0.01)
    data = np.delete(data, feature_label, axis=1)
    labels = k_means_cluster(data)

    abnormal_id = 0 if 2 * np.sum(labels) > len(labels) else 1  # 两类中少的判为异常类

    res_data = {'coordinate': []}  # 返回json 格式: {'coordinate': [{'long': long, 'lat': lat}, ...]}

    for i in range(len(labels)):
        if labels[i] == abnormal_id:
            res_data['coordinate'].append({'long': location[i][0], 'lat': location[i][1]})

