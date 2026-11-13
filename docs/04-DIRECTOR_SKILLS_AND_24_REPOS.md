# 16 套导演与转场技能预设 + 7 套视觉画风 + 全球 24 大开源 AI 导演 Skills 生态图鉴

> 结构化机器可读全量配置（含完整英文/中文注入 Prompt 与别名表）请直接查阅或加载本仓库 [`presets/director_presets_catalog.json`](../presets/director_presets_catalog.json)。

---

## 一、5 套黄金导演组合（一键套用推荐）

| 组合 ID | 组合名称 | `style_preset` | `skill_preset`（逗号叠加） | 适用题材与蒸馏来源 |
| :--- | :--- | :--- | :--- | :--- |
| `combo_short_drama_hook` | 🔥 爆款短剧·黄金3秒钩子+微表演组合 | `cinematic_realistic` | `micro_drama_hook,emotion_micro_acting,cut_on_action` | 0–3s 高反差冲突反转开场 + 潜台词眼神呼吸微动作 + 30°动接动切镜（融合 `zenstory-ai/drama-skills` · `kangarooking/director-skills`） |
| `combo_xianxia_combat` | ⚔️ 东方仙侠·变速打戏+灵力因果无缝转场 | `3d_xianxia` | `xianxia_speed_ramp,action_choreography,occlusion_wipe` | 蓄力静帧→极速突进(Speed-Ramp)→法术气浪掀衣反馈 + 单镜完整攻防节拍 + 前景石柱/披风遮挡转场（融合 `liyue-aigc/xianxia-cinematic-video-director`） |
| `combo_manju_continuity` | 🎬 精品漫剧·全流程导演+三维空间连戏锁 | `2d_anime` | `manju_director,spatial_blocking_continuity,over_shoulder_axis` | 漫剧导演 v2.2 五大铁律 + 三维舞台主光源/左右手道具连戏锁 + 180°轴线越肩正反打（融合 `HBAI-Ltd/Toonflow-app` · `eternityspring/shuohao-skills`） |
| `combo_commercial_tvc` | 🛍️ 商业TVC·微距流体受力链+焦点叙事 | `ecommerce_ugc` | `tvc_product_hero,rack_focus_mood,match_cut` | 前三秒痛点钩子 + 产品开盖/滴落张力/高光物理受力链 + f/1.4浅景深移焦 + 图形匹配转场（融合 `nutllwhy/seedance-tvc-director` · `Vincentwei1021/video-shotcraft`） |
| `combo_auteur_cinema` | 🎞️ 大师电影·王家卫框景霓虹+推轨长镜头 | `cinematic_realistic` | `auteur_wong_kar_wai,dolly_zoom_oner,emotion_micro_acting` | 门框/百叶窗前景框景与冷暖霓虹对比 + 斯坦尼康推轨变焦一镜到底 + 潜台词克制微表情（融合 `wuwangzhang1216/DirectorSKILL` · `lemomo-ai/lemo-opuscar`） |

---

## 二、7 套内置视觉画风预设（`style_preset`）

| 预设 ID | 常用别名 | 视觉锁定说明 |
| :--- | :--- | :--- |
| `none` | `raw`, `off` | **不注入内置风格**：100% 由用户原始 `prompt` 与参考图决定画面风格 |
| `cinematic_realistic` | `realistic`, `cinematic`, `live_action` | **好莱坞真人实拍电影感**：ARRI Alexa 35mm 变形宽银幕、真实皮肤毛孔与织物纹理、体积光与胶片调色，禁 2D/3D 卡通感 |
| `2d_anime` | `anime`, `2d`, `cel_shaded`, `manju_2d` | **2D 日漫/国漫赛璐璐**：清晰黑线勾勒、扁平赛璐璐色块、戏剧化冷暖边缘光，禁 3D CGI 与真人写实 |
| `3d_xianxia` | `3d`, `xianxia`, `cg` | **高清 3D 国漫修仙 CG**：UE5 电影级 3D 国漫渲染、丝绸刺绣流光、灵力粒子与体积云雾 |
| `american_comic` | `cartoon`, `comic` | **欧美暗黑爽文漫剧**：粗犷美漫墨线、高对比明暗块面（Chiaroscuro）、冷硬派张力构图 |
| `cyberpunk_neon` | `cyberpunk`, `scifi` | **赛博朋克霓虹科幻**：雨夜青品双色霓虹反射、全息 HUD 光效、近未来机能质感 |
| `ecommerce_ugc` | `ugc`, `ecommerce` | **电商带货 / 真人种草实拍**：干净通透自然日光、商品材质与色彩高保真还原、微距清晰无畸变 |

---

## 三、16 套电影学与开源导演技能预设（`skill_preset`）

支持单项传入，或使用英文逗号 `,` 自由组合多项（如 `"occlusion_wipe,micro_drama_hook,emotion_micro_acting"`）：

| 编号 | 预设 ID | 常用别名 | 核心导演技法摘要 | 致敬出处与协议 |
| :---: | :--- | :--- | :--- | :--- |
| `RAW` | `none` | `raw`, `off` | 不注入任何内置运镜/转场规则，完全按用户原始提示词执行 | — |
| `①` | `occlusion_wipe` | `occlusion`, `wipe` | **前景遮挡无缝转场 5 步法**：片段 A 末尾用真实前景物（树干/石柱/披风/门框）同向平移盖满镜头 → 截取暗部低熵尾帧作片段 B 首帧 → 同向同速滑出遮挡物（严禁反向防刹车感） | 经典电影剪辑遮挡法 |
| `②` | `cut_on_action` | `cut`, `camera_switch` | **动接动硬切与 `≥30°` 景别切换**：在动作发力最高点切镜，同时切换 `≥30°` 机位与景别（远景→特写→低机位仰拍），严守 180° 轴线 | Walter Murch · `Rylaispirit/cinematic-video-prompt-skill` (MIT) |
| `③` | `match_cut` | `match` | **图形/动作相似性匹配转场**：对齐前一镜结尾与下一镜开头的几何轮廓与运动矢量（圆月→瞳孔、旋涡→车轮） | 今敏/库布里克 · `Vincentwei1021/video-shotcraft` (Apache-2.0) |
| `④` | `whip_pan` | `whip` | **极速甩镜动量转场**：镜头结尾 0.8s 高速同向甩动产生自然运动模糊条纹，下一镜同向甩入平滑定格 | `jnMetaCode/ai-shortfilm-prompts` (MIT) |
| `⑤` | `dolly_zoom_oner` | `dolly_zoom`, `oner`, `vertigo` | **希区柯克推轨变焦与一镜到底**：斯坦尼康长镜头向前推轨同时压缩/拉伸背景纵深，强化震惊或觉醒张力 | `wuwangzhang1216/DirectorSKILL` (MIT) |
| `⑥` | `over_shoulder_axis` | `ots`, `axis` | **180° 轴线越肩正反打（OTS）**：锁死左看右 / 右看左屏幕方位，以前景肩颈浅景深虚化建立对话空间纵深 | `eternityspring/shuohao-skills` (Apache-2.0) |
| `⑦` | `rack_focus_mood` | `rack_focus`, `bokeh` | **浅景深虚实移焦与情绪空镜**：`f/1.4` 大光圈从前景细节（雨滴/茶盏/剑尖）平滑移焦至后景人物眼眸 | `popopo-99/zy-cinematic-realism` |
| `⑧` | `action_choreography` | `action`, `fight`, `combat` | **高燃动作攻防节拍**：单镜单完整攻防交换（闪避→格挡→反击→`1.2s` 落地收势），明确前进/后退矢量与冲击反馈 | `kangarooking/director-skills` (MIT) |
| `⑨` | `manju_director` | `director`, `manju`, `drama` | **漫剧全流程导演 v2.2**：每镜锚定角色图+彩色分镜符、锁定角色音色、单镜单微动作+1.2s留白、遮挡/动接动转场 | `HBAI-Ltd/Toonflow-app` · `zenstory-ai/drama-skills` (MIT) |
| `⑩` | `micro_drama_hook` | `hook`, `hongguo` | **黄金 3 秒冲突钩子与付费卡点**：`0–3s` 直接以高反差视觉冲突/反转开场（禁慢空镜铺垫），末尾 `1.5s` 悬念定格 | `zenstory-ai/drama-skills` · `manju-laoli-skill` (MIT) |
| `⑪` | `emotion_micro_acting` | `micro_acting`, `subtext` | **潜台词微表情与呼吸落点表演**：将抽象情绪拆解为「眼神→屏息→下颌微紧→手指抓握→`1.0s` 余韵落点」时间序 | `kangarooking/director-skills` (MIT) |
| `⑫` | `xianxia_speed_ramp` | `speed_ramp`, `xianxia_director` | **东方仙侠变速运镜与灵力因果链**：蓄力静帧→极速突进（Speed-Ramp）→气浪掀动衣袍/水纹/尘土物理因果→收势稳停 | `liyue-aigc/xianxia-cinematic-video-director` |
| `⑬` | `tvc_product_hero` | `tvc`, `commercial` | **商业 TVC 产品因果与微距流体质感**：前三秒抓人钩子 + 开盖/滴落表面张力/涂抹/边缘高光扫掠真实受力链 | `nutllwhy/seedance-tvc-director` (MIT) |
| `⑭` | `auteur_wong_kar_wai` | `wong_kar_wai`, `auteur` | **王家卫式抽帧霓虹与前景框景美学**：门框/百叶窗/镜面画中画构图，暖黄钨丝灯撞冷青暗部与手持呼吸抽帧感 | `wuwangzhang1216/DirectorSKILL` · `lemomo-ai/lemo-opuscar` (MIT) |
| `⑮` | `spatial_blocking_continuity` | `blocking`, `continuity` | **三维空间走位锁与左右手/道具连戏**：跨镜头锁死三维舞台平面、主光源方向与人物持握武器左右手，杜绝穿帮 | `eternityspring/shuohao-skills` (Apache-2.0) |

---

## 四、全球 24 大精选开源 AI 影视 / 短剧 / 漫剧导演 Skills 仓库导航

| # | 领域分类 | 开源仓库 | Stars | 开源协议 | 核心亮点与推荐联动预设 |
| :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | 综合视频智能体与镜头工程 | [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) | 75.8k+ | AGPL-3.0 | 开源多智能体视频生产系统，内置 12 条制片管线与 700+ Agent Skill 文件 · 推荐 `cut_on_action,spatial_blocking_continuity` |
| 2 | 综合视频智能体与镜头工程 | [HBAI-Ltd/Toonflow-app](https://github.com/HBAI-Ltd/Toonflow-app) | 20.3k+ | MIT | 开源 AI 短剧与漫剧工作台：小说改编、角色场景四视图资产锚定与无限画布分镜 · 推荐 `manju_director,occlusion_wipe` |
| 3 | 综合视频智能体与镜头工程 | [chatfire-AI/huobao-drama](https://github.com/chatfire-AI/huobao-drama) | 16.9k+ | Open Source | 火宝短剧一站式全自动生成平台：剧本拆解、定妆、分镜到成片合成 · 推荐 `micro_drama_hook,cut_on_action` |
| 4 | 综合视频智能体与镜头工程 | [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) | 16.4k+ | Apache-2.0 | 面向 Claude Code & Codex 的 124 张电影感镜头配方卡与 150 种运镜节拍库 · 推荐 `match_cut,tvc_product_hero` |
| 5 | 综合视频智能体与镜头工程 | [waooAI/waoowaoo](https://github.com/waooAI/waoowaoo) | 14.7k+ | Open Source | 好莱坞工业标准 AI 影视生产 Agent 平台，可控多镜角色资产与画布导演流 · 推荐 `dolly_zoom_oner,spatial_blocking_continuity` |
| 6 | 综合视频智能体与镜头工程 | [HKUDS/ViMax](https://github.com/HKUDS/ViMax) | 12.8k+ | MIT | 港大开源多智能体视频框架（导演 Director + 编剧 Screenwriter + 制片 Producer 协同） · 推荐 `manju_director,emotion_micro_acting` |
| 7 | 电影风格与大师镜头库 | [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) | 11.6k+ | MIT | 66 套即用型电影视觉风格提示词与样片工程库 · 推荐 `auteur_wong_kar_wai,rack_focus_mood` |
| 8 | AI短剧与漫剧专项 Skills | [Forget-C/Jellyfish](https://github.com/Forget-C/Jellyfish) | 7.1k+ | Apache-2.0 | 端到端 AI 短剧制片空间：结构化分镜与跨镜头角色/服装一致性管理 · 推荐 `spatial_blocking_continuity,over_shoulder_axis` |
| 9 | AI短剧与漫剧专项 Skills | [eternityspring/shuohao-skills](https://github.com/eternityspring/shuohao-skills) | 5.9k+ | Apache-2.0 | 跨 Agent 通用短剧 7 大 Skill 套件（含 `novel-staging` 三维空间舞台调度） · 推荐 `spatial_blocking_continuity,over_shoulder_axis` |
| 10 | AI短剧与漫剧专项 Skills | [dexhunter/seedance2-skill](https://github.com/dexhunter/seedance2-skill) | 4.4k+ | MIT | 多模态视频提示词标准库：`@图` 参考语法、运镜词典与短剧/MV 多镜头模板 · 推荐 `cut_on_action,occlusion_wipe` |
| 11 | AI短剧与漫剧专项 Skills | [zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills) | 3.7k+ | MIT | 11 个标准 `SKILL.md` 组成的开源短剧/漫剧全流程：分集钩子、资产设定、分镜与审稿质检 · 推荐 `micro_drama_hook,manju_director` |
| 12 | AI视频剪辑与故事线导演 | [FireRedTeam/FireRed-OpenStoryline](https://github.com/FireRedTeam/FireRed-OpenStoryline) | 3.6k+ | Apache-2.0 | 意图驱动的 AI 导演剪辑 Agent，把自然语言导演意图转化为故事线节拍 · 推荐 `cut_on_action,match_cut` |
| 13 | AI短剧与漫剧专项 Skills | [lixiaoxiao9888-create/manju-laoli-skill](https://github.com/lixiaoxiao9888-create/manju-laoli-skill) | 1.8k+ | MIT | 漫剧老李全流程导演套装（1 总控 + 12 子技能 + 六道前置锁 + 三大打戏引擎） · 推荐 `micro_drama_hook,action_choreography,spatial_blocking_continuity` |
| 14 | 开源导演 Skills 索引大全 | [UnderleveledBuilder/awesome-short-drama-skills](https://github.com/UnderleveledBuilder/awesome-short-drama-skills) | 1.7k+ | CC0-1.0 | 人工盲测评分的 83 个 AI 短剧/漫剧 `SKILL.md` 索引库 + 16 个开源制片平台汇总 · 推荐 `micro_drama_hook,emotion_micro_acting` |
| 15 | AI短剧与漫剧专项 Skills | [alibaba/lumenx](https://github.com/alibaba/lumenx) | 1.4k+ | MIT | 阿里巴巴开源 LumenX Studio 动态漫/短漫剧一站式平台 · 推荐 `manju_director,occlusion_wipe` |
| 16 | 电影摄影与表演运镜 Skills | [popopo-99/zy-cinematic-realism](https://github.com/popopo-99/zy-cinematic-realism) | 648+ | Open Source | 造梦师 Dream Director：物理可信光影、前景遮挡构图与克制电影感实拍体系 · 推荐 `rack_focus_mood,spatial_blocking_continuity` |
| 17 | 电影摄影与表演运镜 Skills | [Shanyin-ai/shanyin-director-master](https://github.com/Shanyin-ai/shanyin-director-master) | 621+ | MIT | 山音超级导演大师：导演定调→节奏规划→工业标准九列分镜表拆解 · 推荐 `cut_on_action,over_shoulder_axis` |
| 18 | 电影摄影与表演运镜 Skills | [jnMetaCode/ai-shortfilm-prompts](https://github.com/jnMetaCode/ai-shortfilm-prompts) | 513+ | MIT | 覆盖 21 种影片类型与 5 阶段叙事结构的跨模型电影短片提示词库 · 推荐 `whip_pan,cut_on_action` |
| 19 | 商业 TVC 与仙侠打戏 Skills | [nutllwhy/seedance-tvc-director](https://github.com/nutllwhy/seedance-tvc-director) | 334+ | MIT | 商业广告 TVC 导演 Skill：黄金前三秒钩子、产品物理受力证据链与局部返工诊断 · 推荐 `tvc_product_hero,rack_focus_mood` |
| 20 | 电影摄影与表演运镜 Skills | [wuwangzhang1216/DirectorSKILL](https://github.com/wuwangzhang1216/DirectorSKILL) | 311+ | MIT | Cinematic Director v2.1：潜台词拆解、场面调度与 20 位殿堂级导演风格滤镜 · 推荐 `auteur_wong_kar_wai,dolly_zoom_oner` |
| 21 | 商业 TVC 与仙侠打戏 Skills | [liyue-aigc/xianxia-cinematic-video-director](https://github.com/liyue-aigc/xianxia-cinematic-video-director) | 276+ | Open Source | 东方仙侠变速运镜导演 + 高燃打斗导演：变速曲线與法术环境因果反馈 · 推荐 `xianxia_speed_ramp,action_choreography` |
| 22 | 电影摄影与表演运镜 Skills | [kangarooking/director-skills](https://github.com/kangarooking/director-skills) | 258+ | MIT | 收录 7 个专项导演 Skill：情绪微表演导演（`emotion-performance-director`）、动作打戏导演等 · 推荐 `emotion_micro_acting,action_choreography` |
| 23 | 电影摄影与表演运镜 Skills | [Rylaispirit/cinematic-video-prompt-skill](https://github.com/Rylaispirit/cinematic-video-prompt-skill) | 173+ | MIT | 700+ 电影摄影专业术语词典与公式化组装器（机位、推拉摇移、布光、胶片调色） · 推荐 `cut_on_action,dolly_zoom_oner` |
| 24 | AI短剧与漫剧专项 Skills | [LuoJiangYong/muse-video-skill](https://github.com/LuoJiangYong/muse-video-skill) | 52+ | MIT | 视频创作虚拟剧组引擎：38 个经典案例技法库 × 六大剧组角色协作与质量门控 · 推荐 `manju_director,micro_drama_hook,occlusion_wipe` |

*(注：若列表还包含社区补充子仓如 `shuyu-labs/BigBanana-AI-Director` 或 `seedance-2-5-fight-director`，其完整代表性分镜模板均已收录于 `presets/director_presets_catalog.json`。)*
