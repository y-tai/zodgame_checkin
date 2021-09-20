# zodgame_checkin
Zodgame automatic check-in using github action


### 1. 添加 Cookie 至 Secrets

- 首先通过F12抓取到Cookie，随后在项目页面，依次点击`Settings`-->`Secrets`-->`New secret`
- 建立名为`ZODGAME_COOKIE`的 secret，值为`步骤1`中复制的`Cookie`内容，最后点击`Add secret`
- secret名字必须为`ZODGAME_COOKIE`！
- secret名字必须为`ZODGAME_COOKIE`！
- secret名字必须为`ZODGAME_COOKIE`！
### 2. 启用 Actions

- 本仓库 Actions 默认为关闭状态，需要通过 `Settings`-->`Actions`-->`Allow all actions`开启。
- Fork 之后需要手动执行一次，若成功运行其才会激活。
返回项目主页面，点击上方的`Actions`，再点击左侧的`Zod Game`，再点击`Run workflow`
至此，部署完毕。
- 本项目由WorkFlow控制，每日8时自动执行。
