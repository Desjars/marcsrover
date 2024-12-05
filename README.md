# MarCSRover : la plateforme de développement pour les véhicules autonomes 100% Python 3.10.15

Marcs Rover est un projet du pôle projet Véhicule Autonome de CentraleSupélec. Nous utilisons pour ce projet un ordinateur embarqué
la raspberry PI 3 Model B. Ce projet est un projet de recherche et développement, et a pour but de développer un véhicule autonome
capable de se déplacer dans un environnement urbain et de fournir une véritable **plateforme de développement** pour les étudiants
facilement utilisable et modifiable.

# Modernité

Nous avons voulu proposer une plateforme de développement facile et moderne : tout se fait en Python 3.10.15, avec un outil de gestion
(`uv`), un framework de communication IPC (`zenoh`) qui permet de développer la plateforme sous la forme d'un graph de tâches.

**Note**: `uv` permet de s'assurer que l'utilisation du projet est simple et rapide, il permet de gérer les dépendances, les environnements virtuels
et de lancer les différents composants du projet.

# Documentation

**End to End project**: Notre but a été de proposer un projet simple, après avoir cloné le repository et installé `uv`, tout se programme
en python très facilement sans se soucier des dépendances, des versions de python etc... Le projet installera (avec `uv`) tout seul le bon
python pour le bon système, créera un environnement virtuel et installera les dépendances souhaitées.

## Tester le véhicule sans modifier le code

Pour tester le véhicule sans modifier le code, c'est très simple. Mettons que vous ayez une voiture fonctionnelle avec le bon programme
dans le microcontrolleur et une Raspberry PI avec `uv` d'installer (se fier à la documentation). Alors, il suffit **sur la voiture** de :

1. De créer un dossier de test

```bash
cd ~/Documents
mkdir test-marcsrover && cd test-marcsrover
```

2. Créer un environnement virtuel et installer le projet

```bash
uv venv --python 3.10.15
uv pip install git+https://github.com/desjars/marcsrover[car]
```

3. Lancer le programme

```bash
uv run car
```

Si tout est bien configuré la voiture devrait être capable de se déplacer toute seule. Il est possible de changer certains paramètres

```bash
uv run car --lidar-port <PORT OF LIDAR> --servo-port <PORT OF SERVO> --microcontroller-port <PORT OF MICROCONTROLLER>
```

où `PORT OF LIDAR`, `PORT OF SERVO` et `PORT OF MICROCONTROLLER` sont les ports respectifs des composants. Par défaut, les ports sont respectivement
`/dev/ttyUSB0`, `/dev/ttyACM1` et `/dev/ttyACM0`.

## Tester le véhicule sans modifier le code **et** en monitorant les données

Pour tester le véhicule sans modifier le code et en monitorant les données, c'est très simple. Il faut que la Raspberry PI soit connectée
au même réseau (Wifi ou Ethernet) qu'un ordinateur. Il faut ensuite récupérer l'adresse IP de la Raspberry PI (par exemple `10.0.0.10`) sur ce réseau.

Ensuite, vous devez suivre les étapes précédentes et lancer le programme avec le paramètre `--ip` :

```bash
uv run car --ip <IP OF RASPBERRY PI>
```

Ensuite vous devez faire presque les mêmes étapes sur votre ordinateur !

1. Créer un dossier de test

```bash
cd ~/Documents
mkdir test-marcsrover && cd test-marcsrover
```

2. Créer un environnement virtuel et installer le projet

```bash
uv venv --python 3.10.15
uv pip install git+https://github.com/desjars/marcsrover[host]
```

3. Lancer le programme

```bash
uv run host --ip <IP OF RASPBERRY PI>
```

## Développer le véhicule

Merci de suivre la [documentation](documentation/src/SUMMARY.md) spécifique.

# Contribution

Toutes les contributions sont les bienvenues. Pour contribuer, merci de suivre les [instructions](CONTRIBUTING.md).
