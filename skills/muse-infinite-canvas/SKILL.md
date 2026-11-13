---
name: muse-infinite-canvas
description: Operate and orchestrate multimodal workflows inside the Infinite Canvas (/studio/) with Muse and multi-vendor models — wiring text/script nodes, native WebP character reference sheets, first/last frames, multi-reference 10s–60s video & video extension nodes, podcast/TTS/voice-chat nodes, and the 16-Preset & 24-Repo AI Director Workbench.
---

# Infinite Canvas (`/studio/`) Multimodal & Director Workflow Skill

Use this skill when guiding users or canvas agents to build multi-shot visual stories, anime/manju episodes, or multimodal chains inside the **Infinite Canvas (`/studio/`)** and **Video Studio (`/video`)**.

---

## 1. Node Categories & Muse Model Mapping in Canvas

| Canvas Node Type | Recommended Muse Models | Capabilities & Wiring Behavior |
| :--- | :--- | :--- |
| **Text / Script Node** | `muse-chat`, `muse-agent`, `muse-audio`, `muse-live` | Writes scripts/storyboards; inspects upstream Image nodes (`vision`); runs Python sandbox (`muse-agent`); accepts upstream Audio nodes via `input_audio` (`muse-audio` / `muse-live`) |
| **Image Node** | `muse-image` | Native WebP up to 2K (`1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`). Accepts `≤4` upstream Image nodes for multi-ref character/scene editing (preserves `image/webp` MIME seamlessly) |
| **Audio Node** | `muse-tts`, `muse-podcast` | `muse-tts` synthesizes character voice lines; `muse-podcast` runs async (`Auto` / `30s` / `60s` / `180s`) with live `0→100%` progress bar to produce multi-host MP3 episodes |
| **Video Node** | `muse-video`, `muse-video-20s..60s`, `muse-director` | Top-level `images` (`≤6` refs), `first_image_url` / `last_image_url` (`first_frame` / `last_frame` edge roles), `video_url` seamless extension (`20s–60s` tiers), `mute_voice` toggle, and Director Presets |

> Note: Utility/STT models (`muse-invite`, `muse-asr`) are intentionally excluded from Canvas generation dropdowns to keep creative node selectors clean.

---

## 2. Canonical Canvas Wiring Topologies

### Workflow A — Consistent Multi-Character Long Video (`10s–60s`)
1. Create **2–4 Image Nodes (`muse-image`)** to generate Character A Reference Sheet, Character B Reference Sheet, and Environment Concept Art (`16:9` or `9:16`).
2. Create a **Video Node (`muse-video-50s` or `muse-video-60s`)** and drag edges from those Image Nodes into the Video Node:
   - Set edge role to **`reference`** for character/costume consistency (`≤6` images total, sent as top-level `images[]`).
   - Optionally set 1 image edge to **`first_frame`** (`first_image_url`) and 1 to **`last_frame`** (`last_image_url`).
3. Click the **`Clapperboard` (导演预设 & 开源Skills)** button on the Video Node prompt bar:
   - Pick a **Golden Combo** (e.g. `⚔️ 仙侠打戏变速组合` or `🎬 漫剧全流程连戏组合`) or stack multiple `skill_preset` badges (`occlusion_wipe` + `spatial_blocking_continuity`).
   - Verify the node settings pill displays e.g. `720p · 9:16 · 50s · 🎬3项导演技能`.

### Workflow B — Autonomous Script-to-Episode (`muse-director`)
1. Create a **Text Node (`muse-chat` / `muse-agent`)** containing your episode script/beats, plus **Image Nodes** for your main characters.
2. Wire both the **Text Node** and **Image Nodes** into a **Video Node** set to **`muse-director`** (`10–90s` range; Canvas automatically widens the polling budget to **25 minutes / 600 polls** and folds any `first_frame`/`last_frame` edges into `images[]`).
3. Toggle **「生成声音」** ON (default, deterministic character TTS) or OFF (`mute_voice: true`, lip-sync kept with vocals muted for external dubbing).

### Workflow C — Seamless Video Extension (`muse-video-20s` ~ `muse-video-60s`)
1. Wire a completed **Video Node** (e.g. a `5s` or `10s` clip, `≤20 MB`) into a new **Video Node** set to `muse-video-20s` (or `30s`..`60s`).
2. **Pre-flight Guardrail**: Source video duration **must be `< tier_cap - 1s`** (e.g. `< 19s` for `muse-video-20s`, `< 29s` for `muse-video-30s`). Canvas blocks invalid lengths upfront at zero cost before sending any HTTP request.

### Workflow D — Voice-to-Voice Multimodal Chain (`muse-tts` → `muse-audio` / `muse-live`)
1. Generate or upload speech in an **Audio Node (`muse-tts`)**.
2. Drag an edge from the **Audio Node** into a **Text Node** running **`muse-audio`** or **`muse-live`** — Canvas automatically serializes the audio into `input_audio` Base64 and renders both the text answer and playable Avocado v2 voice reply link.

---

## 3. Built-in Director Workbench & Cross-Model Empowerment

- **3-Tab Director Modal (`Clapperboard` icon)**:
  - **Tab 1**: 5 Golden Combos + 16 `skill_preset` cards (with clickable GitHub source repo, OSS license badge, and demo preview; supports multi-select stacking).
  - **Tab 2**: 7 `style_preset` visual locks + `custom_style` input.
  - **Tab 3**: Searchable directory of **24 Global Open-Source AI Director Repositories** (`OpenMontage`, `Toonflow-app`, `huobao-drama`, `video-shotcraft`, `ViMax`, `drama-skills`, `manju-laoli-skill`, etc.) with one-click preset & storyboard template insertion.
- **Zero-Latency Built-in Prompt Library**: Open the left sidebar **「提示词」** tab (`muse-director-open-source-skills`, expanded by default) for 50 ready-to-use director combos, shot recipes, and style templates.
- **Cross-Model Compatibility**: Selecting any `style_preset` or `skill_preset` on `muse-*` sends clean top-level API fields; selecting them on **`seedance-2.0/2.5`, `flow-omni`, `flow-veo`, `kling-v3`, `wan3.0-video`, or `grok-video`** automatically fuses the distilled cinematic directives into `prompt` so every model on the canvas benefits.
