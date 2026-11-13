# Muse 视频生成：遭遇上游安全建议时的「粘性会话接续」与 100% 计费保障指南

在使用 `muse-director` 或 `muse-video-20s ~ 60s` 生成包含激烈冲突、史诗战斗或高张力剧情的长视频时，偶发会遇到如下报错信息：

> `upstream completed without readable video output: A different direction I can make for you in the same winter town, with the same dragon and cinematic look: ... Let me know if you'd like me to build the 60 seconds that way.`

本指南详细说明该现象的成因、网关内置的双层自动拦截机制、如何通过**粘性会话（Session Stickiness）**零成本复用已生成的设定图继续出片，以及中转网关的**零重叠扣费保障铁律**。

---

## 一、现象本质与网关双层自动拦截

### 1. 为什么会出现这段英文/中文提议？
当提示词中出现较激进的动作或冲突词汇（如 `attack`、`kill`、`destroy`、`blood`、写实肉搏/冷兵器砍杀等）触发上游安全策略时，Muse 云端 Agent 不会直接粗暴断开，而是在对话线程里礼貌地给出一个**温和化/电影化的替代分镜方案**（例如将写实破坏改为极光能量盘旋或奇幻光盾对决），并停下来等待确认（`"Let me know if you'd like me to build the 60 seconds that way."`）。

### 2. 网关底层已自动处理的 90% 场景（事前 + 事中）
在服务端驱动层，系统已经内置了两道全自动防线：
1. **事前零拒答改写法则注入**：要求云端 Agent 在调用底层生成工具前，主动将敏感冲突词转写为合规的科幻能量护盾、灵力光波或戏剧性走位并直接出片，严禁停下反问；
2. **事中自动追问确认**：当检测到 Agent 仍然返回了替代方案询问话术（匹配 `different direction`、`would you like me to`、`safer version`、`换个方向`、`如果你愿意，我可以` 等），网关会在同一线程内自动代发一轮确认指令（`"Yes, sounds good! Immediately generate, stitch, and upload that exact safer/adapted version right now..."`）并自动顺延超时窗口。

### 3. 什么时候需要客户端「粘性接续」？
仅在少数极端长耗时场景下（例如首轮已先花数分钟生成了角色设定图与彩色导演分镜符，随后触发替代方案追问并制作 6 段 60 秒视频，总耗时跨过单次任务截止线），任务最终以超时/无成片退出并返回上述提示。

此时：**云端沙盒 VM 里的角色设定图（`ref_*.png`）、导演分镜符（`director_board_act`）以及刚才 Agent 拟好的 60 秒和平版分镜方案仍然完整保存在该会话线程中！** 只要锁定同一会话发起一轮确认请求，就能直接接力出片，无需重做任何设定图。

---

## 二、标准操作姿势：从首轮起绑定 `conversation_id` 无缝接续

> **⚠️ 中转网关关键实践提示**：
> 在经由 OpenAI Video 异步任务网关（`POST /v1/videos`）调用时，**请务必将 `conversation_id`（或 `session_id`）放在 JSON Body 顶层（或 `multipart/form-data` 表单字段）中**，且**建议从第 1 轮提交时就带上自定义的业务会话 ID**（如 `"ep01_winter_dragon_01"`）。
> - **原因**：异步视频适配器（Type-55）会完整透传 JSON Body 与表单字段，但默认不会向后端转发自定义 HTTP Header 或 URL Query 参数；同时第 1 轮显式传入 `conversation_id` 能确保云端实例将该线程持久注册到会话映射表中，第 2 轮传入同一个 `conversation_id` 即可 100% 精准命中同一沙盒与同一对话线程。

### 第 1 轮：提交创作任务（在 JSON Body 携带自定义 `conversation_id`）

```bash
curl -sS https://api.oairegbox.cc/v1/videos \
  -H "Authorization: Bearer $OAIREGBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "muse-director",
    "conversation_id": "ep01_winter_dragon_001",
    "prompt": "Direct a 60-second cinematic fantasy sequence in a snow-covered winter town with the giant ice dragon...",
    "aspect_ratio": "16:9",
    "seconds": "60",
    "images": [
      "https://example.com/dragon_sheet.webp",
      "https://example.com/hero_sheet.webp"
    ]
  }'
```

### 第 2 轮：若第 1 轮因安全建议超时 `failed`，原样传入同一 `conversation_id` 采纳方案继续生成

无需重新上传或重新生成设定图，直接复用 `"conversation_id": "ep01_winter_dragon_001"` 并明确同意 Agent 给出的替代方向：

```bash
curl -sS https://api.oairegbox.cc/v1/videos \
  -H "Authorization: Bearer $OAIREGBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "muse-director",
    "conversation_id": "ep01_winter_dragon_001",
    "prompt": "Yes, please build that exact 60-second version you suggested! Soaring peacefully above the snow-covered rooftops with aurora-like light, reuse the existing character/dragon sheets in this workspace, stitch all clips, and upload the final MP4 immediately.",
    "aspect_ratio": "16:9",
    "seconds": "60"
  }'
```

*(附：如果是直连支持全量 Header/Query 路由的网关环境，除 JSON Body `conversation_id` 外，亦支持 `X-Conversation-Id` 请求头、`?session_id=...` URL 参数，或在先调用 `/v1/chat/completions` 讨论剧本后，将返回的 `mconv_...` 签名令牌直接填入 `/v1/videos` 的 JSON Body `"conversation_id"` 中实现「先聊分镜、再出成片」的跨端点无缝串联！)*

---

## 三、如何保证扣费 100% 正确？（计费安全铁律）

在中转网关的异步任务计费体系下，您完全无需担心“失败扣钱”或“重试双倍扣钱”：

1. **失败任务 100% 自动全额退费**：
   - 任何终态为 `failed` / `FAILURE` 的异步视频任务（无论是安全审核拒单、给出替代方案未产出可读 MP4，还是网络超时），网关异步轮询调度器（`relay_task`）在捕获终态的瞬间都会**自动全额退还预扣额度（Quota）**，并在账户流水中生成清晰的退费记录（`type=6`）。
   - 没有产出实际可播放的视频文件 = **净扣费严格为 0**。
2. **成片才核销，重试周期完全独立**：
   - 第 2 轮携带 `conversation_id` 发起的接续请求是一个全新的标准任务周期；
   - 前一笔失败任务的预扣款已全额退回，只有第 2 轮真正产出 MP4 视频直链并进入 `completed` / `SUCCESS` 状态后，系统才会按该模型的定价（或 `muse-director` 的实际产出清单 `img{I}_vid{V}_sec{S}`）结算一次费用，**绝无重叠扣费**。
