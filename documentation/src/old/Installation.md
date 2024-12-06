# Installation des outils

Nous allons utiliser des outils modernes pour programmer le véhicule:

- Python 3.12.6
- UV (python package manager)
- Zenoh

**Cependant**, vous n'avez qu'à installer `uv` : cet outil se chargera tout seul d'installer exactement la bonne version de python au bon endroit,
les dépendances nécessaires etc...

## Ordinateur Host (votre ordinateur)

Sur windows, ouvrez un terminal powershell et tapez la commande suivante:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Sur linux/MacOS, ouvrez un terminal et tapez la commande suivante:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Puis il faut cloner le repository:

```bash
cd ~
git clone https://github.com/Desjars/marcsrover.git
```

## Carte RB5

Pour suivre ces étapes vous devez avoir le logiciel `adb` installé sur votre ordinateur, suivre les instructions sur le site officiel de `adb` pour l'installer.

Il est nécessaire de procéder aux mêmes installations sur la carte `RB5`:

Vous devez alimenter la carte RB5 avec une alimentation 12V, et la connecter à votre ordinateur avec un câble USB-C. Ensuite après 1 minute vous devez
lancer dans un terminal, la commande:

```bash
adb shell
su pXX # Remplacez pXX par votre nom d'utilisateur, e.g p26, p27, p28, etc.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Puis il faut cloner le repository:

```bash
cd ~
git clone https://github.com/Desjars/marcsrover.git
```

## Installation

Comme il y'a plusieurs dépendances il est conseillé de faire cette étape sur un bon Wifi. Une fois le repository cloné vous devez vous y rendre:

```bash
cd ~/marcsrover
```

Puis lancer la commande suivante:

### Ordinateur host
```bash
uv sync --extra host
```

### Carte RB5
```bash
uv sync --extra car
```

Cela va installer toutes les dépendances nécessaires pour le projet.
