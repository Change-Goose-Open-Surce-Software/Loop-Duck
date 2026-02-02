#!/bin/bash

wget -O ~/.local/bin/loopduck https://raw.githubusercontent.com/Change-Goose-Open-Surce-Software/Loop-Duck/main/Loopduck.py
chmod +x ~/.local/bin/loopduck
cd ~/.local/bin
ln -s loopduck Loop
ln -s loopduck loop
