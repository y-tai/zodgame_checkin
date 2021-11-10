import re
import sys
import time

import undetected_chromedriver.v2 as uc

def zodgame(cookie_string):
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    #options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Mobile Safari/537.36")
    driver = uc.Chrome(options=options)

    driver.execute_script('window.open("https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign");')
    time.sleep(10)

    cookie_dict = [ 
        {"name" : x.split('=')[0].strip(), "value": x.split('=')[1].strip()} 
        for x in cookie_string.split(';')
    ]

    url = "https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign"
    driver.get(url)
    driver.delete_all_cookies()
    for cookie in cookie_dict:
        driver.add_cookie({
            "domain": "zodgame.xyz",
            "name": cookie["name"],
            "value": cookie["value"],
            "path": "/",
        })
    driver.execute_script('window.open("https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign");')
    driver.get(url)
    time.sleep(30)
    try:
        driver.find_element(uc.selenium.webdriver.common.by.By.XPATH, '//div[@class="bm_h cl"]')
    except:
        print("Login failed, Please check the cookie.")
        #assert False, "Login failed, Please check the cookie."

    #time.sleep(600)

    formhash = driver.find_element(uc.selenium.webdriver.common.by.By.XPATH, '//input[@name="formhash"]').get_attribute('value')
    url2 = "https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=0"    
    ajax_query = """
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
        """ % (formhash, url2)
    ajax_query = ajax_query.replace("\n", "")
    resp = driver.execute_script("return " + ajax_query)
    match = re.search('<div class="c">\n(.*?)</div>\n',resp["response"],re.S)
    if match is not None:
        message = match.group(1)
    else:
        message = "签到失败"
    print(message)
    if "您今日已经签到，请明天再来" in message or "恭喜你签到成功!" in message:
        pass
    else:
        assert False
    driver.close()
    driver.quit()
    
if __name__ == "__main__":
    cookie_string = sys.argv[1]
    if cookie_string:
        zodgame(cookie_string)
    else:
        print("未配置Cookie")
        assert False, "Please set the cookie."
