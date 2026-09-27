#!/bin/bash

nohup anvil --state ./log/state.json --state-interval 3600 -a 0 -m "$MNEMONIC" &

exec python3 app.py
