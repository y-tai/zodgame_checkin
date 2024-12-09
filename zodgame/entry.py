import nodriver as uc
import os
import requests
import json
import sys
import random
from nodriver.core.config import find_chrome_executable

def cmd_start_brower(chrome_path, port, user_data_dir):
  chrome_path_temp = chrome_path.replace('\chrome.exe', '')
  start_params = r'cd {} && chrome.exe --remote-debugging-port={} --user-data-dir={} --no-first-run --disable-infobars --allow-file-access-from-files --no-default-browser-check --profile-directory=Profile1'
  os.popen(start_params.format(chrome_path_temp, port, user_data_dir))

def get_session_url(chrome_path, port, user_data_dir):
  url = f'http://127.0.0.1:{port}/json/version'
  try:
    res = requests.get(url)
    print(res.text)
    webSocketDebuggerUrl = json.loads(res.text)['webSocketDebuggerUrl']
  except Exception as e:
    print('error:', e)
    cmd_start_brower(chrome_path, port, user_data_dir)
    time.sleep(random.randint(4, 6))

async def main1():
  config = uc.Config()
  config.host = "127.0.0.1"
  config.port = 9315
  config.user_data_dir = user_data_dir
  driver = await uc.start(config=config)
  page = await driver.get('https://www.bing.com')
  get_content = await page.get_content()
  print(get_content)
  await page.scroll_down(150)

port = 9315
chrome_path = find_chrome_executable()
current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
user_data_dir = os.path.join(current_path, "pyppeteer_chrome")

get_session_url(chrome_path, port, user_data_dir)
uc.loop().run_until_complete(main1())
