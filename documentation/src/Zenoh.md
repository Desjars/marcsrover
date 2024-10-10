# Configuration de Zenoh

Zenoh est très simple à utiliser, il suffit de lancer les différents programmes python et ils communiqueront entre eux automatiquement. Il faut cependant
spécifier les adresses IP des ordinateurs qui communiquent entre eux.

Pour cela vous devez être connecté au même réseau que les autres ordinateurs, et la carte RB5. Ensuite il faut, sur chaque ordinateur différent,
éditer le fichier `zenoh_config.json` à la racine du projet, et spécifier les adresses IP des autres ordinateurs:

```json
{
  "mode": "peer",
  "connect": {
    "endpoints": [  // Les adresses IP des autres ordinateurs que le votre, avec le port 7447 et le protocole udp
      "udp/{adress1}:7447",
      "udp/{adress2}:7447",
    ]
  },
  "listen": {
    "endpoints": [
      "udp/0.0.0.0:7447"
    ]
  },
  "scouting": {
    "multicast": {
      "enabled": true
    }
  }
}
```

Ensuite dans un noeud Python il faudra écrire:

```python
import zenoh

config = zenoh.Config.from_file("zenoh_config.json")
session = zenoh.open(config)
```
