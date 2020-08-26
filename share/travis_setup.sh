#!/bin/bash
set -evx

mkdir ~/.kyancore

# safety check
if [ ! -f ~/.kyancore/.kyan.conf ]; then
  cp share/kyan.conf.example ~/.kyancore/kyan.conf
fi
