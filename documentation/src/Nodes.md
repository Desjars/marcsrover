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

Merci de suivre la structure, en l'adaptant. Elle doit contenir:

- La déclaration des messages dans le module `message.py`
- L'intégration des messages dans le noeud
- La création d'une classe pour encapsuler le noeud
- La création d'une méthode `run` pour lancer le noeud
- La création d'une méthode `close` pour fermer le noeud
- L'ouverture d'une session `Zenoh` etc...

```python
import signal
import time
import threading

import zenoh

class NodeTemplate:
    def __init__(self):

        # Register signal handlers
        signal.signal(signal.SIGINT, self.ctrl_c_signal)
        signal.signal(signal.SIGTERM, self.ctrl_c_signal)

        self.running = True
        self.mutex = threading.Lock()

        # Create node variables

        # Create zenoh session
        config = zenoh.Config.from_file("zenoh_config.json")
        self.session = zenoh.open(config)

        # Create zenoh pub/sub
        self.stop_handler = self.session.declare_subscriber("marcsrover/stop", self.zenoh_stop_signal)

    def run(self):
        while True:
            # Check if the node should stop

            self.mutex.acquire()
            running = self.running
            self.mutex.release()

            if not running:
                break

            # Put your update code here

            time.sleep(1)

        self.close()

    def close(self):
        self.stop_handler.undeclare()
        self.session.close()

    def ctrl_c_signal(self, signum, frame):
        # Stop the node

        self.mutex.acquire()
        self.running = False
        self.mutex.release()

        # Put your cleanup code here

    def zenoh_stop_signal(self, sample):
        # Stop the node

        self.mutex.acquire()
        self.running = False
        self.mutex.release()

if __name__ == "__main__":
    node = NodeTemplate()
    node.run()
```
