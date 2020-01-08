#!/usr/bin/env bash
set -x

# MUST BE RUN ON AN OSX MACHINE
CWD=$(pwd)

# Install some needed packages through brew
brew install carthage &&
brew install pocketsphinx &&
brew install --HEAD usbmuxd &&
brew install --HEAD libimobiledevice &&
brew install wix/brew/applesimutils &&
brew install gradle &&
brew install npm &&
pip3 install pocketsphinx --upgrade

# Install appium packages
sudo npm install -g npm &&
npm install -g ios-deploy --unsafe-perm=true &&
npm install -g appium appium-doctor json &&

cd /usr/local/lib/node_modules/appium/node_modules/appium-xcuitest-driver/WebDriverAgent &&
mkdir -p Resources/WebDriverAgent.bundle &&
./Scripts/bootstrap.sh -d &&

cd ${CWD}
