#!/usr/bin/env python
import pika
import sys
import time
#import urlib


def tester(msg):
    pass


class Skt(object):
    def __init__(self, user=None, password=None, host='localhost'):
        if (user):
            urlib.init_all()
            credentials = pika.PlainCredentials(user, password)
            params = pika.ConnectionParameters(host=host, 
                                               credentials=credentials)
        else:
            urlib.init_all()
            params = pika.ConnectionParameters(host=host, heartbeat=0)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        self.funcQueue = dict()
        self.ak = dict()


    def AddQ(self, queue, ttl, pubsub='p', func=None, auto_ack0=True, callback=True):
        if (type(ttl)==str):
            ttl=int(ttl,10)
        if (ttl>0):
            self.channel.queue_declare(queue=queue, arguments={'x-message-ttl' : ttl,"overflow":"reject-publish"})
        else:
            self.channel.queue_declare(queue=queue)
        if (pubsub=='s'):
            self.funcQueue[queue]=func
            self.ak[queue]=auto_ack0
            if(callback):
                self.channel.basic_consume(
                    queue=queue,
                    auto_ack=auto_ack0,
                    on_message_callback=self.callback)
        else:
            pass

    def Send(self, queue, msg):
        self.channel.basic_publish(exchange='', routing_key=queue, body=msg, mandatory=True)
        print("[send on (%s)] %s" % (queue, msg) )


    def Start(self):
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        msg=body.decode()
        print("[recieve on (%s)] %s" % (method.routing_key, msg) )
        self.funcQueue[method.routing_key](msg)
        if(not(self.ak[method.routing_key])):
            print("*** ack from (%s) ****"% method.routing_key)
            ch.basic_ack(delivery_tag = method.delivery_tag)

    def TryGet(self, queue, timeout=0, auto_ack0=False):
        try:
            method_frame, properties, body = self.channel.consume(queue, inactivity_timeout=timeout, auto_ack=auto_ack0).__next__()
            if (not(method_frame)):
                return(None,None)
            return(method_frame.delivery_tag, body.decode())   
        except Exception as e:
            print('e: ',e)
            return(None,None)


    def Ack(self, m):
        self.channel.basic_ack(m)

    def close(self):
        self.connection.close()



if __name__ == "__main__":
    try:
        if(sys.argv[1]=='send'):
            # Pefer to name Pub var same as queue name (1st param)
            s = Skt()
            s.AddQ(sys.argv[2],sys.argv[3])
            s.Send(sys.argv[2],sys.argv[4])
            s.close()
        elif(sys.argv[1]=='recv'):
            s = Skt()
            s.AddQ(sys.argv[2],sys.argv[3],'s',tester)
            s.Start()
        elif(sys.argv[1]=='syncav'):
            s = Skt()
            s.AddQ('audio_cmd', 1000)
            s.AddQ('faces', 1000)
            input("Enter to continue")
            s.Send('audio_cmd','l')
            s.Send('faces','l')

        else:
            raise Exception("! Error!")
    

    except KeyboardInterrupt:
            s.close()

    except Exception as e:
        print(e)
        usage="error"
        print (usage)
