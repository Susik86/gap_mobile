#!/bin/bash

# Usage: ./switch_env.sh bstack or ./switch_env.sh sim
TARGET_ENV=$1

if [ -z "$TARGET_ENV" ]; then
  echo "❌ Missing environment name. Usage: ./switch_env.sh [bstack|sim|qa|dev]"
  exit 1
fi

ENV_FILE="utils/.env.$TARGET_ENV"

if [ ! -f "$ENV_FILE" ]; then
  echo "❌ Environment file not found: $ENV_FILE"
  exit 1
fi

cp "$ENV_FILE" utils/.env
echo "✅ Switched environment to: $TARGET_ENV"
