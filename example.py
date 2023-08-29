from paho.mqtt import client
from mqttpipe import Mqttpipe

'''
基本使用流程:

    * 使用 Mqttpipe(vehicle_id) 初始化一个MQTT客户端实例，同时和服务器进行连接，并订阅id为vehicle_id的topic
    * mqtt消息以push的方式传送给所有订阅该topic的客户端。使用 callback_add(topic, callback)为topic下所有msg绑定回调函数进行处理
    * msg中的payload将作为参数传入callback(),该回调阻塞，建议在此回调中将msg传给其他线程执行数据处理，避免消息传输延迟
    * 使用 callback_remove(topic) 将之前绑定给topic的回调函数删除。
    * 使用 subscribe(topic, callback) 订阅某topic，并为该topic下的所有msg绑定回调函数。
    * 使用 publish(topic, payload) 来发送数据。其中payload以字节流传送。topic即为接收端vehicle_id
    * 使用 disconnect() 断开和服务器的连接
'''


def my_callback(msg):
    print("Received message with payload: " + msg.decode())


vehicle_id = "vehicle_01"
pipe_v01 = Mqttpipe(vehicle_id)
pipe_v01.callback_add(vehicle_id, my_callback)
pipe_v01.subscribe("topic")  # 绑定默认回调
msg = "hello"
target = "vehicle_02"
pipe_v01.publish(target, msg)