set -e

if [ "${BUILD}" = "dev" ]
then
    echo "Fetching transactions for $(date)"
elif [ "${BUILD}" = "production" ]
then
    python python/daily_scrape.py
fi
