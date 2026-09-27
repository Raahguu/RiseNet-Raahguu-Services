#!/bin/bash

nohup anvil --state ./log/state.json --state-interval 3600 -a 0 --mnemonic $MNEMONIC &

exec python3 app.py
