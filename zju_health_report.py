# -*- coding: utf-8 -*-
import datetime
import json
import os
import random
import time
from typing import Tuple

import ddddocr
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Edge as Browser, EdgeOptions as Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from users import USERS

MAX_REPEAT = 3
TIMEOUT = 20


def save_cookies(driver: WebDriver, user: dict):
    cookies = driver.get_cookies()
    with open(f"./{user['name']}-cookies.json", "w") as f:
        f.write(json.dumps(cookies))
    print(f"{user['name']}'s cookies saved!")


def load_cookies(driver: WebDriver, user: dict):
    driver.delete_all_cookies()
    with open(f"./{user['name']}-cookies.json", "r") as f:
        cookies = json.load(f)
    for c in cookies:
        driver.add_cookie(c)


def check_cookies_exist(driver: WebDriver, user: dict) -> bool:
    if os.path.exists(f"{user['name']}-cookies.json"):
        return True
    else:
        return False


def check_cookies_valid(driver: WebDriver) -> bool:
    try:
        driver.find_element_by_xpath('//*[@id="username"]')
    except NoSuchElementException:
        return True
    else:
        return False


def login(driver: WebDriver, user: dict):
    username_box = driver.find_element_by_xpath('//*[@id="username"]')
    password_box = driver.find_element_by_xpath('//*[@id="password"]')
    username_box.send_keys(user["username"])
    password_box.send_keys(user["password"])

    # tick remember login box
    rember = driver.find_element_by_xpath('//*[@id="fm1"]/div[4]/div[2]/label')
    rember.click()

    login_btn = driver.find_element_by_xpath('//*[@id="dl"]')
    login_btn.click()
    return True


def find_and_click_by_xpath(driver: WebDriver, xpath: str):
    try:
        elem: WebElement = driver.find_element_by_xpath(xpath)
        if elem.is_displayed():
            elem.click()
    except NoSuchElementException:
        print(f"Not find: {xpath}")


def find_and_click_by_name(driver: WebDriver, name: str):
    try:
        elem: WebElement = driver.find_element_by_name(name)
        if elem.is_displayed():
            elem.click()
    except NoSuchElementException:
        print(f"Not find: {name}")


def checkin(driver: WebDriver, user: dict) -> Tuple[bool, str]:
    try:
        WebDriverWait(driver, timeout=TIMEOUT, poll_frequency=1).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div[1]/div/section/div[4]",
                )
            )
        )

        # 点掉一些通知
        time.sleep(1)
        find_and_click_by_xpath(driver, '//*[@id="wapat"]/div/div[2]/div')

        # 是否意向接种
        find_and_click_by_xpath(
            driver, "//div[@name='sfyxjzxgym']/descendant::span[contains(.,'是 Yes')]"
        )
        # 是否是不宜接种人群
        find_and_click_by_xpath(
            driver, "//div[@name='sfbyjzrq']/descendant::span[.='否']"
        )  # title box also contains '否'
        # 当前接种情况
        find_and_click_by_xpath(
            driver, "//div[@name='jzxgymqk']/descendant::span[contains(.,'已接种第三针')]"
        )
        # 今日是否因发热请假未到岗
        find_and_click_by_xpath(
            driver, "//div[@name='sffrqjwdg']/descendant::span[contains(.,'否 No')]"
        )
        # 今日是否因发热外的其他原因请假未到岗
        find_and_click_by_xpath(
            driver, "//div[@name='sfqtyyqjwdg']/descendant::span[contains(.,'否 No')]"
        )
        # 今日是否有发热症状
        find_and_click_by_xpath(
            driver, "//div[@name='tw']/descendant::span[contains(.,'否 No')]"
        )
        # 今日是否被当地管理部门要求在集中隔离点医学观察
        find_and_click_by_xpath(
            driver, "//div[@name='sfyqjzgc']/descendant::span[contains(.,'否 No')]"
        )
        # 今日是否居家隔离观察
        find_and_click_by_xpath(
            driver, "//div[@name='sfcyglq']/descendant::span[contains(.,'否 No')]"
        )
        # 是否有任何与疫情相关的，值得注意的情况？
        find_and_click_by_xpath(
            driver, "//div[@name='sfcxzysx']/descendant::span[contains(.,'否 No')]"
        )
        # 选择校区
        find_and_click_by_xpath(
            driver, "//div[@name='campus']/descendant::span[contains(.,'玉泉校区')]"
        )
        # 是否已经申领校区所在地健康码
        find_and_click_by_xpath(
            driver, "//div[@name='sfsqhzjkk']/descendant::span[contains(.,'是 Yes')]"
        )
        # 今日申领校区所在地健康码的颜色
        find_and_click_by_xpath(
            driver,
            "//div[@name='sqhzjkkys']/descendant::span[contains(.,'绿码 Green code')]",
        )
        # 是否在校
        find_and_click_by_xpath(
            driver, "//div[@name='sfzx']/descendant::span[contains(.,'是 Yes')]"
        )
        # 所在地点
        find_and_click_by_xpath(
            driver, "//div[@name='sfzgn']/descendant::span[contains(.,'境内')]"
        )
        # 获取定位
        elems = driver.find_elements_by_xpath("//div[@name='area']/descendant::input")
        if len(elems) > 0:
            loc_elem = elems[0]
            loc_elem.click()
            # waitting loading animation
            time.sleep(2)
            WebDriverWait(driver, timeout=TIMEOUT, poll_frequency=1).until(
                lambda driver: driver.find_element_by_class_name(
                    "page-loading-container"
                ).is_displayed()
                == False
            )

        # 以下地区
        find_and_click_by_xpath(
            driver, "//div[@name='jrdqtlqk']/descendant::span[contains(.,'None')]"
        )
        # 家庭成员
        find_and_click_by_xpath(
            driver, "//div[@name='sfymqjczrj']/descendant::span[contains(.,'否 No')]"
        )
        # 验证码
        elems = driver.find_elements_by_xpath(
            "/html/body/div[1]/div[1]/div/section/div[4]/ul/li[26]/div/span/img"
        )
        if len(elems) > 0:
            img_elem = elems[0]
            img_bytes = img_elem.screenshot_as_png
            ocr = ddddocr.DdddOcr(show_ad=False)
            ver_code = ocr.classification(img_bytes)
            print(f"OCR验证码：{ver_code}")
            # put code into the textbox
            text_box = driver.find_element_by_xpath(
                "/html/body/div[1]/div[1]/div/section/div[4]/ul/li[26]/div/input"
            )
            text_box.clear()
            text_box.send_keys(ver_code)

        # 本人承诺
        find_and_click_by_name(driver, "sfqrxxss")

        # submit
        elems = driver.find_elements_by_xpath(
            "//div[@class='footers']/descendant::a[contains(.,'Submit')]"
        )
        if len(elems) > 0:
            elems[0].click()

        # wapcf 确认和提交信息
        # wapat 有问题的提示
        # //*[@id="wapcf"]  # mask
        # //*[@id="wapcf"]/div  # box
        # //*[@id="wapcf"]/div/div[1]  # title box
        # //*[@id="wapcf"]/div/div[2]  # botton box
        # //*[@id="wapcf"]/div/div[2]/div[2]  # right button
        WebDriverWait(driver, timeout=TIMEOUT, poll_frequency=1).until(
            lambda driver: driver.find_element_by_xpath(
                '//*[@id="wapat"]' + " | " + '//*[@id="wapcf"]'
            )
        )
        popup = driver.find_element_by_xpath(
            '//*[@id="wapat"]/div/div[1]' + " | " + '//*[@id="wapcf"]/div/div[1]'
        )
        popup_msg = popup.text
        if "确认" in popup_msg:
            popup_btn = driver.find_element_by_class_name("wapcf-btn-ok")
            popup_btn.click()
            time.sleep(1)
            # alert = driver.find_element_by_xpath('//*[@id="wapat"]/div/div[1]')
            alert = driver.find_element_by_class_name("alert")
            alert_msg = alert.text
            if "成功" in alert_msg:
                return True, "打卡成功"
            else:
                return False, alert_msg
        elif "你已提交过" in popup_msg:
            return True, "今天已经打卡"
        else:
            return True, popup_msg

    except TimeoutException as e:
        print(e)
        time.sleep(5)
        return False, "加载页面超时"
    except Exception as e:
        print(e)
        time.sleep(5)
        return False, "其他错误"


def report(sleep=True):
    for user in USERS:
        if sleep:
            # 1min - 2hours
            time.sleep(random.randint(60, 600))
            print(f"现在时间是：{datetime.datetime.now()}，开始打卡")

        options = Options()
        options
        options.add_argument(
            "--user-data-dir=" + r"C:\Users\nico\AppData\Local\Microsoft\Edge\User Data"
        )
        if os.path.exists("./msedgedriver.exe"):
            driver: WebDriver = Browser(
                executable_path="./msedgedriver.exe", options=options
            )
        else:
            driver: WebDriver = Browser(
                executable_path=r"F:\Downloads\msedgedriver.exe", options=options
            )

        cookies_exist_flag = check_cookies_exist(driver, user)
        if cookies_exist_flag:
            # fake page to fix the domain
            driver.get(
                "https://healthreport.zju.edu.cn/ncov/wap/default/index/404error"
            )
            load_cookies(driver, user)
            print("load from cookies")
            driver.get("https://healthreport.zju.edu.cn/ncov/wap/default/index")
            cookies_valid_flag = check_cookies_valid(driver)
            if not cookies_valid_flag:
                print("cookies no longer valid, will relogin to obtain cookies later.")

        if cookies_exist_flag and cookies_valid_flag:
            cookies_state = "load from old cookies"
        else:
            driver.get("https://healthreport.zju.edu.cn/ncov/wap/default/index")
            login(driver, user)
            save_cookies(driver, user)
            cookies_state = "new cookies are saved"

        # # geolocation = {"latitude": 30.2339, "longitude": 119.7247, "accuracy": 80}
        # # driver.execute_cdp_cmd("Page.setGeolocationOverride", geolocation)
        # geolocation = {"location": {"latitude": 30.2339, "longitude": 119.7247}}
        # driver.execute(Command.SET_LOCATION, geolocation)
        ret_msgs = []
        for i in range(MAX_REPEAT):
            done_flag, ret_msg = checkin(driver, user)
            if done_flag:
                print(f"【反馈】：{ret_msg}")
                print(f"{datetime.date.today()}：{user['name']} 打卡成功!")
                ret_msgs.append(ret_msg)
                break
            else:
                print(f"【错误】：第{i+1}次错误：{ret_msg}")
                ret_msgs.append(ret_msg)
        driver.close()

        if done_flag:
            msg = f"用户{user['name']}：今日打卡成功；日期：{datetime.datetime.now()}，cookies状态：{cookies_state}，弹窗信息：{ret_msgs}。"
        else:
            msg = f"用户{user['name']}：{MAX_REPEAT}次尝试依然打卡失败；日期：{datetime.datetime.now()}，cookies状态：{cookies_state}，弹窗信息：{ret_msgs}。请检查代码!"
        print(f"【推送】：{msg}")
        send_push(done_flag, msg, user["push_token"])


def send_push(state: bool, msg: str, token: str):
    import requests

    title = f"ZJU健康打卡【{'成功'if state else '失败'}】"
    content = msg
    r = requests.get(
        f"http://www.pushplus.plus/send?token={token}&title={title}&content={content}"
    )

    if r.status_code == 200:
        print(r.content)
    else:
        print("The push server may have some problem, please check it!")
    return r


if __name__ == "__main__":
    report(sleep=False)
