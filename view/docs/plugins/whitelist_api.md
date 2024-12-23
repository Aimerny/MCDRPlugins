# Whitelist API

一个通用的白名单管理 API 插件，提供完整的白名单操作功能。

## 功能特性

- 自动跟踪 `whitelist.json` 文件变化并同步列表
- 支持在线/离线模式自适应
- 提供完整的白名单管理 API
- 支持正版和离线玩家

## 主要功能

- ✅ 获取白名单内所有成员
- ✅ 获取白名单内所有成员的玩家名
- ✅ 获取白名单内所有成员的 UUID 列表
- ✅ 开启/关闭服务器白名单功能
- ✅ 添加正版玩家白名单
- ✅ 添加离线玩家白名单
- ✅ 移除玩家白名单
- ✅ 根据服务器在线/离线自适应添加白名单

## 依赖

| 依赖项 | 版本要求 |
|-------|---------|
| mcdreforged | ^2.6.0 |
| watchdog | ^5.0.2 |

## 安装

1. 下载插件
2. 将插件放入 MCDR 的 plugins 目录
3. 安装依赖：
   ```bash
   pip install watchdog>=5.0.2
   ```
4. 重载 MCDR 或重启服务器

## API 使用

```python
def on_load(server, old):
    # 获取 API 实例
    whitelist_api = server.get_plugin_instance('whitelist_api')
    
    # 获取白名单信息
    whitelist_api.get_whitelist()           # 获取所有成员
    whitelist_api.get_whitelist_uuids()     # 获取所有 UUID
    whitelist_api.get_whitelist_names()     # 获取所有玩家名
    
    # 添加白名单
    whitelist_api.add_player('Aimerny')     # 自适应添加
    whitelist_api.add_offline_player('Aimerny')  # 添加离线玩家
    whitelist_api.add_online_player('Aimerny')   # 添加正版玩家
    
    # 移除白名单
    whitelist_api.remove_player('Aimerny')
    
    # 白名单功能开关
    whitelist_api.enable_whitelist()        # 开启白名单
    whitelist_api.disable_whitelist()       # 关闭白名单
```

## API 方法说明

### 获取白名单信息

- `get_whitelist()`: 获取白名单内所有成员的完整信息
- `get_whitelist_uuids()`: 获取白名单内所有成员的 UUID 列表
- `get_whitelist_names()`: 获取白名单内所有成员的玩家名列表

### 管理白名单

- `add_player(name)`: 根据服务器模式自动选择添加方式
- `add_offline_player(name)`: 添加离线玩家
- `add_online_player(name)`: 添加正版玩家
- `remove_player(name)`: 移除玩家的白名单

### 白名单功能控制

- `enable_whitelist()`: 开启服务器白名单功能
- `disable_whitelist()`: 关闭服务器白名单功能

## 使用此 API 的插件

- [Offline Whitelist Reforged](./offline_whitelist_reforged.md) - 离线服白名单插件
- [KookIn](./kookin.md) - Kook 平台的 MC 机器人

## 注意事项

1. 插件会自动监控 `whitelist.json` 文件的变化
2. API 会自动处理在线/离线模式的差异
3. 所有操作都是线程安全的

## 更新日志

### v1.0.0
- 初始版本发布
- 完整的白名单管理功能
- 自动文件监控
- 在线/离线模式支持
