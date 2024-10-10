# Installation des outils

Nous allons utiliser des outils modernes pour programmer le véhicule:

- Python 3.12.6
- UV (python package manager)
- Zenoh

## Ordinateur Host (votre ordinateur)

### Installation de `uv`

Sur windows, ouvrez un terminal powershell et tapez la commande suivante:

```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Sur linux/MacOS, ouvrez un terminal et tapez la commande suivante:

```bash
curl -s https://astral.sh/uv/install.sh | bash
```

### Installation de Python 3.12.6

Pour installer Python 3.12.6, tapez la commande suivante:

```bash
uv python install 3.12.6
```

### Installation des dépendances

Pour installer les dépendances, tapez la commande suivante:

```bash
uv pip install -r requirements.txt
```

## Carte RB5

Pour suivre ces étapes vous devez avoir le logiciel `adb` installé sur votre ordinateur, suivre les instructions sur le site officiel de `adb` pour l'installer.

Il est nécessaire de procéder aux mêmes installations sur la carte `RB5`:

Vous devez alimenter la carte RB5 avec une alimentation 12V, et la connecter à votre ordinateur avec un câble USB-C. Ensuite après 1 minute vous devez
lancer dans un terminal, la commande:

```bash
adb shell
su p26
cd ~
curl -s https://astral.sh/uv/install.sh | bash
git clone https://github.com/Desjars/marcsrover.git
cd ~/marcsrover
uv venv
uv pip install -r requirements.txt
```

**Note**: pour cloner le dépôt et installer les dépendances, vous devez avoir un accès internet sur la carte RB5, pour ce faire, sur votre ordinateur host, éxécutez la commande suivante:

```bash
adb pull /data/misc/wifi/wpa_supplicant.conf
```

Puis éditez le fichier `wpa_supplicant.conf` pour ajouter votre réseau wifi, de la forme:

```python
network={
ssid="NomDuWifi"
 key_mgmt=WPA-PSK
 pairwise=TKIP CCMP
 group=TKIP CCMP
 psk="MotDePasseDuWifi"
}
```

Enfin, envoyez le fichier modifié sur la carte RB5 avec la commande:

```bash
adb push wpa_supplicant.conf /data/misc/wifi/
adb reboot
```
