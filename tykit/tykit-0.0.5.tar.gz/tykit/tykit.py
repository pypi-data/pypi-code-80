'''
Description: typb -> Tian_Yu_Progress_Bar 进度条,显示range的进度条，生成器进度条，多线程进度条，多线程偏函数进度条
version: 
Author: TianyuYuan
Date: 2021-03-26 13:44:18
LastEditors: TianyuYuan
LastEditTime: 2021-04-02 17:53:58
'''
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from concurrent.futures import ThreadPoolExecutor,as_completed
from functools import partial
from datetime import datetime

console = Console()
class ProgressBar():
    """类：进度条，可用于显示普通迭代的进度"""
    def __init__(self,task,length,batchs=50):
        """类：进度条，可用于显示迭代的进度
        - task: 任务名称，可填入·函数名·或者·字符串·,若填入函数名，则可自动获取该函数的名字描述
        - length: 任务长度，通常为可迭代对象的长度，即len(iter_files)
        - batch: 进度条的份数，默认为100个单位，以百分制显示进度
        """
        if isinstance(task,str): self.task_name = task
        else: self.task_name = task.__name__
        self.length = length
        if self.length < batchs: 
            self.batchs=self.length
            self.batch_size=1
        else: 
            self.batchs = batchs
            self.batch_size = self.length/self.batchs
        self.begin_time = datetime.now()

    def progress_layout(self):
        # TODO 进度条布局模块化
        layout = ""
        return layout

    def time_countdown(self,progress):
        if progress == 0:
            return "--:--"
        now_time = datetime.now()
        time_cost = now_time-self.begin_time
        time_cost = time_cost.seconds
        predict_time = round(time_cost/progress*self.batchs)
        time_cost = round(time_cost)
        return time_cost,predict_time

    def print_progressbar(self,i):
        """
        - i: 迭代到了第i个job
        """
        progress = int(i/self.batch_size)
        p_bar = "["+"[bold green]>[/bold green]"*(progress)+"]"
        p_propotion = "[green]{}[/green]/[red]{}[/red]".format(i,self.length)
        p_percentage = ":rocket: {}%".format(round(i/self.length*100))
        p_time = "[cyan]{}/{}s[/cyan]".format(*self.time_countdown(progress))
        if i < self.length:
            rprint(f"{self.task_name}  {p_percentage}  {p_time} :{p_bar}  {p_propotion}",end="\r")
        else:
            rprint(f"{self.task_name}  {p_percentage}  {p_time} :{p_bar}  {p_propotion}")


# * * * * * * * * * * * * * * * * * * * * * * * #
# *            请调用这一部分的函数！             * #
# * * * * * * * * * * * * * * * * * * * * * * * #
def pb_iter(iter_files):
    """生成器，将可迭代对象填入，在生成element的同时显示迭代的进度"""
    pb = ProgressBar("iter",len(iter_files))
    i = 0
    for element in iter_files:
        i += 1
        pb.print_progressbar(i)
        yield element

def pb_range(*args):
    """可显示迭代进度的range()，功能用法与range相同
    """
    iter_files = range(*args)
    return pb_iter(iter_files)

def pb_multi_thread(workers:int,task,iter_files) -> list:
    """显示多进程进度条
    - workers: 指定多进程的max_workers
    - task: 任务函数
    - iter_files: 填入要处理的可迭代对象
    - return: 返回每个job的结果，并存入list返回
    """
    pb = ProgressBar(task,len(iter_files))
    result = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        job_list = []
        for task_input in iter_files:
            job = pool.submit(task,task_input)
            job_list.append(job)
        i = 0
        for done_job in as_completed(job_list):
            i += 1
            result.append(done_job.result())
            pb.print_progressbar(i)
    return result

def pb_multi_thread_partial(workers:int,task,iter_files,**kwargs):
    """显示多进程进度条，针对具有多参数的任务
    - workers: 指定多进程的max_workers
    - task: 任务函数
    - iter_files: 填入要处理的可迭代对象
    - **kwargs: 填入'keyword=constant_object....'
    - return: 返回每个job的结果，并存入list返回
    """
    new_task = partial(task,**kwargs)
    new_task.__name__ = task.__name__
    return pb_multi_thread(workers,new_task,iter_files)


class RLog():
    """打印log的模版 with rich
    ### method：
    say(line), saynum(line,num), start, done, error, caution
    """
    console = Console()

    @staticmethod
    def say(line):
        """简单的log"""
        console.log(line)

    @staticmethod
    def saynum(line,num):
        """语句+数字变量"""
        line += str(num)
        console.log(line)

    @staticmethod
    def start(line:str,title:str='Start!',align='left',padding=0):
        """提示开始的log"""
        console.log(Panel.fit(
            line,
            title=f'[green bold]{title}[/green bold]',
            border_style='green',
            padding=padding,
        ),justify=align)

    @staticmethod
    def done(line:str,title:str='Completed!',align='left',padding=0):
        """提示完成的log"""
        console.log(Panel.fit(
            line,
            title=f'[green bold]{title}[/green bold]',
            border_style='green',
            padding=padding,
        ),justify=align)
    
    @staticmethod
    def error(line:str,title:str='Error!',align='left',padding=0):
        """提示错误的log"""
        console.log(Panel.fit(
            line,
            title=f'[bold red]{title}[/bold red]',
            border_style='red',
            padding=padding,
        ),justify=align)
    
    @staticmethod
    def caution(line:str,title:str='Caution!',align='left',padding=0):
        """提示，注意事项的log"""
        console.log(Panel.fit(
            line,
            title=f'[bold cyan]{title}[/bold cyan]',
            border_style='cyan',
            padding=padding,
        ),justify=align)

    @staticmethod
    def stage(title:str='Next Stage'):
        """打印水平横线外加标题，适用于提示stage change"""
        console.rule(title)
# * * * * * * * * * * * * * * * * * * * * * * * #
# *           Test Cases & Examples           * #
# * * * * * * * * * * * * * * * * * * * * * * * #
def square_a_num(x):
    """任务函数"""
    import time
    time.sleep(0.05)
    return x*x

def multi_param_task(x,a,b,c):
    """多参数任务函数"""
    return x+a+b+c

def pb_range_testcase(*args):
    result = []
    for i in pb_range(*args):
        result.append(square_a_num(i))
    # print(result)

def pb_simple_iter_testcase(x):
    result = []
    for i in pb_iter(range(x)):
        result.append(square_a_num(i))
    # print(result)
    
def pb_multi_thread_testcase(x):
    iter_files = range(x)
    result = pb_multi_thread(10,square_a_num,iter_files)
    # print(result)

def pb_multi_thread_partial_testcase(x,a,b,c):
    iter_files = range(x)
    result = pb_multi_thread_partial(10,multi_param_task,iter_files,a=a,b=b,c=c)
    # print(result)

if __name__ == "__main__":
    # ! Progress Bar Test case
    rlog = RLog()
    rlog.start('Use tykit.progress bar in for-loop just like range()')
    pb_range_testcase(3)
    pb_range_testcase(50)
    rlog.stage()
    rlog.start("Use tykit.progress bar with multi-threading and boost your speed! ")
    pb_multi_thread_testcase(50)
    pb_multi_thread_testcase(1000)
    rlog.console.log("pb_multi_thread_partial_testcase(15,1,1,1)")
    rlog.say("tykit also supports multi-threading task with multi-thread inputs!")
    pb_multi_thread_partial_testcase(1000,1,1,1)
    rlog.done("The show is done! Hope it's helpful!:smile:")
    # ! RLog Test case
    # rlog = RLog()
    # a = 9
    # rlog.say('To be or not to be, its a question')
    # rlog.saynum('hello world: ', a)
    # rlog.start('*** GenerateLabelFiles Start! ***')
    # rlog.done('Sort img has completed')
    # rlog.error('missing img')
    # rlog.caution('Model test isnt done yet!')
    # rlog.done('Pipeline Completed!\nThe dataset has been build successfully!',align='center',padding=1)
    # rlog.caution("Note: Model Test Not Done, Please download and test model manually......")
    # rlog.stage('chapter one')

