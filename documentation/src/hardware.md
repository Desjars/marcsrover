# Hardware

La voiture de base est présentée ici : [Covapsy](https://github.com/ajuton-ens/CourseVoituresAutonomesSaclay/tree/main/Materiel)

Nous avons ajusté les branchements/composants car nous avons visiblement beaucoup d'éléments deffectueux.

## Servo moteur de direction

Le servo moteur de direction a été remplacé par un XL430-W250T de Robotis, pour le driver nous utilisons une Waveshare Servo Driver, qui est branchée
par USBC à un ordinateur (ici la Raspberry PI). L'alimentation passe par l'ancienne alimentation du PCB principal, qui fonctionnait bien.

TODO : Photo du branchement

## IMU

L'IMU rentre en conflit dans le bus I2C donc nous l'avons retiré.

## Capteurs

Les capteurs arrière de la voiture rentraient en conflit avec le bus I2C donc nous les avons retirés.

## Microcontrolleur

Le microcontrolleur utilisé est un Nucleo G4 de STM32. **Il peut être branché en USB et alimenté par la batterie de la voiture**.

## Raspberry PI

La raspberry PI est branchée sous le microcontrolleur, elle est alimentée par le GPIO donc **il ne faut pas brancher de câble USB d'alimentation**.
