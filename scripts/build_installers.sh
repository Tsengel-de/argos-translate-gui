#!/usr/bin/env bash
# ==============================================================================
# Argos Translate GUI - Standalone Desktop Application Packager
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$REPO_ROOT/dist"

echo "=== Building Standalone Argos Translate Desktop Application ==="
echo "Repo Root: $REPO_ROOT"

cd "$REPO_ROOT"

# Ensure pyinstaller and PyQt5 are installed
python3 -m pip install --upgrade pip
python3 -m pip install pyinstaller PyQt5 sentencepiece ctranslate2
python3 -m pip install -e ../argos-translate
python3 -m pip install -e .

# Run PyInstaller
echo "Compiling binary with PyInstaller..."
pyinstaller \
    --name "ArgosTranslate" \
    --windowed \
    --onefile \
    --clean \
    bin/argos-translate-gui

echo "Build complete. Executable located at: $DIST_DIR/ArgosTranslate"
