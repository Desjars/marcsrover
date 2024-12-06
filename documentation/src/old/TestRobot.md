# Test du Robot

## Test des moteurs

En théorie le micro controlleur STM32 contient déjà le logiciel et il n'y a rien à modifier. Vous pouvez alors tester le bon fonctionnement des moteurs en lançant la commande suivante:

- Branchez l'alimentation batterie du Robot
- Passez l'interrupteur général à ON
- Passez l'interrupteur de l'ESC à ON, vous devriez entendre deux bips espacés d'une seconde

- Appuyez sur le bouton le plus haut de la carte d'extension du STM32, le robot devrait lancer les moteurs pour avancer vers l'avant
- Appuyez sur le bouton le plus bas de la carte d'extension du STM32, le robot devrait lancer les moteurs pour reculer

**Note**: la marche arrière démarre plus lentement que la marche avant, c'est normal.

## Test de la communication et de la caméra

Après avoir suivis toutes les étapes d'installation on peut tester la communication entre le robot et l'ordinateur hôte.

- Allumez la voiture, branchez la carte RB5 sur alimentation secteur (pas d'autre solution pour le moment)
- Connectez la carte RB5 à l'ordinateur hôte avec un câble USB-C, puis entrez dedans avec `adb`
- Tapez ifconfig pour obtenir l'adresse IP de la carte RB5 sur le réseau WIFI auquel elle est connectée
- Ensuite, toujours sur la carte RB5, tapez la commande suivante:

```bash
su pXX # votre promo, e.g p26
cd ~/marcsrover
uv run marcsrover-car ADDRESS_IP_OBTENUE_SUR_IFCONFIG
```

- Sur l'ordinateur hôte, tapez la commande suivante:

```bash
cd ~/marcsrover
uv run marcsrover-host ADDRESS_IP_OBTENUE_SUR_IFCONFIG_DE_LA_CARTE_RB5
```

Vous devriez alors voir apparaître un écran de monitoring sur votre ordinateur, avec le flux vidéo de la caméra du robot et les informations du LiDAR.

## Test avec manette

Vous pouvez aussi brancher une manette PS4, Switch ou Xbox sur l'ordinateur hôte et contrôler le robot avec. Refaites les mêmes étapes que précédemment mais avec la manette de branché.
Puis lancez un nouveau terminal sur votre ordinateur :

```bash
cd ~/marcsrover
uv run src/marcsrover/host/joystick_controller.py
```

Vous devriez pouovoir contrôler le robot avec la manette.
