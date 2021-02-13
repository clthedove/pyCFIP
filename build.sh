#!/bin/bash
export RELEASE_FOLDER=release
export BIN_NAME=$RELEASE_FOLDER/pycfip-$(uname -s | tr '[A-Z]' '[a-z]')-$(uname -m | tr '[A-Z]' '[a-z]')
rm -rf $RELEASE_FOLDER
pyinstaller -F main.py
mkdir $RELEASE_FOLDER
mv dist/main $BIN_NAME
rm -rf build dist *.spec
chmod +x $BIN_NAME
echo "===== Build Finished ====="
ln -s $BIN_NAME pycfip
