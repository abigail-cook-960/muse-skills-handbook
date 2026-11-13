---
name: muse-director-shotcraft
description: Direct cohesive AI anime/manju, short dramas, TVC commercials, and multi-segment films using the 5 Manju Director Production Laws, 16 film-theory & open-source skill_preset directives, 7 visual style_preset locks, and 5 golden combos (native top-level fields on muse-* or prompt injection on Seedance/Veo/Kling/Wan/Grok).
---

# Muse AI Director & Shotcraft Skill (`muse-director-shotcraft`)

Use this skill when writing storyboards, multi-segment prompts, or API payloads for AI short dramas (`短剧`), dynamic manga/anime (`漫剧`), Xianxia action (`仙侠打戏`), or commercial TVCs — either natively on `muse-director` / `muse-video-20s..60s` or via prompt injection on any other video model (`seedance-2.0/2.5`, `flow-omni`, `flow-veo`, `kling-v3`, `wan3.0-video`, `grok-video`).

---

## 1. The Five Mandatory Manju & Short-Drama Production Laws

1. **LAW 1 — Anchor Every Clip with Character Sheet + Full-Color Director Storyboard**:
   - Text alone never holds art style across multiple 10s segments. Always pass persistent character reference sheets + a 4–6 panel color storyboard sheet (`images` array, up to 6 images) into **every** video generation call, paired with a strict style lock (`style_preset`).
2. **LAW 2 — Lock Deterministic Character Voices (or Use `mute_voice: true` for Post-Dubbing)**:
   - On `muse-director`, each character is assigned a fixed Avocado v2 voice ID and mixed over a `0.28x` SFX bed (`adelay=350ms`). When producing non-English/regional dubs externally, pass `"mute_voice": true` so characters still perform natural mouth movements while keeping pure Foley/SFX/BGM without random vocal drift.
3. **LAW 3 — Deliberate Pacing: One Complete Micro-Action + `1.2s` Settle Beat per Clip**:
   - Never cram 10 plot points into a single 10s segment. Stage **1 clear self-contained micro-action** (`dodge -> read -> counter -> landing hold`) plus `<= 16 words` (`<= 6.8s`) of dialogue, ending with a **`1.0s–1.5s` visual settle beat** so no cut ever slices mid-swing or mid-sentence.
4. **LAW 4 — Eliminate the 4 AI Splice Defects (`跳帧` / `刹车感` / `色调漂移` / `空间割裂`)**:
   - Across segment boundaries (`seg_{k-1}` → `seg_k`), use **Foreground Occlusion Wipe (`occlusion_wipe`)**: in the last `1.5s` of Segment A, pan smoothly in one direction (`→`) until a real in-scene foreground object (pillar, tree trunk, cloak, doorway shadow) **completely covers the lens**; extract that low-entropy dark frame as Segment B's first frame, and continue panning in the **EXACT SAME direction and speed (`→`)** as the occluder wipes off! Never reverse camera direction (`→` to `←`) across a boundary.
   - For non-wipe dialogue/combat cuts, enforce **Motivated Cut-on-Action (`cut_on_action`)** with a **`>= 30°` camera angle & shot-scale switch** (`Wide -> ECU on eyes -> Low-Angle Hero`) while preserving the **180° screen-direction axis (`over_shoulder_axis`)**.
5. **LAW 5 — Proactive Policy-Safe Dramatic Choreography**:
   - Avoid literal gore/graphic keywords (`blood`, `decapitate`, `kill`, `shoot`) that trigger upstream safety refusals or confirmation pauses. Express high-stakes conflict via **luminous spiritual/sci-fi energy shockwaves, blade sparks, shattered jade/stone, dramatic chiaroscuro lighting, and micro-expression tension**.

---

## 2. Visual Style Presets (`style_preset` — Pick 1 or `"none"`)

| `style_preset` ID | Style Lock Summary |
| :--- | :--- |
| `none` | Raw pass-through — 0 built-in style words injected |
| `cinematic_realistic` | ARRI Alexa 35mm anamorphic live-action cinema, skin pores, volumetric light, zero CGI/cartoon |
| `2d_anime` | Strict 2D hand-drawn cel-shaded Japanese/Chinese anime, crisp black ink lines, flat vibrant cel shading |
| `3d_xianxia` | Unreal Engine 5 cinematic 3D Chinese fantasy CG, silk robes, gold embroidery, spiritual aura particles |
| `american_comic` | Bold 2D Western graphic-novel animation, heavy ink outlines, chiaroscuro shadows |
| `cyberpunk_neon` | Rain-slicked cyan/magenta neon reflections, holographic HUD glow, atmospheric mist |
| `ecommerce_ugc` | Clean natural daylight commercial & creator UGC showcase, true product material/color fidelity |

---

## 3. 16 Director & Film-Theory Skill Presets (`skill_preset` — Comma-Stackable)

Combine multiple IDs with commas, e.g. `"skill_preset": "micro_drama_hook,emotion_micro_acting,cut_on_action"`:

### Film-Theory Classics (`①–⑨`)
- `occlusion_wipe` (①): 5-step Foreground Occlusion Wipe + same-direction momentum across 10s boundaries (default on `muse-video-20s..60s`)
- `cut_on_action` (②): Peak-momentum cut + `>= 30°` angle & shot-scale switch (`Walter Murch` / `Rylaispirit`)
- `match_cut` (③): Geometric shape & motion-vector Match Cut (`Satoshi Kon` / `Vincentwei1021/video-shotcraft`)
- `whip_pan` (④): High-speed directional Whip-Pan motion-blur transition (`jnMetaCode/ai-shortfilm-prompts`)
- `dolly_zoom_oner` (⑤): Unbroken Steadicam Oner + Hitchcock Vertigo Dolly-Zoom (`wuwangzhang1216/DirectorSKILL`)
- `over_shoulder_axis` (⑥): Strict 180° axis Shot/Reverse-Shot OTS bokeh (`eternityspring/shuohao-skills`)
- `rack_focus_mood` (⑦): `f/1.4` foreground-to-eyes Rack Focus + Ozu/Wong Kar-wai mood framing (`popopo-99/zy-cinematic-realism`)
- `action_choreography` (⑧): Readable combat vectors (`attack -> parry -> counter -> 1.2s recoil hold`, `kangarooking/director-skills`)
- `manju_director` (⑨): Full Manju Drama Director v2.2 5-law bundle (default on `muse-director`, `HBAI-Ltd/Toonflow-app`)

### Distilled Open-Source Short-Drama & Auteur Skills (`⑩–⑮`)
- `micro_drama_hook` (⑩): `0.0–3.0s` immediate visual hook/reversal (zero scenery padding) + `1.5s` cliffhanger tail (`zenstory-ai/drama-skills`)
- `emotion_micro_acting` (⑪): Observable subtext timeline (`Subtext -> Gaze/Breath/Jaw/Hand micro-signals -> 1.0s Afterbeat`, `kangarooking/director-skills`)
- `xianxia_speed_ramp` (⑫): Stillness charge -> sudden Speed-Ramp burst -> physical shockwave on robes/water/dust -> clean settle (`liyue-aigc/xianxia-cinematic-video-director`)
- `tvc_product_hero` (⑬): 3s commercial hook + tactile physical force chain (uncapping, droplet tension, specular sweep, `nutllwhy/seedance-tvc-director`)
- `auteur_wong_kar_wai` (⑭): Doorframe/blinds Frame-within-a-Frame + tungsten-amber vs emerald-cyan step-printed melancholy (`wuwangzhang1216/DirectorSKILL` · `lemomo-ai/lemo-opuscar`)
- `spatial_blocking_continuity` (⑮): 3D stage floorplan lock — locks key-light direction, landmarks, and left/right weapon handedness (`eternityspring/shuohao-skills`)

---

## 4. Five Battle-Tested Golden Director Combos

1. **Short-Drama 3s Hook (`爆款短剧`)**: `style_preset="cinematic_realistic"`, `skill_preset="micro_drama_hook,emotion_micro_acting,cut_on_action"`
2. **Xianxia Speed-Ramp Combat (`东方仙侠`)**: `style_preset="3d_xianxia"`, `skill_preset="xianxia_speed_ramp,action_choreography,occlusion_wipe"`
3. **Manju Full Continuity (`精品漫剧`)**: `style_preset="2d_anime"`, `skill_preset="manju_director,spatial_blocking_continuity,over_shoulder_axis"`
4. **Commercial TVC Hero (`商业TVC`)**: `style_preset="ecommerce_ugc"`, `skill_preset="tvc_product_hero,rack_focus_mood,match_cut"`
5. **Auteur Cinema Oner (`王家卫长镜`)**: `style_preset="cinematic_realistic"`, `skill_preset="auteur_wong_kar_wai,dolly_zoom_oner,emotion_micro_acting"`

> **Cross-Model Usage**: On `muse-*` models, send `style_preset` and `skill_preset` as top-level JSON fields. On non-Muse models (`seedance`, `veo`, `kling`, `wan`, `grok`), load `presets/director_presets_catalog.json` and prepend the corresponding `prompt` directive strings directly to the model's `prompt`.
