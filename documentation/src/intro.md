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

Voici les différentes étapes que vous pourrez suivre pour commencer à développer sur le projet :

- Hardware, branchements, etc... : [Hardware](hardware.md)

- Setup de la Raspberry PI : [Setup de la Raspberry PI](sbc.md)
- Setup du microcontrolleur : [Setup du STM32](microcontroller.md)
- Setup de l'ordinateur de développement : [Setup de l'ordinateur de développement](devpc.md)

- Archiecture du projet : [Architecture](architecture.md)
- Qu'est ce que c'est Zenoh ? : [Zenoh](zenoh.md)

# Contribution

Toutes les contributions sont les bienvenues. Pour contribuer, merci de suivre les [instructions](CONTRIBUTING.md).
