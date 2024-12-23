# Kookin

> [!NOTE]
> 自 v1.0.0 起，此插件增加依赖 [Whitelist API](./whitelist_api.md)，移除对 [Kook API](./kook_api.md) 的依赖。
> 更新亮点：v1.0.0 摒弃了 v0.x 版本冗长的链路，从与 kook 网关的交互到对消息事件的处理全都内聚在 Kookin 插件中。

一个功能丰富的 MCDR 服务器管理插件，支持 Kook 与 MC 服务器的双向通信和管理功能。

## 功能特性

### MC 端功能
- 发送消息到指定 Kook 频道组
- 将所有 MC 的聊天消息同步到指定 Kook 频道组

### Kook 端功能
- ✅ 查看 MC 服务器中在线玩家列表
- ✅ 离线时向服务器中发送消息
- ✅ 管理服务器白名单（仅管理员可用）
- ✅ 远程执行服务端指令（仅管理员可用）
- ✅ 远程执行 MCDR 指令（仅管理员可用）

### 计划功能
- 支持配置离线/在线服以支持自动加白名单
- 一套基于 Kook 的审核、加白、绑定流程
- 更多功能开发中...

## 依赖

- [Whitelist API](./whitelist_api.md) - 白名单管理 API

## 安装

1. 下载插件
2. 将插件放入 MCDR 的 plugins 目录
3. 安装依赖插件
4. 创建并修改配置文件
5. 重载 MCDR 或重启服务器

## 配置

配置文件路径：`$MCDR/config/kookin/conf.json`

```json
{
    "token": "your_bot_token",
    "prefixes": ["/"],
    "admin_channel": [
        {
            "channel_name": "管理频道",
            "channel_id": "3168870203890905"
        }
    ],
    "public_channel": [
        {
            "channel_name": "公共频道",
            "channel_id": "3168870203890906"
        }
    ],
    "sync_chat_channel": [
        {
            "channel_name": "同步频道",
            "channel_id": "3168870203890907"
        }
    ],
    "admins": ["Aimerny#0476"],
    "server_name": "Survival"
}
```

### 配置项说明

| 配置项 | 说明 | 类型 | 示例 |
|-------|------|------|------|
| token | 机器人 Token | string | 从 Kook 开发者中心获取 |
| prefixes | 指令前缀 | Array[string] | ["/"] |
| admin_channel | 服务器管理频道 | Array[channelInfo] | - |
| public_channel | 服务器公共频道 | Array[channelInfo] | - |
| sync_chat_channel | 服务器消息同步频道 | Array[channelInfo] | - |
| channel_name | 频道名称备注 | string | "频道A" |
| channel_id | 频道 ID | string | "3168870203890905" |
| admins | 管理员列表 | Array[string] | ["Aimerny#0476"] |
| server_name | Kook 展示服务器名 | string | "Survival" |

## 命令

### MC 端命令
```
!!kk <msg>  # 发送消息到对应 Kook 服务器
```

### Kook 端命令

#### 基础命令
```
/help       # 查询指令帮助
/bind       # 成员绑定
/whitelist  # 白名单管理
/list       # 在线玩家列表
/mc <msg>   # 发送消息到服务器（需要先绑定账号）
```

#### 管理员命令
```
/execute <command>  # 执行服务器指令
/mcdr <mcdr_cmd>   # 执行 MCDR 指令
```

### 命令示例

```bash
# 白名单管理
/whitelist add Aimerny
/whitelist remove Aimerny

# 服务器命令执行
/execute ban Aimerny
/execute whitelist add Aimerny

# MCDR 命令执行
/mcdr !!kk 这是通过 kook 令服务器发送的消息
/mcdr !!pb make 存档
```

## 频道说明

1. 公共频道：
   - 只有使用 `!!kk` 指令的消息会被发送到此频道
   - 只有使用 `/mc` 指令的消息会发送到服务器

2. 同步频道：
   - 所有游戏内消息都会被发送至此频道
   - 此频道中的所有消息都会同步到游戏中（指令除外）

## 获取频道 ID

1. 打开网页端 Kook
2. 进入指定频道
3. 从 URL 中获取 ID：
   ```
   https://www.kookapp.cn/app/channels/8474959284287105/3168870203890905
   ```
   - guild_id: 8474959284287105
   - channel_id: 3168870203890905

> [!NOTE]
> Kookin 配置中只需要用到 `channel_id`，可以跨多个 Kook 服务器使用同一个 Kookin 实例。

## 注意事项

1. 确保机器人 Token 正确且有效
2. 管理员命令只能由配置文件中指定的管理员使用
3. 发送消息到服务器需要先完成账号绑定

## 更新日志

### v1.0.0
- 移除对 Kook API 的依赖
- 添加对 Whitelist API 的依赖
- 重构消息处理机制
- 优化插件架构

### v0.x
- 初始版本
- 基本的消息同步功能
- 简单的服务器管理功能
