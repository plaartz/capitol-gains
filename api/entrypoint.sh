set -e

echo "Running Migrations..."
python3 manage.py migrate

if [ "${BUILD}" = "dev" ]
then
    echo "Loading initial fixtures..."
    python3 manage.py loaddata ./api/fixtures/*.json
fi 

echo "Starting server..."
python3 manage.py runserver 0.0.0.0:8000