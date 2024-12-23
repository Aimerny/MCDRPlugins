---
nav: 
  title: 插件
  order: 0
title: Bili Live Helper
---

# BiliLiveHelper | B站直播助手-弹幕姬

<Alert type="error">
此插件仅用于学习交流，请勿用于违法犯罪或其他不良用途。
</Alert>

一个用于将 B 站直播弹幕同步到 MC 聊天栏的 MCDR 插件。

## 功能特性

- ✅ 全异步拉取 B 站弹幕
- ✅ 支持多个玩家订阅各自的直播间
- ✅ 玩家可以随时启停弹幕姬
- ✅ 游戏内通过直播姬账号发送弹幕
- 🚧 支持查询订阅的直播间状态
- 🚧 管理员批量管理订阅信息

## 依赖

### Python 依赖
| 依赖项 | 版本要求 |
|-------|---------|
| mcdreforged | ^2.12.0 |
| bilibili-python-api | ^16.3.0 |

### MCDR 依赖
| 依赖项 | 版本要求 |
|-------|---------|
| mcdreforged | ^2.13.0 |

## 安装

1. 下载插件
2. 将插件放入 MCDR 的 plugins 目录
3. 安装依赖：
   ```bash
   pip install bilibili-python-api>=16.3.0
   ```
4. 配置 B 站账号信息
5. 重载 MCDR 或重启服务器

## 配置

配置文件：`config/bili_live_helper/config.json`

```json
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
    "send": true
}
```

### 配置项说明

| 配置项 | 说明 | 类型 | 默认值 |
|-------|------|------|--------|
| enable | 是否启用插件 | boolean | true |
| data_file_path | 数据文件路径 | string | "data.json" |
| console_output | 是否输出弹幕到控制台 | boolean | true |
| account | B 站账号配置 | object | - |
| account.uid | B 站账号 UID | number | - |
| account.sessdata | 登录凭证 | string | - |
| account.bili_jct | 登录凭证 | string | - |
| account.buvid3 | 登录凭证 | string | - |
| account.ac_time_value | 登录凭证 | string | - |
| send | 是否允许发送弹幕 | boolean | true |

<Alert type="info">
B 站账号凭证获取方法请参考：[获取 Credential 类所需信息](https://nemo2011.github.io/bilibili-api/#/get-credential)
</Alert>

## 命令

### 基础命令
```
!!blh help           # 获取帮助
!!blh bind <rid>     # 绑定直播间 ID
!!blh on             # 启动直播弹幕姬
!!blh off            # 停止直播弹幕姬
!!blh info           # 查看我的直播间信息
!!blh query          # 查看其他玩家的直播间信息
```

### 弹幕发送
```
!!blh send <danmu>   # 向直播间发送弹幕
!!blh s <danmu>      # 向直播间发送弹幕（简写）
```

## 使用示例

1. 绑定直播间：
   ```
   !!blh bind 12345
   ```

2. 启动弹幕姬：
   ```
   !!blh on
   ```

3. 发送弹幕：
   ```
   !!blh s 你好，直播间！
   ```

4. 查看信息：
   ```
   !!blh info
   ```

## 效果展示

### 弹幕同步
游戏内可以实时看到直播间的弹幕消息：
```
[直播姬] <用户A> 主播好强！
[直播姬] <用户B> 666
```

### 弹幕发送
从游戏内发送的消息会实时显示在直播间：
```
!!blh s 主播加油！
```

## 注意事项

<Alert type="warning">
1. 建议使用小号作为弹幕姬账号
2. 账号凭证通常不会经常过期
3. 为避免影响性能，建议适度使用
4. 确保账号凭证的安全性
</Alert>

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本的弹幕同步功能
- 支持多直播间订阅
- 支持弹幕发送功能

### v1.1.0
- 优化异步处理机制
- 改进错误处理
- 添加更多调试信息
- 支持控制台输出开关
