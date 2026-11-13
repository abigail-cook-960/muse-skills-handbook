#!/usr/bin/env bash
# Muse Full-Modal Relay Quickstart (cURL Cookbook)
# Usage: export OAIREGBOX_API_BASE_URL="https://api.oairegbox.cc" OAIREGBOX_API_KEY="sk-..."

set -euo pipefail

: "${OAIREGBOX_API_BASE_URL:=https://api.oairegbox.cc}"
: "${OAIREGBOX_API_KEY:?Please export OAIREGBOX_API_KEY=sk-... first}"

echo "=== 1. Discover visible models ==="
curl -sS "${OAIREGBOX_API_BASE_URL}/v1/models" \
  -H "Authorization: Bearer ${OAIREGBOX_API_KEY}" | head -c 400
echo -e "\n"

echo "=== 2. Cloud Sandbox Chat (returns signed mconv_... sticky token) ==="
curl -sS "${OAIREGBOX_API_BASE_URL}/v1/chat/completions" \
  -H "Authorization: Bearer ${OAIREGBOX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "muse-chat",
    "messages": [{"role": "user", "content": "请用一句话介绍前景遮挡无缝转场（Occlusion Wipe）的核心要点。"}]
  }'
echo -e "\n"

echo "=== 3. Native 2K Image Generation (muse-image) ==="
curl -sS "${OAIREGBOX_API_BASE_URL}/v1/images/generations" \
  -H "Authorization: Bearer ${OAIREGBOX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "muse-image",
    "prompt": "2D 赛璐璐动漫角色三视图设定单：银发青衣少年剑客，佩戴铜框护目镜，干净浅灰背景",
    "aspect_ratio": "16:9",
    "style": "anime"
  }'
echo -e "\n"

echo "=== 4. Submit 20s Video with Director Skill Presets (async task) ==="
curl -sS "${OAIREGBOX_API_BASE_URL}/v1/videos" \
  -H "Authorization: Bearer ${OAIREGBOX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "muse-video-20s",
    "conversation_id": "demo_sticky_vid_001",
    "prompt": "Part 1 (0-10s): 少年剑客在竹林中向右疾行，前景粗竹干向右扫过盖满镜头；Part 2 (10-20s): 镜头同向同速滑出竹干，切至山巅云海拔剑定格。",
    "aspect_ratio": "16:9",
    "seconds": "20",
    "style_preset": "2d_anime",
    "skill_preset": "occlusion_wipe,xianxia_speed_ramp",
    "mute_voice": true
  }'
echo -e "\n"
