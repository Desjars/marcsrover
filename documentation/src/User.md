# User

Avant de procéder aux installations futures vous devez créer un nouvel utilisateur sur la carte RB5, pour ce faire, connectez vous à la carte RB5 avec la commande:

```bash
adb shell
apt install sudo
adduser <username> # Remplacez <username> par "pXX" où XX est le numéro de votre promo, comme password, définissez quelque chose comme "pp" pour "pôle projet""
sudo adduser <username>
sudo usermod -aG sudo <username>
```

Donnez les droits de communication TTY et DIALOUT à l'utilisateur créé:

```bash
sudo usermod -aG tty <username>
sudo usermod -aG dialout <username>
```
