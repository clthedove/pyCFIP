#!/usr/bin/env bash
rm -rf pycfip
pyinstaller -F main.py
mv dist/main pycfip
rm -rf build dist *.spec
chmod +x pycfip
echo "===== Build Finished ====="

