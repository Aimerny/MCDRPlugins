# Player Last Play

一个用于跟踪玩家最后游玩时间的 MCDR 插件。

## 功能

- 记录玩家的最后在线时间
- 显示玩家活跃度状态（非常活跃/一般/不活跃/潜水）
- 支持分页显示玩家列表
- 支持按时间排序
- 支持白名单玩家筛选
- 支持忽略特定玩家（如机器人）

## 依赖

- [online_player_api](https://github.com/MCDReforged/OnlinePlayerAPI)

## 安装

1. 下载插件
2. 将插件放入 MCDR 的 plugins 目录
3. 安装依赖：`pip install online-player-api`
4. 重载 MCDR 或重启服务器

## 配置

配置文件 `config.json`:

```json
{
  "active": 7,           // 7天内上线视为非常活跃
  "normal": 14,          // 7-14天内上线视为一般活跃
  "inactive": 21,        // 14-21天内上线视为不活跃，超过21天视为潜水
  "reverse": true,       // 是否倒序显示（从近到远）
  "pageSize": 10,        // 每页显示的玩家数量
  "ignorePlayerRegexes": ["^bot_.*$", "^Bot_.*$"],  // 忽略的玩家名正则表达式
  "only_whitelist_player": false  // 是否只统计白名单内的玩家
}
```

### 配置说明

- `active`、`normal`、`inactive`: 这三个值必须递增，否则配置验证会失败
- `pageSize`: 必须大于 0
- `ignorePlayerRegexes`: 支持正则表达式，默认忽略所有以 `bot_` 或 `Bot_` 开头的玩家名
- `only_whitelist_player`: 启用后只会统计白名单内的玩家

## 命令

- `!!plp help` - 显示帮助信息
- `!!plp list [页码]` - 显示玩家列表，可选择页码
- `!!plp get <玩家名>` - 获取指定玩家的最后游玩时间
- `!!plp clean <玩家名>` - 清除指定玩家的记录（需要权限等级 ≥ 3）

### 命令示例

```
!!plp list        # 显示第一页玩家列表
!!plp list 2      # 显示第二页玩家列表
!!plp get Steve   # 查看玩家 Steve 的最后游玩时间
!!plp clean Alex  # 清除玩家 Alex 的记录（需要权限）
```

## 显示效果

玩家列表示例：
```
------ 玩家列表 ------
|-> player1: 在线
|-> player2: 2023-11-18 (3天未上线)
|-> player3: 2023-11-15 (6天未上线)
|-> player4: 2023-11-10 (11天未上线)
<<< 第1页/共2页 >>>
```

玩家状态颜色：
- 绿色：在线或非常活跃（7天内有上线）
- 黄色：一般活跃（7-14天内有上线）
- 金色：不活跃（14-21天内有上线）
- 红色：潜水（超过21天未上线）

## 权限

- 使用 `!!plp help`、`!!plp list`、`!!plp get` 命令无需特殊权限
- 使用 `!!plp clean` 命令需要权限等级 ≥ 3

## 数据存储

玩家数据存储在 `data.json` 文件中，格式如下：

```json
{
  "player_list": {
    "player1": "2023-11-18",
    "player2": "2023-11-15"
  }
}
```

## 注意事项

1. 如果启用了 `only_whitelist_player` 选项：
   - 如果服务器的 `whitelist.json` 不存在或为空，将无法记录任何玩家数据
   - 已存在的非白名单玩家数据不会自动清除，需要手动使用 `!!plp clean` 命令清除

2. 插件依赖 `online_player_api`，请确保正确安装并启用

3. 修改配置后需要重载插件才能生效

## 常见问题

### Q: 为什么某些玩家的记录没有更新？
A: 可能的原因：
- 玩家名匹配了 `ignorePlayerRegexes` 中的规则
- 启用了 `only_whitelist_player` 但玩家不在白名单中
- 玩家异常退出服务器（崩溃等情况）

### Q: 如何修改玩家状态的时间阈值？
A: 在 `config.json` 中修改 `active`、`normal`、`inactive` 的值，注意这三个值必须递增。

### Q: 如何清除所有数据重新开始记录？
A: 删除 `data.json` 文件并重启服务器，或者使用 `!!plp clean` 命令逐个清除。

## 更新日志

### v1.0.0
- 初始版本发布
- 基本的玩家时间跟踪功能
- 分页显示支持
- 白名单集成

### v1.1.0
- 添加配置验证
- 改进命令提示
- 优化代码结构
- 修复已知问题
