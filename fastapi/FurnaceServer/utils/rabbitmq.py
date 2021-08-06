import pika
import json
import threading


class RabbitMq:
    def __init__(self, user, pwd, host, port):
        credentials = pika.PlainCredentials(user, pwd)  # mq用户名和密码
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host, port=port, credentials=credentials, heartbeat=0)
        )
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)

    def __create_queue(self, routing_keys):
        # 创建队列。有就不管，没有就自动创建
        if not isinstance(routing_keys, list):
            routing_keys = [routing_keys]
        for _, v in enumerate(routing_keys):
            self.channel.queue_declare(queue=v)

    '''单向发送消息'''

    def send(self, routing_key, body):
        # 使用默认的交换机发送消息。exchange为空就使用默认的
        self.__create_queue(routing_keys=routing_key)
        msg_props = pika.BasicProperties()
        msg_props.content_type = "application/json"
        if isinstance(body, dict):
            body = json.dumps(body)
        self.channel.basic_publish(
            exchange='', properties=msg_props, routing_key=routing_key, body=body)

    def received(self, routing_key, fun):
        self.__create_queue(routing_keys=routing_key)
        self.channel.basic_consume(routing_key, fun, True)

    #  传入k-fun，可以实现topic到函数路由功能
    def received_dict(self, fun_dict):
        for i, v in fun_dict.items():
            self.received(routing_key=i, fun=v)

    def consume(self):
        self.channel.start_consuming()

    def close(self):
        self.connection.close()


class AsyncMq(threading.Thread):
    def __init__(self, rabbitmq: RabbitMq, queue: str):
        threading.Thread.__init__(self)
        self.mq = rabbitmq
        self.queue = queue

    def callback(self, ch, method, properties, body):
        # print(ch)
        # print(method)
        # print(properties)
        # print(" [x] Received %r" % (body,))
        print(json.loads(body))

    def consume(self):
        self.mq.received(routing_key=self.queue, fun=self.callback)
        self.mq.consume()


# if __name__ == 'utils.rabbitmq':
if __name__ == '__main__':
    mq = AsyncMq(RabbitMq(user='furnance', pwd='123456', host='127.0.0.1', port=5672),'test')
    mq.consume()
    
