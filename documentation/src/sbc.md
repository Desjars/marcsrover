# Setup de la Raspberry PI

Nous utilisons une Raspberry PI. Elle est très simple à prendre en main, peu importe le modèle la procédure est la même.

**Attention** si la voiture vous est fourni avec une Raspberry PI déjà utilisée, il est fort probable qu'il ne soit pas nécessaire
de flasher une nouvelle carte SD. Il suffit de se connecter en `ssh` et de suivre les instructions.

Installer `rpi-manager` sur un ordinateur, sélection le bon modèle de Raspberry PI et la version de Raspberry PI OS que vous voulez.
Ensuite il faut flasher une carte SD avec Raspberry PI OS (toujours grâce à `rpi-manager`). **N'oubliez pas d'activer `ssh`, il
sera plus simple de se connecter à la Raspberry PI**.

Une fois la raspberry PI installée, vous pouvez vous y connecter en `ssh` :

```bash
ssh <le username>@<adresse IP du raspberry PI>
```

Ensuite il faut tout mettre à jour :

```bash
sudo apt update
sudo apt upgrade
```

Ensuite, il faut installer `uv` :

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

vous pouvez ensuite récupérer le projet :

```bash
cd ~/Documents
git clone https://github.com/desjars/marcsrover
```

Et vous pouvez installer tous les composants nécessaire pour le projet :

```bash
cd ~/Documents/marcsrover
uv sync --extra car
```

**Voici un lien utile pour mettre des noms aux ports du LiDAR, du servo moteur et du microcontrolleur** : [ici](https://www.freva.com/assign-fixed-usb-port-names-to-your-raspberry-pi/)
