#!/usr/bin/env bash
set -e

echo "Script started"

echo "OSTYPE=$OSTYPE"

if [[ "$OSTYPE" == "msys" ]]; then
  echo "Windows Git Bash detected"
else
  echo "Unix-like system detected"
fi

echo "Script finished successfully"
