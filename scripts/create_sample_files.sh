#!/usr/bin/env bash
set -e
mkdir -p sample-files
cat > sample-files/example.md <<'MD'
# Second Brain Test Note

This note is a simple test document for the Second Brain upload pipeline.

Areas: AI, Business, Research.
MD
cat > sample-files/example.txt <<'TXT'
This is a TXT file used to test the upload registry and duplicate detection.
TXT
cat > sample-files/example.csv <<'CSV'
Area,Performance
AI,95
Business,87
Research,91
CSV
