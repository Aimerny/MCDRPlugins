# Offline Whitelist Reforged

> [!IMPORTANT]
> 自 v2.0.0 起，此插件增加依赖 [Whitelist API](./whitelist_api.md)。

一个简单小巧的离线服白名单管理插件，提供基本的白名单管理功能。

## 功能特性

- 简单易用的白名单管理
- 支持权限分级
- 完整的命令系统
- 与 Whitelist API 集成

## 依赖

- [Whitelist API](./whitelist_api.md) - 白名单管理 API

## 安装

1. 安装 [Whitelist API](./whitelist_api.md)
2. 下载插件
3. 将插件放入 MCDR 的 plugins 目录
4. 重载 MCDR 或重启服务器

## 配置

配置文件：`config/offline_whitelist_reforged/config.json`

```json
{
    "perms": {
        "on": 4,
        "off": 4,
        "list": 2,
        "add": 3,
        "remove": 3
    }
}
```

### 权限配置说明

| 命令 | 权限等级 | 对应身份 | 说明 |
|------|---------|----------|------|
| help | 0 | 所有人 | 显示帮助信息 |
| list | 2 | Helper | 查看白名单列表 |
| add | 3 | Admin | 添加白名单 |
| remove | 3 | Admin | 移除白名单 |
| on | 4 | Owner | 开启白名单 |
| off | 4 | Owner | 关闭白名单 |

> [!NOTE]
> - 权限等级遵循 MCDR 的权限系统
> - 控制台拥有与 Owner 相同的权限

## 命令

### 基础命令
```
!!wr help              # 显示帮助信息
!!wr list              # 显示白名单列表
!!wr add <player>      # 添加白名单
!!wr remove <player>   # 移除白名单
!!wr on                # 开启白名单
!!wr off               # 关闭白名单
```

### 命令示例

1. 添加白名单：
   ```
   !!wr add Steve
   ```

2. 查看白名单列表：
   ```
   !!wr list
   ```

3. 移除白名单：
   ```
   !!wr remove Steve
   ```

## 权限说明

### 玩家权限等级
- 等级 0：所有人
- 等级 2：Helper
- 等级 3：Admin
- 等级 4：Owner

### 命令权限要求
- `help`：无权限要求
- `list`：Helper 及以上
- `add`/`remove`：Admin 及以上
- `on`/`off`：仅 Owner

## 注意事项

1. 确保服务器为离线模式
2. 正确配置权限等级
3. 确保 Whitelist API 正常工作
4. 权限变更需要重载插件

## 常见问题

### Q: 为什么某些命令无法使用？
A: 检查以下几点：
- 确认你的权限等级
- 检查命令拼写是否正确
- 确认插件正常加载

### Q: 如何修改命令权限？
A: 在配置文件中修改对应命令的权限等级值：
- 0：所有人可用
- 2：Helper 及以上可用
- 3：Admin 及以上可用
- 4：仅 Owner 可用

## 更新日志

### v2.0.0
- 添加 Whitelist API 依赖
- 重构白名单管理逻辑
- 优化命令处理

### v1.0.0
- 初始版本发布
- 基本的白名单管理功能
- 简单的权限系统
