import smay
import rospy

import threading

__all__ = ['StateMachine']


class StateMachine(smay.StateMachine):

    def __init__(self, node_name='monitor'):
        smay.StateMachine.__init__(self)
        self._thread = None

        self.sub = {}
        self.pub = {}
        rospy.init_node(node_name)

    def add_sub(self, topic, msg_type):
        def cb(msg):
            self.sub[topic] = msg.data

        rospy.Subscriber(topic, msg_type, callback=cb, queue_size=10)
        self.sub[topic] = None

    def add_pub(self, topic, msg_type):
        self.pub[topic] = rospy.Publisher(topic, msg_type, queue_size=10)

    def _begin_thread(self):
        self._thread = threading.Thread(target=smay.StateMachine.begin, args=(self,))
        self._thread.setDaemon(True)
        self._thread.start()

    def begin(self):
        if self._thread is None:
            self._begin_thread()
            rospy.spin()
        elif not self._thread.is_alive():
            self._begin_thread()
