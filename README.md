# optIRSAM
Développée lors d'un stage de 2 mois au siège de l'assocation IRSAM (Institut National des Sourds et des Aveugles de Marseille), optIRSAM est une application web permettant d'optimiser les tournées de transports des usagers. Cette dernière a été developpée en python en utilisant le framework Django. Voici donc ici une v1 qui sera sans doute amené à évoluer (pour d'autres stagiaires peut être ?).

## Prérequis
Avoir git et pyhton d'installés sur sa machine (au minimum la version trois pour python).
Si ce n'est pas le cas:
- Pour git: [Git - Downloads](https://git-scm.com/downloads)
- Pour python: [Download Python | Python.org](https://www.python.org/downloads/) 

Optionnellement, mais recommandé s'il y a une volonté d'apporter des modifications au code, installer un éditeur de code. VS Code est gratuit, populaire et marche très bien ([Download Visual Studio Code - Mac, Linux, Windows](https://code.visualstudio.com/Download)).
 
## Installation
Afin d'installer le projet et le faire tourner en local sur sa machine, il y a quelques étapes à suivre après avoir validé les prérequis:
1. Aller chercher le projet sur mon repo, pour se faire ouvrez un invite de commande (Powershell sur Windows c'est parfait) et tapez `git clone https://github.com/nathanvanneste/optIRSAM.git` ce qui va créer une copie du projet en local sur votre machine.

2. Placez-vous dans le répertoire du projet copié (par exemple: `cd optIRSAM`).

3. Créer un environnement virtuel. Un environnement virtuel c'est en quelque sorte une configuration de votre machine qui vous permet d'installer des dépendances relatives à un projet sans avoir à les installer de manière définitive sur votre machine. Pour en créer un tapez `python -m venv venv` votre environnement virtuel s'appelle donc `venv` (comme virtual environment).

4. Après la création de l'environnement virtuel il s'agit de l'activer avec:
	- Sur Windows `venv\Scripts\activate`
	- Sur MACOS et Linux `source venv/bin/activate`

	Après activation, vous devriez voir un `(venv)` dans votre bash. Par ailleurs il est possible de désactiver l'environnement virtuel avec la commande `deactivate`.
5. Il vous faudra installer les dépendances du projets. Comme elles sont listés dans un fichier `requirements.txt` vous n'avez qu'à taper `pip install -r requirements.txt`.
6. Ensuite migrez la base de données avec `python manage.py migrate`.
7. Enfin lancez le serveur avec `python manage.py runserver`. Pour arrêter le serveur maintenez `ctrl` + `c`.
L'application est alors disponible sur votre adresse locale, dans un navigateur tapez: `http://127.0.0.1:8000/`.

Une fois ces étapes effectuées l'application tourne en local !
## Utilisation
Une fois installée, vous pouvez simplement faire tourner l'application en local (si elle ne tourne déjà pas).

1. Placez vous dans le répertoire du dépôt local.

2. Activez votre environnement virtuel ( `venv\Scripts\activate` ou `source venv/bin/activate`).

3. Lancez le serveur  `python manage.py runserver`.


Pour permettre au plus grand nombre de profiter de l'application, il est envisageable de la déployer sur un serveur de production en suivant le guide notifié ici [How to deploy Django | Django documentation | Django](https://docs.djangoproject.com/en/5.2/howto/deployment/).