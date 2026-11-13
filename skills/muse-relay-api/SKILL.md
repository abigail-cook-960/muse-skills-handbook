---
name: muse-relay-api
description: Integrate Meta Muse (muse-fast) full-modal models via an OpenAI-compatible relay gateway (OAIREGBOX / New-API). Use when calling muse-chat, muse-agent, muse-image, muse-video (10s–60s & video extension), muse-director, muse-podcast, muse-tts, muse-asr, muse-audio, or muse-live; handling top-level media JSON contracts; resuming sticky sessions after upstream safety suggestions; or auditing task billing/refunds.
---

# Muse Full-Modal Relay API Skill (`muse-fast`)

Use this skill when building applications, scripts, or automated pipelines on top of the **Muse (`muse-fast`)** full-modal model family through an OpenAI-compatible relay gateway (such as `https://api.oairegbox.cc` or `https://newapi-2.oairegbox.cc`).

## 1. Environment & Safety Rules

1. **Credentials from `.env` only**: Read `OAIREGBOX_API_BASE_URL` (default `https://api.oairegbox.cc`, no trailing `/v1`) and `OAIREGBOX_API_KEY` from `.env`. Never hardcode `sk-*` keys in code or frontend bundles.
2. **Discover live models first**: Always verify token-scoped model availability with `GET {BASE_URL}/v1/models` before submitting paid tasks.
3. **Never resubmit an in-flight async video task**: `muse-video-*` (20s–60s) and `muse-director` run inside cloud sandboxes and routinely take **3–18 minutes**. Use a polling timeout of **at least 15 minutes** (`25 minutes` for `muse-director`). On network hiccups, retry `GET /v1/videos/{task_id}` — never re-POST `/v1/videos`.
4. **Zero charge on failure**: Any task ending in `status: "failed"` (upstream safety suggestion timeout, moderation block, or sandbox error) triggers **100% automatic refund** of pre-reserved quota in the relay gateway (`type=6` refund log). Only `completed` tasks with playable media are billed.

---

## 2. Model Matrix & Endpoint Routing

| Model ID | Modality & Use Case | Endpoint | Billing Mode | Key Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `muse-chat` | Multimodal chat, vision & cloud sandbox | `POST /v1/chat/completions` | Per-token | Supports vision, code execution, OpenAI `tools`, sticky `conversation_id` |
| `muse-agent` (`muse-spark`) | Autonomous multi-step cloud VM agent | `POST /v1/chat/completions` | Per-token + media | Full Linux VM; generated media inside chat settles as completion tokens |
| `muse-image` | Native 2K text-to-image & multi-image edit | `POST /v1/images/generations`<br>`POST /v1/images/edits` | Per-call | Native WebP up to 2K (`1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`), `≤4` ref images; no `transparent` matting |
| `muse-video` | Single-segment HD video with audio (`≤10s`) | `POST /v1/videos` | Per-call | `seconds`: `"1"`–`"10"` (string). Rejects `>10s` or `video_url` extension (`400`) |
| `muse-video-20s` .. `60s` | Multi-segment stitched HD video or extension | `POST /v1/videos` | Per-call | Fixed `20s`/`30s`/`40s`/`50s`/`60s`; with `video_url`, extends clip up to tier cap (source must be `< tier - 1s`) |
| `muse-director` (`muse-drama`) | Autonomous AI Manju / Short-Drama Director | `POST /v1/videos` | Dynamic (`images + seconds`) | Accepts `script` / `.md` / `.srt` + `≤6` ref sheets; natural beat cuts (`10–90s`); deterministic character TTS |
| `muse-podcast` | Multi-speaker researched podcast (MP3) | `POST /v1/videos` | Per-call | Async task; audio URL returned in `video_url` / `url` / `/content` |
| `muse-tts` | Avocado v2 neural TTS | `POST /v1/audio/speech` | Per-call | Voices: `alloy`, `nova`, `echo`, `fable`, `coral`; formats: `mp3`, `wav`, `opus`, `pcm` |
| `muse-asr` | Fast speech-to-text (STT) | `POST /v1/audio/transcriptions` | Per-call | Multipart `file=@audio.mp3` (`mp3`/`wav`/`ogg`/`m4a`/`flac`/`webm`) |
| `muse-audio` / `muse-live` | Voice-in/voice-out chat & realtime duplex | `POST /v1/chat/completions`<br>`WS /v1/realtime?model=muse-live` | Per-token | Accepts `input_audio` Base64 in `messages`; returns text + synthesized speech |

---

## 3. Critical Parameter Contracts (Avoid Silent Pitfalls)

### Rule A — Top-Level Media Fields Only on `POST /v1/videos`
Never nest reference images inside `metadata.content`! Always place media fields at the **top level** of the JSON body (or as top-level `multipart/form-data` fields):
- **First frame**: `first_image_url` (also `image`, `first_frame`, `input_reference`)
- **Last frame**: `last_image_url` (also `last_frame`)
- **Character / scene reference images (`≤6` images)**: `images: ["https://...", "data:image/webp;base64,..."]` (also `reference_images`)
- **Source video for extension (`20s`–`60s` tiers only, `≤20 MB`)**: `video_url` (source duration must be `< 19s / 29s / 39s / 49s / 59s` respectively; `seconds` represents **total output duration**, not added duration)

### Rule B — Always Send `seconds` as a String
In OpenAI Video relay DTOs, pass `"seconds": "8"` or `"seconds": "30"` (string), not an integer, to avoid `invalid_json` schema rejections.

### Rule C — Vocal Mute with Lip-Sync (`mute_voice`)
All `muse-video*` and `muse-director` models generate **H.264 + AAC audio by default** (`mute_voice: false`). Setting `"mute_voice": true` keeps character mouth acting/lip movement intact for post-production dubbing while muting spoken vocals and preserving cinematic SFX/BGM/Foley.

### Rule D — Director & Style Presets (`style_preset` + `skill_preset`)
Pass at JSON top level on any `muse-video*` or `muse-director` call:
- `style_preset`: `"none"` (raw), `"cinematic_realistic"`, `"2d_anime"`, `"3d_xianxia"`, `"american_comic"`, `"cyberpunk_neon"`, `"ecommerce_ugc"`
- `skill_preset`: `"none"` (raw), or comma-separated multi-select from the 16 presets, e.g. `"occlusion_wipe,micro_drama_hook,emotion_micro_acting"`
- `custom_style` / `custom_skill`: free-form supplemental instructions

---

## 4. Sticky-Session Continuation on Upstream Safety Suggestions

### Why `"A different direction I can make for you..."` Happens
When a prompt contains intense combat/conflict words (`attack`, `kill`, `destroy`, `blood`, etc.), the upstream Muse Agent may propose a gentler cinematic alternative instead of failing abruptly:
> `upstream completed without readable video output: A different direction I can make for you in the same winter town... Let me know if you'd like me to build the 60 seconds that way.`

The gateway already intercepts ~90% of these automatically (proactive safe-choreography rewrite instruction + one automatic `"Yes, sounds good! Immediately generate..."` follow-up). If the follow-up still hits the task deadline, the task turns `failed` (**100% quota refunded automatically**), while **the cloud VM sandbox, character sheets, and conversation context remain alive**.

### How to Resume Seamlessly Without Regenerating Character/Storyboard Sheets

1. **Best Practice — Pass a custom `conversation_id` in the JSON Body starting from Round 1**:
   > **Gateway Relay Rule**: On `POST /v1/videos` (Type-55 async video endpoint), always put `"conversation_id"` (or `"session_id"`) **inside the JSON Body** (or multipart form field). HTTP headers (`X-Conversation-Id`) and URL query params (`?session_id=...`) are recommended for `/v1/chat/completions`, whereas JSON Body is guaranteed to pass straight through Type-55 video adaptors.
2. **Round 1 (Initial Creation)**:
   ```json
   {
     "model": "muse-director",
     "conversation_id": "drama_ep01_act02_v1",
     "prompt": "Direct a 60-second winter town dragon confrontation episode...",
     "seconds": "60",
     "images": ["https://example.com/hero_sheet.webp"]
   }
   ```
3. **Round 2 (Sticky Continuation if Round 1 timed out after an alternative offer)**:
   Reuse the **exact same `conversation_id`** (or, if continuing from an existing session/task identifier bound in that workspace, pass that same identifier in `conversation_id`) and confirm the suggested direction:
   ```json
   {
     "model": "muse-director",
     "conversation_id": "drama_ep01_act02_v1",
     "prompt": "Yes, please build that exact 60-second version you suggested! Soaring peacefully above the snow-covered rooftops with aurora-like light, stitch all clips and output the final mp4.",
     "seconds": "60"
   }
   ```
   - **Billing Guarantee**: Round 1 (`failed`) is refunded 100%; Round 2 only charges if it completes with a valid MP4. Zero double billing.
