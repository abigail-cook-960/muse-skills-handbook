#!/usr/bin/env python3
"""
Multi-Reference Video + 16 Director Skill Presets & Cross-Model Prompt Helper.

Shows:
1. Top-level `images`, `first_image_url`, `style_preset`, comma-stacked `skill_preset`,
   and `mute_voice` on `muse-video-*`.
2. How to inject the exact same open-source director presets into non-Muse video models
   (`seedance-2.5`, `flow-veo`, `kling-v3`, `wan3.0-video`, `grok-video`) using
   `presets/director_presets_catalog.json`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CATALOG_PATH = Path(__file__).resolve().parent.parent / "presets" / "director_presets_catalog.json"


def load_catalog() -> dict[str, Any]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def build_video_request_payload(
    *,
    model: str,
    prompt: str,
    seconds: str = "20",
    aspect_ratio: str = "16:9",
    reference_images: list[str] | None = None,
    first_image_url: str | None = None,
    style_preset: str = "cinematic_realistic",
    skill_preset: str = "micro_drama_hook,emotion_micro_acting,occlusion_wipe",
    mute_voice: bool = False,
) -> dict[str, Any]:
    catalog = load_catalog()
    is_muse = model.lower().startswith("muse-")

    if is_muse:
        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "seconds": str(seconds),  # Always string on /v1/videos
            "style_preset": style_preset,
            "skill_preset": skill_preset,
            "mute_voice": mute_voice,
        }
    else:
        # Cross-model director skill fusion for Seedance / Veo / Kling / Wan / Grok
        style_map = {item["id"]: item["prompt"] for item in catalog["style_presets"]}
        skill_map = {item["id"]: item["prompt"] for item in catalog["skill_presets"]}
        injected = [style_map.get(style_preset, "")]
        for sid in [s.strip() for s in skill_preset.split(",") if s.strip()]:
            if skill_map.get(sid):
                injected.append(skill_map[sid])
        injected.append(prompt)
        payload = {
            "model": model,
            "prompt": "\n\n".join(p for p in injected if p),
            "aspect_ratio": aspect_ratio,
            "seconds": str(seconds),
        }

    # CRITICAL: Always put reference images & first_image_url at JSON top level (never inside metadata!)
    if first_image_url:
        payload["first_image_url"] = first_image_url
    if reference_images:
        payload["images"] = reference_images[:6]

    return payload


if __name__ == "__main__":
    muse_payload = build_video_request_payload(
        model="muse-video-20s",
        prompt="Part 1 (0-10s): 女主在雨夜长廊疾步前行，前景廊柱向右扫过全遮挡镜头；Part 2 (10-20s): 同向滑出遮挡切至天台对峙近景。",
        seconds="20",
        aspect_ratio="9:16",
        reference_images=[
            "https://example.com/heroine_sheet.webp",
            "https://example.com/rooftop_concept.webp",
        ],
        style_preset="cinematic_realistic",
        skill_preset="micro_drama_hook,occlusion_wipe,emotion_micro_acting",
        mute_voice=False,
    )
    print("=== Muse Native Top-Level Payload ===")
    print(json.dumps(muse_payload, ensure_ascii=False, indent=2))
