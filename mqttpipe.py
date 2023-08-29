from paho.mqtt import client as mqtt


class Mqttpipe(object):

    def __init__(self, vehicle_id):
        super(Mqttpipe, self).__init__()
        self._vehicle_id = vehicle_id
        self._mqtt_host = "121.37.111.104"
        self._mqtt_port = 1883
        self._mqtt_kpalv = 60
        self._client = mqtt.Client(vehicle_id)
        self._will_msg = {
            "id": f"{self._vehicle_id}",
            "stat": "offline"
        }

        self._client.connect(self._mqtt_host, self._mqtt_port, self._mqtt_kpalv)
        self._client.on_message = self._on_message
        self._client.on_connect = self.on_connect
        self._client.on_publish = self._on_publish
        self._client.on_connect_fail = self._on_connect_fail
        self._client.on_disconnect = self._on_disconnect
        self._client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker, ip:" + self._mqtt_host)
        client.subscribe("msg/" + self._vehicle_id)
        online_msg = {
            "id": f"{self._vehicle_id}",
            "stat": "online"
        }
        self._client.publish("vstat", str(online_msg))
        self._client.will_set("vstat", str(self._will_msg))

    def _on_disconnect(self, client, userdata, rc):
        print("Disconnect from broker with reason code " + rc)

    def _on_connect_fail(self, client, userdata):
        print("Connect failed. Trying to reconnect...")
        self._client.reconnect()

    def _on_publish(client, userdata, mid):
        print("publish success with msg_id: " + str(mid))

    def _on_message(self, client, userdata, msg):
        print("(Default callback) Received topic: " + msg.topic + "\nmessage: " + str(msg.payload.decode("utf-8")))

    def _wrap_on_message(self, callback):
        def on_message_wrapper(client, userdata, message):
            callback(message.payload)

        return on_message_wrapper

    def publish(self, topic, payload, qos=0, retain=False):
        self._client.publish(topic, payload, qos, retain)

    def subscribe(self, topic, callback, qos=2):
        self._client.subscribe(topic, qos)
        self._client.message_callback_add(topic, self._wrap_on_message(callback))

    def callback_add(self, topic, callback):
        self._client.message_callback_add("msg/" + topic, self._wrap_on_message(callback))

    def callback_remove(self, topic):
        self._client.message_callback_remove(topic)

    def disconnect(self):
        self._client.disconnect()
