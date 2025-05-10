#!/bin/zsh

# Fonction pour afficher un message d'aide
show_help() {
  echo "Usage: ./script.sh [build|run]"
  echo ""
  echo "build  : Installe toutes les dépendances pour le backend (Django) et le frontend (Next.js)"
  echo "run    : Lance d'abord le backend (Django), puis le frontend (Next.js)"
  echo "help   : Affiche ce message d'aide"
}

# Vérifier l'argument passé
if [ -z "$1" ]; then
  # Si aucun argument n'est passé, afficher l'aide
  show_help
elif [ "$1" = "build" ]; then
  # Installation du backend (Django)
  echo "Installation des dépendances pour le backend..."
  cd backend
  python3 -m venv venv
  source venv/bin/activate  # Pour macOS/Linux
  pip install django

  # Installation du frontend (Next.js)
  echo "Installation des dépendances pour le frontend..."
  cd ../frontend
  npm install

  echo "Installation terminée ! Vous pouvez maintenant lancer le projet avec 'npm run dev' pour le frontend et 'python3 manage.py runserver' pour le backend."
  cd ../
elif [ "$1" = "run" ]; then
  # Lancer le backend (Django)
  echo "Lancement du backend (Django)..."
  cd backend
  source venv/bin/activate  # Pour macOS/Linux
  python3 manage.py runserver &
  backend_pid=$!  # Sauver l'ID du processus du backend

  # Lancer le frontend (Next.js)
  echo "Lancement du frontend (Next.js)..."
  cd ../frontend
  npm run dev &
  frontend_pid=$!  # Sauver l'ID du processus du frontend

  # Attendre que l'utilisateur appuie sur Ctrl+C pour tout arrêter
  wait $frontend_pid
  wait $backend_pid
else
  # Si une commande inconnue est passée
  echo "Commande inconnue : $1"
  show_help
fi
