#!/bin/bash

ENV_FILE=".env"

if [[ $1 == "sim" ]]; then
  cp .env.sim $ENV_FILE
  echo "✅ Switched to SIMULATOR environment (.env.sim → .env)"
elif [[ $1 == "bstack" ]]; then
  cp .env.bstack $ENV_FILE
  echo "✅ Switched to BROWSERSTACK environment (.env.bstack → .env)"
else
  echo "❌ Invalid option."
  echo "Usage: ./switch_env.sh [sim|bstack]"
  exit 1
fi
