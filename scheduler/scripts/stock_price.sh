set -e


if [ "${BUILD}" = "dev" ]
then
    echo "Fetching stock prices for $(date)"
elif [ "${BUILD}" = "production" ]
then
    python python/parse_stocks.py
fi
