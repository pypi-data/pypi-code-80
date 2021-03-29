import datetime
import signal
import multiprocessing
import threading
import time
import pickle

keep_going = True


def run_nng_sub():
    import numpy as np
    from pynng import Sub0, Timeout

    address = 'tcp://127.0.0.1:31313'
    latencies = []
    with Sub0(listen=address, recv_timeout=100) as sub:
        sub.subscribe(b'')
        time.sleep(0.05)
        global keep_going

        while keep_going:
            try:
                b_datetime = sub.recv()
                received_time = datetime.datetime.utcnow()

                sent_time = pickle.loads(b_datetime)
                latency = received_time - sent_time
                latencies.append(latency)
                # print(f'latency: {latency}')
                if len(latencies) % 100 == 0:
                    print(len(latencies))
            except Timeout:
                if len(latencies) > 1000:
                    keep_going = False
                    break

    print(
        f'latency:\nmax {np.max(latencies)}\naverage {np.mean(latencies)}\nmedian {np.median(latencies)}'
    )


def run_nng_pub():
    from pynng import Pub0

    address = 'tcp://127.0.0.1:31313'
    with Pub0(dial=address) as pub:

        i = 0
        while keep_going:
            pub.send(pickle.dumps(datetime.datetime.utcnow()))
            time.sleep(0.001)
            i += 1
        print(f'sent {i}')


def handler(signal, frame):
    global keep_going
    keep_going = False


signal.signal(signal.SIGINT, handler)

Thing = threading.Thread

t1 = Thing(target=run_nng_pub)
t2 = Thing(target=run_nng_sub)
t1.start()
t2.start()
t1.join()
t2.join()
