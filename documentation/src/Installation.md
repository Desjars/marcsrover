# Installation des outils

Nous allons utiliser des outils modernes pour programmer le véhicule:

- Python 3.11.10
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

### Installation de Python 3.11.10

Pour installer Python 3.11.10, tapez la commande suivante:

```bash
uv python install 3.11.10
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
uv venv --python 3.11.10
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


# Temporaire

```
cmake .. -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=~/marcsrover/realsense/bin/python  -DFORCE_RSUSB_BACKEND=true -DCMAKE_BUILD_TYPE=release -DPYTHON_INCLUDE_DIR=$(python -c "import sysconfig; print(sysconfig.get_path('include'))")  -DPYTHON_LIBRARY=$(python -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))")
```

link : [ça](https://github.com/IntelRealSense/librealsense/blob/development/doc/installation_raspbian.md#raspbianraspberrypi3-installation)
