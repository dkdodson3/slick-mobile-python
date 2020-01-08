#!/usr/bin/env bash

if [[ $(uname) = "Darwin" ]]; then
    brew install imagemagick@6
else
    sudo apt-get update &&
    sudo apt-get install -y imagemagick libmagickwand-dev
fi

pip3 install -r requirements.txt --upgrade
