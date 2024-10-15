# Flash de la carte RB5

Cette section vous guidera à travers les étapes nécessaires pour flasher la carte RB5, à savoir que ce n'est pas nécessaire de la flasher, il est très probable que le système linux soit déjà installé sur la RB5.

## Prérequis

- Une carte RB5
- Une alimentation 12V
- Un câble USB-C
- Un ordinateur sous Windows 11
- Une connexion internet

## Étapes

Les étapes présentées ci-dessous sont issues de la documentation de Thundercomm, enrichie par notre expérience pour faciliter la résolution de problèmes.

### Préparation

- Vous devez posséder une compte Thundercomm (<https://www.thundercomm.com/app_en/register>)
- Sur l'ordinateur avec Windows 11
  - Vous devez télécharger SDK Manager (<https://www.thundercomm.com/product/qualcomm-robotics-rb5-development-kit/#sdk-manager>)
  - Vous devez télécharger et installer T-Flash (<https://docs.thundercomm.com/turbox_doc/tools/turbox-flash-user-guide>)
  - Vous devez télécharger et installer Docker (<https://hub.docker.com/editions/community/docker-ce-desktop-windows/>)

*Remarque :* En cas d'erreur au lancement de Docker, vérifiez dans le BIOS si la virtualisation est activée.

### Création de l'environnement

Dans Windows Powershell :

1. Après avoir extrait TC-sdkmanager-x.x.x.zip accédez à to TC/sdkmanager/x.x.x directory

2. Exécutez les commandes suivantes : (extraites de la documentation officielle)

    ```shell
    rm .\Dockerfile
    cmd /c mklink Dockerfile Dockerfile_18.04
    docker build -t ubuntu:18.04-sdkmanager .
    ```

    *Remarque :* pour notre installation, nous avons choisi la plateforme LU1.0, les autres commandes sont disponibles dans la documentation officielle

3. Créez le container Docker (possible en interface graphique Docker)

    ```shell
    docker run -it -d --name sdkmanager_container ubuntu:18.04-sdkmanager
    ```

4. Exécuter sdkmanager au sein du container Docker

    ```shell
    docker exec -it sdkmanager_container sdkmanager
    ```

### Dans SDK Manager

Maintenant que nous avons exécuté SDK Manager, nous pouvons télécharger et repacker l'image à flasher sur la carte.

*Remarque 1:* Il peut arriver qu'il soit impossible de se connecter, essayez de changer votre mot de passe pour des caractères plus simples.
*Remarque 2:* Lorsque `[Y/n]` est proposé, veillez à taper `y` car un appui sur entrée peut bloquer SDK Manager.

1. Connectez-vous à votre compte Thundercomm lorsque cela vous est demandé.
2. Renseignez votre espace de travail sous la forme `/home/hostPC/[working directory]` car nous utilisons Docker.

3. Sélectionnez le bon produit

4. Sélectionnez la bonne platerforme (nous utilisons LU)

5. Sélectionnez la version de la plateforme (nous utilisons LU2.0 en latest)

6. Commencez le processus de repack (40 minutes environ, cela dépend de votre processeur)

7. L'image est enfin générée dans le working directory renseigné auparavant.

*Remarque :* En cas d'erreur lors du processus, essayez sur un autre ordinateur.

### Flasher la carte

1. Copiez le dossier full_build sur votre ordinateur Windows (en dehors du container Docker). Cela est possible avec la command `cp` ou bien par l'interface graphique de Docker.

2. Passez la carte en mode EDL :
   1. Débranchez la carte (alimentation et USB)
   2. Restez enfoncés sur le bouton F_DL
   3. Branchez l'alimentation, puis le cable USB

*Remarque :* Si la carte est bien en mode EDL, elle sera détectée dans T Flash avec le nombre 9008. Si cela ne fonctionne pas, il existe une autre méthode pour le passage en EDL avec adb (voir la documentation de la carte).

1. Utilisez T Flash pour flasher la full_build générée
    1. Sélectionnez "UFS".
    2. Sélectionnez le fichier `prog_firehose_ddr.elf` dans `full_build`. Des fenêtres s'ouvriront successivement, sélectionnez **tous** les fichiers XML.
    3. Assurez-vous que la carte soit bien détectée.
    4. Flashez la carte avec le bouton `Download`

## Conclusion

Les LEDs vertes doivent s'allumer sur la carte après qu'elle ait été flashée.

Pour plus d'informations (source pour cette documentation):
<https://thundercomm.s3.ap-northeast-1.amazonaws.com/uploads/web/common/Qualcomm%20Robotics%20SDK%20Manager%20User%20Guide.pdf>
