---
nav: 
  title: 插件
  order: 0
title: Bili Live Helper
---

# BiliLiveHelper | B站直播助手-弹幕姬

支持将b站直播间的弹幕同步到mc中

# ✨ 功能

**BiliLiveHelper**是一款~~功能丰富的~~MCDR插件,能够实现将[bilibili](https://bilibili.com)(以下简称"B站)
直播间中的弹幕信息实时同步到MC聊天板中.

- [x] 全异步拉取B站弹幕
- [x] 支持多个玩家订阅各自的直播间,弹幕消息单独发送,互不干扰
- [x] 玩家可以随时启停弹幕姬
- [ ] 支持查询订阅的直播间的状态
- [ ] admin轻松管理所有玩家的订阅信息
- [x] 游戏内通过直播姬账号发送弹幕,即时回应

# 🤖 指令
```
 ---------- BiliLiveHelper ----------
 >> !!blh [help] - | - 获取帮助
 >> !!blh bind <rid> - | - 绑定直播间id
 >> !!blh on - | - 启动直播弹幕姬
 >> !!blh off - | - 停止直播弹幕姬
 >> !!blh info - | - 查看我的直播间信息
 >> !!blh query - | - 查看其他玩家的直播间信息
 >> !!blh send <danmu> - | - 向直播间发送弹幕
 >> !!blh s <danmu> - | - 向直播间发送弹幕
 ------- Authored by Aimerny --------

```

# 📌 依赖

| python依赖项           | 版本      |
|---------------------|---------|
| mcdreforged         | ^2.12.0 |
| bilibili-python-api | ^16.3.0 |

| mcdr依赖项      | 版本      |
|--------------|---------|
| mcdreforged  | ^2.13.0 |

# 🔨 配置
```json5
{
    "enable": true,
    "data_file_path": "data.json",
    "console_output": true,
    "account": {
        "uid": 3546688564234249,
        "sessdata": "",
        "bili_jct": "",
        "buvid3": "",
        "ac_time_value": ""
    },
   "send":true
}
```
## 配置说明

1. `data_file_path`: 数据文件的路径.持久化的信息会保存到这个文件
2. `console_output`: 是否将接收到的弹幕输出到服务器控制台,如果设为false则需要在debug模式才能看到
3. `account`: 使用此插件需要一个真实的B站账号.`account`中是一些鉴权信息
   1. `uid`: 你的B站账号UID
   2. 其他: 参考 [获取 Credential 类所需信息](https://nemo2011.github.io/bilibili-api/#/get-credential)
4. `send`: 是否允许服务器成员使用上述配置中的`account`发送消息到对应直播间,默认为true

> B站的账号如果没有在其他地方登录基本不会过期,建议开一个小号做这件事情

# 🎨 功能预览

## 消息同步

![image-20240831032822332](https://cdn.jsdelivr.net/gh/aimerny/picgo@main/image-20240831032822332.png)

![image-20240831032855128](https://cdn.jsdelivr.net/gh/aimerny/picgo@main/image-20240831032855128.png)

## MC发送弹幕

![](https://cdn.jsdelivr.net/gh/aimerny/picgo@main/image-20240924021814482.png)

![](https://cdn.jsdelivr.net/gh/aimerny/picgo@main/image-20240924021842208.png)
