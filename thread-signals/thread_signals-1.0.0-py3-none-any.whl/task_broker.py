import threading, queue

from thread_signals.task import TaskFuncRun


class Task_broker(queue.Queue):
    def __init__(self, executor_thread_id, on_added_event_list=None, on_all_done_event_list=None):

        queue.Queue.__init__(self, 0)

        self._executor_thread_id = executor_thread_id

        self._on_added_event_list = on_added_event_list
        self._on_all_done_event_list = on_all_done_event_list

    def _notify_all(self, event_list):
        if event_list is None:
            return
        for i in event_list:
            i.set()

    def _notify_added(self):
        self._notify_all(self._on_added_event_list)

    def _notify_all_done(self):
        self._notify_all(self._on_all_done_event_list)


    def run_func_as_task(self, func, args, kwargs, timeout, sync_call=True):
        task = TaskFuncRun(self._executor_thread_id, func, args, kwargs)
        self.put_nowait(task)

        self._notify_added()

        # nothing to wait
        if not sync_call: return

        # wait for execution if sync call
        res = task.wait(timeout)
        if not res: return False

        return (task.is_successful(), task.get_result(), task.get_exception())

    def _run_task(self, task, reraise_error=False):
        task.run_task()
        if reraise_error and not task.is_successful():
            raise task.get_exception()

    def run_all_tasks(self, reraise_error=False):
        if threading.get_ident() != self._executor_thread_id:
            raise Exception('Tasks could only be run from execution thread!')

        while True:
            try:
                t = self.get_nowait()
            except:
                break
            else:
                self._run_task(t, reraise_error)
                self.task_done()

        self._notify_all_done()


    # one broker per thread
    _broker_list_lock = threading.RLock()
    _broker_list = {}  # thread_id: broker

    @classmethod
    def get_task_broker(cls, executor_thread_id, on_added_event_list=None, on_all_done_event_list = None):
        with cls._broker_list_lock:
            if executor_thread_id in cls._broker_list:
                res = cls._broker_list[executor_thread_id]
            else:
                res = cls(executor_thread_id, on_added_event_list, on_all_done_event_list)
                cls._broker_list[executor_thread_id] = res

        return res


def get_thread_broker(thread_ident=None, on_added_event_list=None, on_all_done_event_list = None):
    if thread_ident is None:
        thread_ident = threading.get_ident()

    return Task_broker.get_task_broker(thread_ident, on_added_event_list, on_all_done_event_list)
