# marcsrover

Marcs Rover est un projet du pôle projet Véhicule Autonome de CentraleSupélec. Nous utilisons pour ce projet un ordinateur embarqué
de chez Qualcomm, le RB5. Ce projet est un projet de recherche et développement, et a pour but de développer un véhicule autonome
capable de se déplacer dans un environnement urbain et de fournir une véritable **plateforme de développement** pour les étudiants
facilement utilisable et modifiable.

Nous tenons à remercier Qualcomm pour leur soutien et leur aide dans ce projet.

# Installation

Nous voulons utiliser des technologies récentes pour ce véhicule, et se passser de mauvais outils comme ROS. Nous avons donc décidé
d'utiliser Dora-RS, un framework de robotique open-source, et Zenoh, un middleware de communication.

Le véhicule doit pouvoir se programmer entièrement en Python, et pour cela nous allors utiliser le gestionnaire de projet `uv` pour
installer le bon python et les bonnes bibliothèques.

## Installation de `uv`

Sur windows, ouvrez un terminal powershell et tapez la commande suivante:

```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Sur linux/MacOS, ouvrez un terminal et tapez la commande suivante:

```bash
curl -s https://astral.sh/uv/install.sh | bash
```

## Installation de Python 3.12.6

Pour installer Python 3.12.6, tapez la commande suivante:

```bash
uv python install 3.12.6
```

## Installation du CLI `dora`

Sur windows, ouvrez un terminal powershell et tapez la commande suivante:

```bash
powershell -c "irm https://raw.githubusercontent.com/dora-rs/dora/main/install.ps1 | iex"
```

Sur linux/MacOS, ouvrez un terminal et tapez la commande suivante:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/dora-rs/dora/main/install.sh | bash
```

# Utilisation

Tout ce qu'il faut est probablement déjà sur le véhicule, il faut désormais récupérer les logiciels de contrôle du véhicule côté host, il vous faut alors
cloner ce dépôt.

```bash
git clone https://github.com/Desjars/marcsrover.git
```

Ensuite, il vous faut accéder au dossier du projet avec un terminal, et installer les dépendances avec `uv`:

```bash
cd ~/???/marcsrover
uv venv
uv pip install -r requirements.txt
```
