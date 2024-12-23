---
title: MirrorArchiveManager
---
# Mirror Archive Manager

一个基于 Prime Backup 插件的多镜像服务器管理插件，支持存档同步和启停控制。

## 功能特性

- 支持将主服的 Prime Backup 存档直接回档到镜像服
- 支持配置多个镜像服务器
- 支持通过指令控制镜像服的启停
- 自动化的存档同步机制

## 依赖

### Python 依赖
| 依赖项 | 版本要求 |
|-------|---------|
| requests | ^2.31.0 |
| fastapi | ^0.111.1 |

### MCDR 依赖
| 依赖项 | 版本要求 |
|-------|---------|
| mcdreforged | ^2.12.x |
| prime_backup | ^1.7.4 |

## 安装

1. 确保已安装 [Prime Backup](https://github.com/TISUnion/PrimeBackup)
2. 下载插件
3. 将插件放入 MCDR 的 plugins 目录
4. 安装依赖：
   ```bash
   pip install requests>=2.31.0 fastapi>=0.111.1
   ```
5. 配置主服和镜像服
6. 重载 MCDR 或重启服务器

## 配置说明

### 主服配置

```json
{
    "main": true,
    "mirrors": [
        {
            "name": "mirror",
            "host": "127.0.0.1",
            "port": 30076
        }
    ],
    "perms": {
        "start": 3,
        "stop": 3,
        "sync": 3
    }
}
```

### 镜像服配置

```json
{
    "main": false,
    "main_path": "../main",
    "port": 30076
}
```

### 配置项说明

| 配置项 | 说明 | 示例 | 必填 |
|-------|------|------|------|
| main | 是否为主服角色 | true | 是 |
| mirrors | 镜像服配置列表 | [] | 主服必填 |
| mirrors[].name | 镜像服名称 | "mirror" | 是 |
| mirrors[].host | 镜像服地址 | "127.0.0.1" | 是 |
| mirrors[].port | 镜像服端口 | 30076 | 是 |
| main_path | 主服路径 | "../main" | 镜像服必填 |
| port | 镜像服端口 | 30076 | 镜像服必填 |
| perms | 指令权限等级 | {"start": 3} | 主服必填 |

## 命令

- `!!mam start <server_name>` - 启动指定镜像服
- `!!mam stop <server_name>` - 停止指定镜像服
- `!!mam sync <server_name> <id>` - 将指定备份同步到镜像服

> 注：`server_name` 参数可选，不填时使用第一个配置的镜像服

## 使用示例

1. 启动镜像服：
   ```
   !!mam start mirror
   ```

2. 同步存档：
   ```
   !!mam sync mirror 123  # 将备份 #123 同步到 mirror 服务器
   ```

3. 停止镜像服：
   ```
   !!mam stop mirror
   ```

## 注意事项

1. 使用前请确保已正确配置镜像服务器
2. 镜像服必须处于 MCDR 进程启动的状态
3. 只有通过 MAM 停止的镜像服才能再通过 MAM 启动
4. 同步存档时需要指定有效的 Prime Backup 备份 ID

## 启动验证

### 主服日志
```
[MCDR] [INFO] [mirror_archive_manager]: MAM running with main role!
[MCDR] [INFO] [mirror_archive_manager]: MirrorArchiveManager initialization completed!
```

### 镜像服日志
```
[MCDR] [INFO] [mirror_archive_manager]: MAM running with mirror role!
[MCDR] [INFO] [mirror_archive_manager]: mirror http server started...
[MCDR] [INFO] [mirror_archive_manager]: mirror process...
[MCDR] [INFO] [mirror_archive_manager]: MirrorArchiveManager initialization completed!
```

## 更新日志

### v1.0.0
- 初始版本发布
- 支持多镜像服管理
- 支持存档同步
- 支持远程启停控制
