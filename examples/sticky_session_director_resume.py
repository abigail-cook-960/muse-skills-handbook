#!/usr/bin/env python3
"""
Muse Sticky-Session Continuation Demo (`muse-director` / `muse-video-20s..60s`).

Demonstrates:
1. Passing a custom `conversation_id` at the JSON Body top level from Round 1 so the
   cloud sandbox VM & sidechat thread are deterministically bound.
2. Detecting an upstream safety alternative suggestion when a task fails (which is
   automatically refunded 100% by the relay gateway — zero charge).
3. Seamlessly resuming in Round 2 with the exact same `conversation_id` to accept
   the suggested direction without regenerating character or storyboard sheets.
"""

from __future__ import annotations

import os
import time
import uuid
import urllib.request
import json
from typing import Any

BASE_URL = os.environ.get("OAIREGBOX_API_BASE_URL", "https://api.oairegbox.cc").rstrip("/")
API_KEY = os.environ.get("OAIREGBOX_API_KEY", "")

ALTERNATIVE_OFFER_HINTS = (
    "different direction",
    "let me know if you'd like",
    "would you like me to",
    "safer version",
    "gentler version",
    "换个方向",
    "如果你愿意，我可以",
)


def api_json(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    if not API_KEY:
        raise SystemExit("Please set OAIREGBOX_API_KEY in your environment or .env first.")
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def submit_and_poll_video(body: dict[str, Any], *, timeout_s: int = 1500) -> dict[str, Any]:
    created = api_json("POST", "/v1/videos", body)
    task_id = created.get("task_id") or created.get("id")
    if not task_id:
        raise RuntimeError(f"Unexpected task submission response: {created}")
    print(f"[Submitted] task_id={task_id} | conversation_id={body.get('conversation_id')}")

    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        detail = api_json("GET", f"/v1/videos/{task_id}")
        status = str(detail.get("status") or "").lower()
        progress = detail.get("progress", 0)
        print(f"  [Poll] task_id={task_id} status={status} progress={progress}%")
        if status in ("completed", "succeeded", "success"):
            return detail
        if status in ("failed", "failure", "cancelled"):
            return detail
        time.sleep(5)
    raise TimeoutError(f"Polling deadline ({timeout_s}s) reached for {task_id}; keep polling instead of resubmitting!")


def is_safety_alternative_offer(error_text: str) -> bool:
    low = error_text.lower()
    return any(hint in low for hint in ALTERNATIVE_OFFER_HINTS)


def main() -> None:
    # Bind a deterministic session lock starting from Round 1 (in JSON Body!)
    conv_id = f"drama_winter_dragon_{uuid.uuid4().hex[:8]}"

    round1_body = {
        "model": "muse-director",
        "conversation_id": conv_id,
        "prompt": (
            "Direct a 60-second fantasy drama episode in a snow-covered mountain town as an ancient "
            "frost dragon swoops down above the rooftops confronting the young guardian."
        ),
        "aspect_ratio": "16:9",
        "seconds": "60",
        "style_preset": "3d_xianxia",
        "skill_preset": "manju_director,occlusion_wipe",
    }

    result = submit_and_poll_video(round1_body)
    if str(result.get("status", "")).lower() in ("completed", "succeeded", "success"):
        video_url = result.get("video_url") or (result.get("result") or {}).get("url")
        print(f"[Success on Round 1] MP4 URL: {video_url}")
        return

    err_msg = json.dumps(result.get("error") or result.get("fail_reason") or "", ensure_ascii=False)
    print(f"[Round 1 Failed — Pre-reserved quota 100% auto-refunded]: {err_msg}")

    if is_safety_alternative_offer(err_msg):
        print("[Sticky Resume] Detected upstream peaceful alternative suggestion! Reusing same conversation_id...")
        round2_body = {
            "model": "muse-director",
            "conversation_id": conv_id,
            "prompt": (
                "Yes, please build that exact 60-second version you suggested! Reuse the character and "
                "storyboard sheets already in this workspace, stage the peaceful aurora soaring sequence, "
                "stitch all segments, and output the final MP4 immediately."
            ),
            "aspect_ratio": "16:9",
            "seconds": "60",
        }
        resumed = submit_and_poll_video(round2_body)
        if str(resumed.get("status", "")).lower() in ("completed", "succeeded", "success"):
            video_url = resumed.get("video_url") or (resumed.get("result") or {}).get("url")
            print(f"[Success on Sticky Round 2] MP4 URL: {video_url}")
        else:
            print(f"[Round 2 Ended]: {resumed}")


if __name__ == "__main__":
    main()
