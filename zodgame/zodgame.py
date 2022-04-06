# encoding=utf8
import io
import re
import sys
import time
import subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def get_driver_version():
   cmd = r'''powershell -command "&{(Get-Item 'C:\Program Files\Google\Chrome\Application\chrome.exe').VersionInfo.ProductVersion}"'''
   try:
       out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
       out = out.decode('utf-8').split(".")[0]
       return out
   except IndexError as e:
       print('Check chrome version failed:{}'.format(e))
       return 0


def zodgame_checkin(driver, formhash):
    checkin_url = "https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=0"    
    checkin_query = """
        (function (){
        var request = new XMLHttpRequest();
        var fd = new FormData();
        fd.append("formhash","%s");
        fd.append("qdxq","kx");
        request.open("POST","%s",false);
        request.withCredentials=true;
        request.send(fd);
        return request;
        })();
        """ % (formhash, checkin_url)
    checkin_query = checkin_query.replace("\n", "")
    driver.set_script_timeout(240)
    resp = driver.execute_script("return " + checkin_query)
    match = re.search('<div class="c">\n(.*?)</div>\n', resp["response"], re.S)
    message = match[1] if match is not None else "签到失败"
    print(f"【签到】{message}")
    return "恭喜你签到成功!" in message or "您今日已经签到，请明天再来" in message

def zodgame_task(driver, formhash):

    def show_task_reward(driver):
        driver.get("https://zodgame.xyz/plugin.php?id=jnbux")
        try:
            WebDriverWait(driver, 240).until(
                lambda x: x.title != "Just a moment..."
            )
            reward = driver.find_element(By.XPATH, '//li[contains(text(), "点币: ")]').get_attribute("textContent")[:-2]
            print(f"【Log】{reward}")
        except:
            pass

    def check_task_url(tasks):
        def wrapper(driver):
            vote = 0
            handles = driver.window_handles
            for task in tasks:
                if task["check_flag"] is True:
                    vote = vote + 1
                    continue
                if task["handle"] in handles:
                    driver.switch_to.window(task["handle"])
                    if len(driver.find_elements(By.XPATH, '//div[text()="成功！"]')) != 0:
                        driver.get(task["check_url"])
                        task["adv_flag"] = True
                    if task["adv_flag"] is True and len(driver.find_elements(By.XPATH, '//p[contains(text(), "检查成功, 积分已经加入您的帐户中")]'))!=0:
                        task["check_flag"] = True
            return vote == len(tasks)
        return wrapper
        
    driver.get("https://zodgame.xyz/plugin.php?id=jnbux")
    WebDriverWait(driver, 240).until(
        lambda x: x.title != "Just a moment..."
    )

    join_bux = driver.find_elements(By.XPATH, '//font[text()="开始参与任务"]')
    if len(join_bux) != 0 :    
        driver.get(f"https://zodgame.xyz/plugin.php?id=jnbux:jnbux&do=join&formhash={formhash}")
        WebDriverWait(driver, 240).until(
            lambda x: x.title != "Just a moment..."
        )
        zodgame_task(driver, formhash)
        return

    join_task_a = driver.find_elements(By.XPATH, '//a[text()="参与任务"]')
    success = True

    if len(join_task_a) == 0:
        print("【任务】所有任务均已完成。")
        return success
   
    tasks = list()
    for idx, a in enumerate(join_task_a):
        on_click = a.get_attribute("onclick")
        try:
            function = re.search("""openNewWindow(.*?)\(\)""", on_click, re.S)[0]
            script = driver.find_element(By.XPATH, f'//script[contains(text(), "{function}")]').get_attribute("text")
            task_url = re.search("""window.open\("(.*)", "newwindow"\)""", script, re.S)[1]
            check_url = re.search("""showWindow\('check', '(.*)'\);""", on_click, re.S)[1]
            task_url = "https://zodgame.xyz/" + task_url
            check_url = "https://zodgame.xyz/" + check_url
            driver.tab_new(task_url)
            tasks.append({
                "id": idx + 1,
                "task_url": task_url,
                "check_url": check_url,
                "handle": driver.window_handles[-1],
                "adv_flag": False,
                "check_flag": False,
            })
        except:
            print(f"【Log】任务{idx + 1}获取url失败。")

    if len(tasks) == 0:
        print("【Log】获取广告页失败。")
        return False

    try:
        WebDriverWait(driver, 240).until(check_task_url(tasks))
    except:
        pass
      
    for task in tasks:
        idx = task["id"]
        if task["adv_flag"] is False:
            print(f"【Log】任务 {idx} 广告页检查失败。")
        elif task["check_flag"] is False:
            print(f"【Log】任务 {idx} 确认页检查失败。")
        else:
            print(f"【Log】任务 {idx} 成功。")

    show_task_reward(driver)

    return success

def zodgame(cookie_string):
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
      
    version = get_driver_version()
    driver = uc.Chrome(version_main=version, options = options)

    # Load cookie
    driver.get("https://zodgame.xyz/")

    cookie_string = cookie_string.replace("/","%2")
    cookie_dict = [ 
        {"name" : x.split('=')[0].strip(), "value": x.split('=')[1].strip()} 
        for x in cookie_string.split(';')
    ]

    driver.delete_all_cookies()
    for cookie in cookie_dict:
        if cookie["name"] in ["qhMq_2132_saltkey", "qhMq_2132_auth"]:
            driver.add_cookie({
                "domain": "zodgame.xyz",
                "name": cookie["name"],
                "value": cookie["value"],
                "path": "/",
            })
    
    driver.get("https://zodgame.xyz/")
    
    try:
        WebDriverWait(driver, 240).until(
            lambda x: x.title != "Just a moment..."
        )
        formhash = driver.find_element(By.XPATH, '//input[@name="formhash"]').get_attribute('value')
    except:
        assert False, "Login fails. Please check your cookie."
    
    assert zodgame_checkin(driver, formhash) and zodgame_task(driver, formhash), "Checkin failed or task failed."

    driver.close()
    driver.quit()
    
if __name__ == "__main__":
    cookie_string = sys.argv[1]
    assert cookie_string
    
    zodgame(cookie_string)
