# Muse 全模态中转 API 操作手册（`muse-fast` 分组）

本手册面向通过 OpenAI 兼容聚合中转网关（如 `https://api.oairegbox.cc` / `https://newapi-2.oairegbox.cc`）接入 **Meta Muse（`muse-fast` 分组，亦已纳入 `auto` 分组）** 全部 **16 款模型** 的开发者与创作者。

---

## 一、16 款全模态模型矩阵与计费标准

| 模型 ID | 模态与核心用途 | 标准调用端点 | 计费方式 | 参考价格 / 倍率 | 规格与时长边界 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `muse-chat` | 多模态对话 / 识图 / 代码沙盒 | `POST /v1/chat/completions` | 按量 (Token) | 输入 `¥2.00/M` (1x) · 输出 `¥8.00/M` (4x) | 支持视觉识图、OpenAI `tools` 工具调用、`mconv_...` 会话粘性 |
| `muse-agent`<br>*(别名: `muse-spark` / `muse-bot`)* | 全功能自主云端 Agent（建站 / 漫剧编排） | `POST /v1/chat/completions` | 按量 (Token) + 媒体折算 | 输入 `¥4.00/M` (2x) · 输出 `¥16.00/M` (8x) | 开放完整云端 Linux VM；对话内若生成图/视频/播客按单价折算叠加 Token |
| `muse-image` | 原生 2K 级文生图 & 多参考图编辑 | `POST /v1/images/generations`<br>`POST /v1/images/edits` | 按次 | `¥0.03 / 张` | 原生最高 2K WebP 直出（支持 `png`/`jpeg`/`webp` 容器转换，最多 4 张参考图） |
| `muse-video` | 单段原生 720p HD 有声视频（`≤10s`） | `POST /v1/videos` | 按次 | `¥0.30 / 个` | `seconds`: `"1"`~`"10"` 无损裁剪；传 `>10s` 或 `video_url` 续写直接返 `400` |
| `muse-video-20s` | 20 秒长视频 / 源视频续写（总长 `≤20s`） | `POST /v1/videos` | 按次 | `¥0.50 / 个` | 2 段 720p 24fps 末帧接力无缝拼接；续写要求源视频 `< 19s` |
| `muse-video-30s` | 30 秒长视频 / 源视频续写（总长 `≤30s`） | `POST /v1/videos` | 按次 | `¥0.60 / 个` | 3 段无缝拼接；续写要求源视频 `< 29s` |
| `muse-video-40s` | 40 秒长视频 / 源视频续写（总长 `≤40s`） | `POST /v1/videos` | 按次 | `¥0.80 / 个` | 4 段无缝拼接；续写要求源视频 `< 39s` |
| `muse-video-50s` | 50 秒长视频 / 源视频续写（总长 `≤50s`） | `POST /v1/videos` | 按次 | `¥1.00 / 个` | 5 段无缝拼接；续写要求源视频 `< 49s` |
| `muse-video-60s` | 60 秒长视频 / 源视频续写（总长 `≤60s`） | `POST /v1/videos` | 按次 | `¥1.20 / 个` | 6 段无缝拼接；续写要求源视频 `< 59s` |
| `muse-director`<br>*(别名: `muse-drama` / `muse-manju` / `muse-video-pro`)* | AI 漫剧 / 短剧智能导演（剧本自动分镜 + 配音 + 拼接） | `POST /v1/videos` | 按实际产出动态结算 | 过程生图 `¥0.03 / 张`<br>+ 成片时长 `¥0.02 / 秒` | 支持剧本文件/文本 + 最多 6 张人设/分镜图，`10–90s` 自然剧情节拍切镜，按 `img{I}_vid{V}_sec{S}` 清单精确计费 |
| `muse-podcast` | AI 双人/多人深度播客生成（MP3） | `POST /v1/videos` | 按次 | `¥0.30 / 期` | 自动调研撰稿并合成多音色对谈 MP3，结果位于 `video_url` / `url` / `/content` |
| `muse-invite` | 邀请码自动核销助力 | `POST /v1/chat/completions` | 按次 | `¥0.09 / 次` | 传入邀请码/链接自动分配未核销账号助力，无效码自动回退不扣费 |
| `muse-tts` | Avocado v2 超拟真语音合成 | `POST /v1/audio/speech` | 按次 | `¥0.02 / 次` | 音色：`alloy`、`nova`、`echo`、`fable`、`coral` 等；格式：`mp3`/`wav`/`opus`/`pcm` |
| `muse-asr` | 极速多语种语音识别转写 (STT) | `POST /v1/audio/transcriptions` | 按次 | `¥0.02 / 次` | 兼容 `mp3`/`wav`/`ogg`/`m4a`/`flac`/`webm` |
| `muse-audio` | 多模态语音提问 & 语音回复 | `POST /v1/chat/completions` | 按量 (Token) | 输入 `¥5.00/M` (2.5x) · 输出 `¥20.00/M` (10x) | 支持 `input_audio` 提问，同步返回文本回答 + Avocado v2 语音回复 |
| `muse-live` | 全双工低延迟实时语音流 | `WS /v1/realtime?model=muse-live` | 按量 (Token) | 输入 `¥5.00/M` (2.5x) · 输出 `¥20.00/M` (10x) | 兼容 OpenAI Realtime WebSocket 双向语音协议 |

---

## 二、图像生成与编辑参数（`muse-image`）

支持 `POST /v1/images/generations`（JSON）与 `POST /v1/images/edits`（`multipart/form-data` 或 JSON）：

| 参数名 | 类型 | 必选 | 取值与生效说明 |
| :--- | :--- | :--- | :--- |
| `model` | `string` | 是 | `"muse-image"` |
| `prompt` | `string` | 是 | 画面描述提示词（支持中英文） |
| `aspect_ratio` / `ratio` / `size` | `string` | 否 | 原生画幅比例：`"1:1"`（约 `1600×1600`）、`"16:9"`（`2048×1152`）、`"9:16"`（`1152×2048`）、`"4:3"`、`"3:4"`、`"3:2"`、`"2:3"`；原样返回原生最高 2K 像素，不做插值超分 |
| `image` / `images` / `reference_images` | `string` / `array` | 否 | **最多 4 张**参考图，支持公网 `https://` URL、`data:image/webp;base64,...` 或 multipart 文件上传 |
| `style` | `string` | 否 | 风格指令，如 `"photorealistic"`、`"anime"`、`"cinematic"`、`"3d"` |
| `negative_prompt` | `string` | 否 | 负面提示词（排除不需要的瑕疵或元素） |
| `output_format` | `string` | 否 | `"webp"`（默认原生直出）、`"png"`、`"jpeg"`（无损容器格式转换；不支持 `background="transparent"` 本地抠图） |
| `n` | `integer` | 否 | 单次生成张数（`1`~`4`，默认 `1`） |
| `seed` | `integer` | 否 | 随机种子 |
| `response_format` | `string` | 否 | `"url"`（默认）或 `"b64_json"` |

---

## 三、视频生成、长视频续写与漫剧导演参数（`POST /v1/videos`）

提交异步任务后获取 `id` / `task_id`，通过 `GET /v1/videos/{task_id}` 轮询状态（建议轮询间隔 `4~5s`，长视频超时上限设为 **至少 15 分钟**，`muse-director` 设为 **25 分钟**）。

### ⚠️ 三大防踩坑硬规则
1. **参考图与首尾帧必须放在 JSON 顶层**：切勿包裹进 `metadata.content` 或 `metadata.images`，否则部分客户端封装容易导致多图退化为文生视频。
2. **`seconds` 请统一传字符串**：例如 `"seconds": "8"`、`"seconds": "50"`，避免在 OpenAI Video 严格类型层触发 `invalid_json`。
3. **续写模式（`video_url`）下 `seconds` 代表「成片总时长」而非增量秒数**：源视频必须比目标档位短至少 1 秒（`20s` 档 `<19s`、`30s` 档 `<29s`、`40s` 档 `<39s`、`50s` 档 `<49s`、`60s` 档 `<59s`），单文件 `≤20MB`。

### 完整参数表

| 参数名 | 类型 | 必选 | 取值与生效说明 |
| :--- | :--- | :--- | :--- |
| `model` | `string` | 是 | `"muse-video"` / `"muse-video-20s"` ~ `"muse-video-60s"` / `"muse-director"` |
| `prompt` | `string` | 是 | 镜头动作、光影与环境音效描述（`muse-director` 传 `script` 文件时可省略） |
| `aspect_ratio` / `ratio` / `size` | `string` | 否 | `"16:9"`（横屏 `1280×720` / `1248×704`）、`"9:16"`（竖屏 `720×1280` / `704×1248`）、`"1:1"`、`"4:3"`、`"3:4"` |
| `seconds` | `string` | 否 | 字符串秒数，如 `"5"`、`"10"`、`"30"`、`"60"`（`muse-director` 支持 `"10"`~`"90"`） |
| `first_image_url` / `image` / `first_frame` | `string` / `file` | 否 | **JSON 顶层**首帧参考图（URL / Base64 Data URL / multipart 文件） |
| `last_image_url` / `last_frame` | `string` / `file` | 否 | **JSON 顶层**尾帧参考图 |
| `images` / `reference_images` | `array` | 否 | **JSON 顶层**多参考图数组（**最多 6 张**），用于跨镜头锁定角色外貌、服装与场景 |
| `video_url` / `input_video` | `string` / `file` | 否 | **JSON 顶层**源视频（仅 `muse-video-20s ~ 60s` 支持续写，`≤20MB`） |
| `mute_voice` | `boolean` | 否 | **人物静音控制（默认 `false` 有声）**：传 `true` 时画面人物保留自然口型表演（方便后期贴配音），但剥离人物说话人声，完整保留环境音（SFX）、动作音（Foley）与配乐（BGM） |
| `style_preset` | `string` | 否 | 内置 7 套画风预设：`"none"`、`"cinematic_realistic"`、`"2d_anime"`、`"3d_xianxia"`、`"american_comic"`、`"cyberpunk_neon"`、`"ecommerce_ugc"` |
| `custom_style` | `string` | 否 | 自定义补充画风文本（可与 `style_preset` 叠加） |
| `skill_preset` | `string` / `array` | 否 | 内置 **16 套电影学与开源导演技能 ID**，支持逗号叠加多选（如 `"occlusion_wipe,micro_drama_hook,emotion_micro_acting"`）或传 `"none"` 纯原样模式；详见 `04-DIRECTOR_SKILLS_AND_24_REPOS.md` |
| `custom_skill` | `string` | 否 | 自定义运镜、分镜或转场指令（可与 `skill_preset` 叠加） |
| `camera_motion` / `negative_prompt` / `seed` | `string` / `int` | 否 | 运镜控制（如 `"zoom_in"`、`"pan_left"`、`"orbit"`）、负向提示词、随机种子 |
| `script` / `script_url` / `storyboard` / `character_bible` | `string` / `file` | 否 | `muse-director` 专属剧本、分镜表与人设圣经输入（支持 `.md/.txt/.json/.yaml/.srt`） |
| `conversation_id` / `session_id` | `string` | 否 | **JSON 顶层**云端沙盒粘性会话锁（用于在多轮创作或安全建议确认时复用同一沙盒与设定图上下文；详见 `02-STICKY_SESSION_AND_BILLING_GUIDE.md`） |

---

## 四、云端沙盒会话粘性（`/v1/chat/completions` 与 `/v1/videos`）

- **默认隔离**：未传粘性标识时，每次调用都会在低负载实例中创建全新子会话线程，不同调用方与不同对话之间严格隔离。
- **在 `/v1/chat/completions` 中**：首轮响应头 `X-Conversation-Id` 与响应体 `conversation_id` 会返回带 HMAC-SHA256 防篡改签名的 `mconv_<acc_tag>_<conv_id>_<sig>` 令牌，后续轮次原样回传即可 100% 命中同一实例与同一线程。
- **在 `/v1/videos` 中**：请从首轮起直接在 **JSON Body 顶层**（或 multipart 表单字段）传入自定义 `"conversation_id"`（如 `"conversation_id": "ep01_act02_run1"`），网关会自动按调用方命名空间隔离并锁定同一云端沙盒与对话线程。
