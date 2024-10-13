import re
import sys
import nodriver
from nodriver import cdp

async def zodgame_checkin(tab, formhash):

    checkin_url = "https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=0"    

    checkin_query = """
        (async function() {
            const formdata = new FormData();
            formdata.append("formhash","%s");
            formdata.append("qdxq","kx");

            const result = await fetch('%s', {
                method: 'POST',
                body: formdata
            })
            .then(response => {
                return response.text();
            })

            return result;
        })();
        """ % (formhash, checkin_url)

    resp = await tab.evaluate(checkin_query, await_promise=True, return_by_value=True)
    match = re.search('<div class="c">\n(.*?)</div>\n', resp, re.S)
    message = match[1] if match is not None else "签到失败"
    #print(f"【签到】{message}")

    return "恭喜你签到成功!" in message or "您今日已经签到，请明天再来" in message

async def zodgame_task(broswer):

    async def show_task_reward(broswer):
        tab = await broswer.get("https://zodgame.xyz/plugin.php?id=jnbux", new_tab=True)
        try:
            reward_li = (await tab.find('//li[contains(text(), "点币: ")]', timeout=60))
            print(f"【Log】{reward_li.text}")
        except:
           pass

    jnbux_tab = await broswer.get("https://zodgame.xyz/plugin.php?id=jnbux")
    
    try:
        join_task = await jnbux_tab.find_all('//a[text()="参与任务"]')
    except:
        join_task = []
        success = True

    if len(join_task) == 0:
        #print("【任务】所有任务均已完成。")
        #return success
        pass

    for idx, a in enumerate(join_task):
        print(a.attrs)
        on_click = a.attrs["onclick"]
        print(on_click)
        #await a.click()
        try:
            tab = broswer.tabs[-1]
            try:
                await tab.find('//div[text()="成功！"', timeout=240)
            except:
                #print(f"【Log】任务 {idx+1} 广告页检查失败。")
                pass

            try:     
                check_url = re.search("""showWindow('check', '(.*)');""", on_click, re.S)[1]
                tab = await tab.get(f"https://zodgame.xyz/{check_url}")
                await tab.find('//p[contains(text(), "检查成功, 积分已经加入您的帐户中")] | //title[text()="BUX广告点击赚积分 - ZodGame论坛 - Powered by Discuz!"]')
            except:
                #print(f"【Log】任务 {idx+1} 确认页检查失败。")
                pass

            print(f"【任务】任务 {idx+1} 成功。")
        except Exception as e:
            success = False
            #print(f"【任务】任务 {idx+1} 失败。", type(e))

    await show_task_reward(broswer)

    return success

async def zodgame(cookie_string):

    browser = await nodriver.start(
        headless=False,
        sandbox=False
    )
    tab = await browser.get('https://zodgame.xyz')

    # Log in with cookie string
    if cookie_string.startswith("cookie:"):
        cookie_string = cookie_string[len("cookie:"):]
    cookie_string = cookie_string.replace("/","%2")
    cookie_dict = [
        {"name": x.split('=')[0].strip(), "value": x.split('=')[1].strip()} 
        for x in cookie_string.split(';')
    ]
    cookies = [
        cdp.network.CookieParam(domain = 'zodgame.xyz', name = cookie["name"], value = cookie["value"], path = '/') 
        for cookie in cookie_dict if cookie["name"] in ["qhMq_2132_saltkey", "qhMq_2132_auth"]
    ]
    #await browser.cookies.set_all(cookies)
    await tab.send(cdp.storage.set_cookies(cookies))
    await tab.reload()

    formhash = (await tab.find('//input[@name="formhash"]', timeout=180)).attrs["value"]

    #await zodgame_checkin(tab, formhash)
    await zodgame_task(browser)

    await tab.sleep(180)

if __name__ == '__main__':
    cookie_string = sys.argv[1]
    assert cookie_string
    
    nodriver.loop().run_until_complete(zodgame(cookie_string))
