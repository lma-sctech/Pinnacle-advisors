#!/bin/bash
echo "Démarrage du serveur Django..."
echo ""
cd "$(dirname "$0")"
source venv/bin/activate
python manage.py runserver
