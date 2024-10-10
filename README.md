# marcsrover

Marcs Rover est un projet du pôle projet Véhicule Autonome de CentraleSupélec. Nous utilisons pour ce projet un ordinateur embarqué
de chez Qualcomm, le RB5. Ce projet est un projet de recherche et développement, et a pour but de développer un véhicule autonome
capable de se déplacer dans un environnement urbain et de fournir une véritable **plateforme de développement** pour les étudiants
facilement utilisable et modifiable.

Nous tenons à remercier Qualcomm pour leur soutien et leur aide dans ce projet.


# Documentation

Merci de suivre la [documentation](documentation/src/SUMMARY.md) pour plus d'informations sur le projet.

# Prochaines tâches

- Faire la capture des informations du LiDAR dans un noeud Zenoh dans ce [fichier](nodes/capture_lidar.py), et bien penser à rajouter le [format de message](nodes/message.py)
- Faire l'affichage des informations du LiDAR avec DearPyGui dans ce [fichier](nodes/stream_lidar.py)
- Encapsuler le code de Brice/Yassine pour le joystick dans un noeud Zenoh dans ce [fichier](nodes/capture_joystick.py), et bien penser à rajouter le [format de message](nodes/message.py)

- Faire un premier test de récupération des infos de l'IMU embarqué dans la realsense D435i en python avec la lib pyrealsense2
