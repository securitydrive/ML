from django.http import HttpResponse
import json
from road.k_means import result


def k_means(request):
    """
    APP发送一个car_id 算法用json返回用这个car_id之前的数据得到的危险点坐标 目前只有一个car_id的数据
    现在只能用app_data_store这个数据表里的long lat car_speed car_acc这些字段
    """
    print(request.GET['car_id'])
    k_means_result = result(request.GET['car_id'])
    return HttpResponse(json.dumps(k_means_result))
