import re
import sys
import time

from xvfbwrapper import Xvfb
import undetected_chromedriver.v2 as uc

def zodgame(cookie_string):
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    #options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Mobile Safari/537.36")
    driver = uc.Chrome(options=options)

    login_url = "https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign"
    driver.execute_script('window.location.href="https://zodgame.xyz/";')
    cookie_dict = [ 
        {"name" : x.split('=')[0].strip(), "value": x.split('=')[1].strip()} 
        for x in cookie_string.split(';')
    ]

    driver.delete_all_cookies()
    for cookie in cookie_dict:
        driver.add_cookie({
            "domain": "zodgame.xyz",
            "name": cookie["name"],
            "value": cookie["value"],
            "path": "/",
        })

    #driver.refresh()
    driver.execute_script('window.open("https://zodgame.xyz/");')
    time.sleep(30)
    #driver.switch_to.window(driver.window_handles[1])
    #print(driver.title)
    
    formhash = driver.find_element(uc.selenium.webdriver.common.by.By.XPATH, '//input[@name="formhash"]').get_attribute('value')
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
    resp = driver.execute_script("return " + checkin_query)
    match = re.search('<div class="c">\n(.*?)</div>\n',resp["response"],re.S)
    message = match.group(1) if match is not None else "签到失败"
    print(message)
    assert message not in ("您今日已经签到，请明天再来", "恭喜你签到成功!")        
    driver.close()
    driver.quit()
    
if __name__ == "__main__":

    vdisplay = Xvfb(width=800, height=1280)
    vdisplay.start()
    cookie_string = sys.argv[1]
    if cookie_string:
        zodgame(cookie_string)
    else:
        print("未配置Cookie")
        assert False, "Please set the cookie."
    vdisplay.stop()
