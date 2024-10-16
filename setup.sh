#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 n'a pas été trouvée, installez Python3."
    exit
fi

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Check for the --skip-bootstrap parameter
SKIP_BOOTSTRAP=false
for arg in "$@"
do
    if [ "$arg" == "--skip-bootstrap" ]; then
        SKIP_BOOTSTRAP=true
        break
    fi
done

# Conditionally install Bootstrap
if [ "$SKIP_BOOTSTRAP" = false ]; then
    npm install
    mv node_modules/ firsttuto/LesProduits/static/
fi


# Apply migrations to set up the database
python manage.py migrate

# Create a superuser
echo "Creation d'un superuser suivez les prompts"
python manage.py createsuperuser

# Populate the database with initial data if you have a fixture
# Uncomment the following line if you have a fixture file
python manage.py loaddata db.json

# Run the development server
python manage.py runserver


echo "Setup fini, accédez au serveur au l'url suivant http://localhost:8000/"
echo "Pour accéder à l'interface d'administration, allez à http://localhost:8000/admin/"
echo "Pour lancer le serveur ultérieurement, exécutez la commande suivante: python manage.py runserver (dans le venv)"


