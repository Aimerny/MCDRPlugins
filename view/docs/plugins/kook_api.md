---
nav: 插件
---

# Kook API

> [!NOTE]
> 子插件 kookin 在 v1 版本后不再依赖此插件，此插件暂停更新。如果你有更好的思路，欢迎提交 PR。

一个连接 Kook 和 MCDR 的 API 插件，通过 Kook 机器人事件代理服务将 Kook 服务器（频道）的事件接入 MCDR。

## 功能特性

- 实现 Kook 文本事件的解析与转发
- 提供发送频道消息的 API
- 支持 MC 与 Kook 双向通信
- 支持自定义事件处理

## 依赖

- [Elix](https://github.com/Aimerny/Elix) - Kook 机器人事件代理服务

## 安装

1. 启动 Kook 机器人事件代理服务 [Elix](https://github.com/Aimerny/Elix)
2. 下载插件并放入 MCDR 的 plugins 目录
3. 创建并修改配置文件
4. 重载 MCDR 或重启服务器

## 配置

配置文件路径：`$MCDR/config/kook_api/conf.json`

```json
{
    "kook_host": "127.0.0.1",
    "kook_port": 9000,
    "api_port": 9001
}
```

### 配置项说明

| 配置项 | 说明 | 示例 | 必填 |
|-------|------|------|------|
| kook_host | Kook 机器人代理地址 | "127.0.0.1" | 是 |
| kook_port | Kook 机器人代理 WebSocket 端口 | 9000 | 是 |
| api_port | Kook 机器人代理 HTTP 端口 | 9001 | 是 |

## API 使用

### 事件监听

下游插件可以通过订阅 `kook_api.on_message` 事件来接收消息：

```python
def on_load(server: PluginServerInterface, old_plg):
    server.register_event_listener('kook_api.on_message', on_message)
    
def on_message(server: PluginServerInterface, raw_content: str, event: Event):
    server.logger.info(f"kook message event received: {raw_content}, event: {event}")
```

### 事件数据结构

接收到的事件数据包含：
- `raw_content`: 消息的原始文本内容
- `event`: 完整的事件数据对象

## 使用此 API 的插件

- [KookIn](./kookin.md) - Kook 与 MC 消息互通插件（v1 版本后不再依赖）

## 注意事项

1. 确保 Elix 服务正常运行
2. 检查配置文件中的端口设置
3. 注意处理事件监听中的异常情况

## 常见问题

### Q: 无法连接到 Kook 机器人代理服务？
A: 检查以下几点：
- Elix 服务是否正常运行
- 配置文件中的地址和端口是否正确
- 网络连接是否正常

### Q: 如何测试 API 是否正常工作？
A: 可以通过以下步骤：
1. 启动 MCDR 和插件
2. 检查日志中是否有连接成功的信息
3. 在 Kook 频道发送消息，观察 MCDR 日志

## 更新日志

### v1.0.0
- 初始版本发布
- 实现基本的事件转发功能
- 提供消息发送 API

### v1.1.0
- 改进事件处理机制
- 优化配置结构
- 添加更多调试信息
