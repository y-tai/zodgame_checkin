# zodgame_checkin
Zodgame automatic check-in using github action

### 日志

- 2021.9.22 ZodGame更新反爬机制，本项目暂不可用。

- 2021.9.26 ZodGame回退反爬机制，本项目 **`目前可用`**。

- 2021.10.8 更新了Chrome Driver的下载方式。

- 2021.11.11 更换了自动签到的核心脚本。如果还是不能签到，请手动更新一遍Cookie（针对11月份之后）。
【当前版本由于Xvfb和undetected_chromedriver的冲突，有一定概率会无法创建driver，从而签到失败，介意的朋友增加签到频率即可，或者手动re-run jobs】

## 使用方法
### 1. 添加 Cookie 至 Secrets

- 首先通过F12抓取到在浏览器中抓取`Cookie`.
<p align="center">
  <img src="imgs/Step1.png" />
</p>

- 在项目页面，依次点击`Settings`-->`Secrets`-->`New secret`
- 建立名为`ZODGAME_COOKIE`的 secret，值为复制的`Cookie`内容，最后点击`Add secret`
- secret名字必须为`ZODGAME_COOKIE`！
<p align="center">
  <img src="imgs/Step2.png" />
</p>
<p align="center">
  <img src="imgs/Step3.png" />
</p>

### 2. 启用 Actions

- 本项目由Workflow控制，每日8时自动执行。
- 本项目目前可以正常运行，如果有其他使用问题请在Issues留言。
