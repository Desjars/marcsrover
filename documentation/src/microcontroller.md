# Setup du microcontrolleur

Le microcontrolleur utilisé est un STM32 Nucléo. En théorie il n'y a rien à modifier dans le code.

Son role est simplement d'assurer le déplacement linéaire de la voiture par commande directe du moteur DC Brushed avec un asservissement en vitesse.

Il reçoit un message par port série sous la forme "s0XXXX", où XXXX est un nombre entre 0 et 8000, les valeurs au dessus de 4000 représentent
une vitesse linéaire positive en mm/s et les valeurs en dessous de 4000 représentent une vitesse linéaire négative en mm/s.

## Installation

Il suffit de télécharger CubeIDE sur votre ordinateur, de brancher le microcontrolleur sur votre ordinateur et de flasher le code après avoir ouvert
le projet `cerebri` présent dans le dépôt.

## Test

Sur le PCB d'extension (celui où il y'a un écran), il y'a trois boutons. Celui du haut lance deux actions : un bip sonore, et si l'ESC est allumé
il met en marche le moteur à une vitesse de 1000 mm/s pendant 1 seconde. Vous pouvez vous servir de ce bouton pour tester le microcontrolleur.

Le bouton du milieu est sensé lancer le moteur dans l'autre sens, mais il n'est pas encore bien implémenté.

Le bouton du bas redémarrera le microcontrolleur, utile si vous avez des problèmes de communication.
