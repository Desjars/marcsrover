# Noeuds

Nous choisissons de programmer le véhicule sous forme de noeuds, chaque noeud est un programme qui effectue une tâche spécifique, et communique avec les autres noeuds pour réaliser une tâche plus complexe.

Pour faire cela en Python avec `Zenoh`, il suffit de lancer les différents programmes python et ils communiqueront entre eux automatiquement.

## Structure d'un noeud

Un noeud doit établir une connexion avec le serveur `Zenoh`, et publier des données, ou souscrire à des données.

```python
import zenoh

config = zenoh.Config.from_json5("{}")
session = zenoh.open(config)
```

### Publication de données

Pour publier des données, il suffit de créer un `Publisher` et de publier des données.

```python
import zenoh

config = zenoh.Config.from_json5("{}")
session = zenoh.open(config)

test_publisher = session.declare_publisher("marcsrover/test")

test_publisher.put([0, 4, 8, 4, 3,9].tobytes())
```

### Souscription à des données

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

## Architecture générale

Ne tourne sur chaque composant (ordinateur host ou voiture), qu'un seul logiciel, ce dernier lancera lui même les différents noeuds programmés
dans différents threads afin de simplifier la démarche.

Un noeud ressemble à ceci :

```python
import zenoh
import threading
import json


class Node:
    def __init__(self):
        self.zenoh_config: zenoh.Config = zenoh.Config.from_json5("{}")

        self.zenoh_config.insert_json5(
            "connect/endpoints", json.dumps(["udp/127.0.0.1:7447"])
        )
        self.zenoh_config.insert_json5(
            "listen/endpoints", json.dumps(["udp/127.0.0.1:0"])
        )

    def run(self, stop_event: threading.Event) -> None:
        with zenoh.open(self.zenoh_config) as session:
            while not stop_event.is_set():
                pass

            session.close()

        print("Joystick node stopped")


def launch_node(stop_event: threading.Event) -> None:
    node = Node()

    node.run(stop_event)
```

Puis dans les fichiers `__init__.py` de chacun des modules `host` et `car`, nous lancons les différents noeuds :

```python
monitor = threading.Thread(target=launch_monitor_node, args=(stop_event,))
monitor.start()
```

L'argument `stop_event` permet d'arrêter les différents noeuds en même temps depuis le terminal en appuyant sur `Ctrl+C`.
