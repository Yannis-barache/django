#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 n'a pas été trouvée, installez Python3."
    exit
fi

# Prompt for the virtual environment path
read -p "Entrez le chemin absolu de votre venv (laisser vide pour utiliser 'venv' par défaut) : " VENV_PATH

# Use the default if no path is provided
if [ -z "$VENV_PATH" ]; then
    VENV_PATH="venv"
fi

# Create or activate the virtual environment
if [ -d "$VENV_PATH" ]; then
    echo "Activation de la venv à l'emplacement : $VENV_PATH"
    source "$VENV_PATH/bin/activate"
else
    echo "Création d'une nouvelle venv à l'emplacement : $VENV_PATH"
    python3 -m venv "$VENV_PATH"
    source "$VENV_PATH/bin/activate"
fi

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
echo "Creation d'un superuser, suivez les prompts"
python manage.py createsuperuser

# Load initial data
python manage.py loaddata db.json

# Run the development server
python manage.py runserver

echo "Setup fini, accédez au serveur à l'URL suivante : http://localhost:8000/"
echo "Pour accéder à l'interface d'administration, allez à http://localhost:8000/admin/"
echo "Pour lancer le serveur ultérieurement, exécutez la commande suivante : python manage.py runserver (dans le venv)"