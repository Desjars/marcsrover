# Configuration du simulateur

Il faut installer le simulateur Webots. Et configurer le bon python. Pour cela il faut aller dans l'onglet "Tools" puis "Preferences" et
dans la section `python`, il faut rentrer le chemin vers l'éxécutable de l'environnement virtuel python pour ce projet. Si vous avez suivi
les instructions précédentes, il s'agit de `~/Documents/marcsrover/.venv/bin/python` pour Linux et de `~/Documents/marcsrover/.venv/Scripts/python.exe`
pour Windows. A savoir, le `~` est un raccourci pour le dossier `home` de l'utilisateur, il peut ne pas fonctionner sur Webots, il faut donc le remplacer
par le chemin absolu, c'est à dire `/home/<username>/Documents/marcsrover/.venv/bin/python` pour Linux et `C:\Users\<username>\Documents\marcsrover\.venv\Scripts\python.exe`
et sur MacOS: `/Users/<username>/Documents/marcsrover/.venv/bin/python`.

Ensuite il faut ouvrir le `World` dans ce projet (`sim/worlds/Piste_CoVAPSy_2023b`)
