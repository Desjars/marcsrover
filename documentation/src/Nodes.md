# Noeuds

Nous choisissons de programmer le véhicule sous forme de noeuds, chaque noeud est un programme qui effectue une tâche spécifique, et communique avec les autres noeuds pour réaliser une tâche plus complexe.

Pour faire cela en Python avec `Zenoh`, il suffit de lancer les différents programmes python et ils communiqueront entre eux automatiquement.

## Structure d'un noeud

Un noeud doit établir une connexion avec le serveur `Zenoh`, et publier des données, ou souscrire à des données.

```python
import zenoh

config = zenoh.Config.from_file("zenoh_config.json")
session = zenoh.open(config)
```

## Publication de données

Pour publier des données, il suffit de créer un `Publisher` et de publier des données.

```python
import zenoh

config = zenoh.Config.from_file("zenoh_config.json")
session = zenoh.open(config)

test_publisher = session.declare_publisher("marcsrover/test")

test_publisher.put([0, 4, 8, 4, 3,9].tobytes())
```

## Souscription à des données

Pour souscrire à des données, il suffit de créer un `Subscriber` et de souscrire à des données.

```python
import zenoh
import time

config = zenoh.Config.from_file("zenoh_config.json")
session = zenoh.open(config)

def callback(sample):
    print("Data received: ", sample.payload)

test_subscriber = session.declare_subscriber("marcsrover/test", callback)

while True:
    time.sleep(1)
```

## Exemple complet
