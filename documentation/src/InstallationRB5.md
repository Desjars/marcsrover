# Installation First Time Card

Cette section est destinée à la première installation des logiciels sur la RB5. C'est à dire après avoir flashé la carte,
il est très probable que le système linux soit déjà installé sur la RB5 et que les outils le soient également.

## Wifi

Vous devez suivre les étapes de la section [Wifi](./Wifi.md) pour connecter votre carte RB5 à un réseau wifi.

## Installation des outils

Avant tout, il faut créer un nouvel utilisateur pour votre année en suivant les étapes de la section [User](./User.md).

L'idée est d'installer des paquets de base avec `apt`.

### Installer les outils

**Je le répète, bous ne devez pas suivre cette section si tout est déjà installé, cette section n'est présente que dans le cas où vous êtes dans une situation
où la carte RB5 a du être flashée de nouveau vierge. Vous risquez simplement de perdre beaucoup de temps si jamais vous faites une connerie sur l'installation**

**Ce qu'il faut retenir c'est qu'il faut surtout créer un nouvel utilisateur pour centraliser votre code, et vous connecter au wifi.**

```bash
su pXX # Remplacez XX par le numéro de votre promo
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:git-core/ppa
sudo apt-get update
sudo apt-get install git curl cmake
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation des drivers

Il est indispensable d'installer les drivers de la IntelRealSenseD435i pour pouvoir utiliser la caméra. Passez cette section
si vous ne voulez pas utiliser cette caméra.

```bash
sudo apt-get install -y libdrm-amdgpu1 libdrm-amdgpu1-dbgsym libdrm-dev libdrm-exynos1 libdrm-exynos1-dbgsym libdrm-freedreno1 libdrm-freedreno1-dbgsym libdrm-nouveau2 libdrm-nouveau2-dbgsym libdrm-omap1 libdrm-omap1-dbgsym libdrm-radeon1 libdrm-radeon1-dbgsym libdrm-tegra0 libdrm-tegra0-dbgsym libdrm2 libdrm2-dbgsym
sudo apt-get install -y libglu1-mesa libglu1-mesa-dev glusterfs-common libglu1-mesa libglu1-mesa-dev libglui-dev libglui2c2
sudo apt-get install -y libglu1-mesa libglu1-mesa-dev mesa-utils mesa-utils-extra xorg-dev libgtk-3-dev libusb-1.0-0-dev
```

```bash
cd /home/
git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense
sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
```

```bash
cd /home/
uv venv --python 3.9.20 .realsense # this is a special environment for all users to use the realsense camera
```

```bash
mkdir /home/librealsense/build
cd /home/librealsense/build
cmake .. -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=~/marcsrover/realsense/bin/python  -DFORCE_RSUSB_BACKEND=true -DCMAKE_BUILD_TYPE=release -DPYTHON_INCLUDE_DIR=/home/$USER/.local/share/uv/python/cpython-3.9.20-linux-aarch64-gnu/include/python3.9  -DPYTHON_LIBRARY=/install/lib
sudo make -j4
sudo make install
```

Si vous rencontrez des problèmes lors de l'installation des drivers, vous pouvez consulter la
[documentation officielle](https://github.com/IntelRealSense/librealsense/blob/development/doc/installation_raspbian.md#raspbianraspberrypi3-installation)
