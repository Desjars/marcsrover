# Installation des outils

Nous allons utiliser des outils modernes pour programmer le véhicule:

- Python 3.12.6
- UV (python package manager)
- Zenoh

## Ordinateur Host (votre ordinateur)

### Installation de `uv`

Sur windows, ouvrez un terminal powershell et tapez la commande suivante:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Sur linux/MacOS, ouvrez un terminal et tapez la commande suivante:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation de Python 3.12.6

Pour installer Python 3.12.6, tapez la commande suivante:

```bash
uv python install 3.12.6
```

```bash
cd ~
git clone https://github.com/Desjars/marcsrover.git
cd ~/marcsrover
uv venv --python 3.12.6
uv pip install -r requirements.txt
```

## Carte RB5

Pour suivre ces étapes vous devez avoir le logiciel `adb` installé sur votre ordinateur, suivre les instructions sur le site officiel de `adb` pour l'installer.

Il est nécessaire de procéder aux mêmes installations sur la carte `RB5`:

Vous devez alimenter la carte RB5 avec une alimentation 12V, et la connecter à votre ordinateur avec un câble USB-C. Ensuite après 1 minute vous devez
lancer dans un terminal, la commande:

```bash
adb shell
su pXX # Remplacez pXX par votre nom d'utilisateur, e.g p26, p27, p28, etc.
cd ~
git clone https://github.com/Desjars/marcsrover.git
cd ~/marcsrover
uv venv --python 3.12.6
uv pip install -r requirements.txt
```
