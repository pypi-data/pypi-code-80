'''
Description: 
version: 
Author: TianyuYuan
Date: 2021-04-02 15:40:39
LastEditors: TianyuYuan
LastEditTime: 2021-04-02 18:49:18
'''
name = "tykit"
from tykit import (
    pb_range,
    pb_iter,
    pb_multi_thread,
    pb_multi_thread_partial,
    RLog,
    ProgressBar
    )

if __name__ == "__main__":
    rlog = RLog()
    rlog.start('hello world')