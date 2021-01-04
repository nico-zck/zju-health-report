# -*- coding: utf-8 -*-
import time

import schedule

from zju_health_report import report

if __name__ == "__main__":

    TIME = "08:00"

    print(f"开始执行计划任务，预计每天{TIME}之后执行任务")
    schedule.every().day.at(TIME).do(report)

    # # test
    # def foo():
    #     print("执行任务")
    # schedule.every(30).seconds.do(foo)

    while True:
        schedule.run_pending()
        time.sleep(10)  # check every 10 seconds
