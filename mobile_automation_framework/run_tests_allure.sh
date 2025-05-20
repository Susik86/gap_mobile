#!/bin/bash

echo "🧹 Cleaning old results..."
rm -rf reports/allure-results reports/allure-report results/screenshots

echo "🧪 Running tests..."
PYTHONPATH=$(pwd) pytest tests/Genius_Meter/create_GM_team/multi_allure_tests.py -s -v --alluredir=reports/allure-results
#PYTHONPATH=$(pwd) pytest tests/ -s -v --alluredir=reports/allure-results

echo "📊 Generating Allure report..."
rm -rf reports/allure-report
if allure generate reports/allure-results --clean -o reports/allure-report; then
    echo "✅ Allure report generated."

    echo "🌐 Starting local HTTP server on port 8888..."
    cd reports/allure-report
    python3 -m http.server 8888 &

    sleep 2  # Give server a moment to start

    echo "🌍 Opening report in browser at http://localhost:8888"
    open http://localhost:8888

    # Optional: go back to project root after serving
    cd ../../
else
    echo "❌ Failed to generate Allure report."
fi
