#!/bin/bash
cd "$(dirname "$0")"
git add -A
git commit -m "update: $(date '+%Y-%m-%d %H:%M')"
git push
echo "✅ Subido a GitHub"
