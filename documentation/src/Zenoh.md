# Zenoh Configuration

Zenoh est très simple à utiliser, il suffit de lancer les différents programmes python et ils communiqueront entre eux automatiquement. Il faut cependant
spécifier les adresses IP des ordinateurs qui communiquent entre eux.

Pour cela vous devez être connecté au même réseau que les autres ordinateurs, et la carte RB5. Ensuite il faut, sur chaque ordinateur différent,
éditer le fichier `zenoh_config.json` à la racine du projet, et spécifier les adresses IP des autres ordinateurs:

La configuration de base est celle ci:

```json
{
  "mode": "peer",
  "connect": {
    "endpoints": []
  },
  "listen": {
    "endpoints": [
      "udp/localhost:0",
      "udp/127.0.0.1:0"
    ]
  },
  "scouting": {
    "multicast": {
      "enabled": true
    }
  }
}
```

Il faut ouvrir des listener sur chaque interface réseau que l'on veut, et spécifier le port 0 pour que le système choisisse un port libre.
Par exemple `localhost:0` ouvrira un listener sur l'interface de réseau local, et `127.0.0.1:0` sur l'interface de loopback (wifi).

Si vous vous connectez à un autre ordinateur par Ethernet, vous devez connaître votre IP (que ce soit vous ou la RB5), par exemple :
- Host: `169.254.4.2`
- RB5: `169.254.4.1`

Dans cette situation, il faut différencier le fichier `zenoh_config.json` de chaque ordinateur, et spécifier des adresses IP différentes pour chaque ordinateur:

- Sur l'host, rajouter un endpoint de `connect` avec le protocole `udp`, et le port `7447`, et
rajouter un listener sur l'interface éthernet: `udp/169.254.4.2:0`

```json
"connect": {
  "endpoints": [
    "udp/169.254.4.1:7447"
  ]
},
"listen": {
  "endpoints": [
    ...,
    "udp/169.254.4.2:0"
  ]
},

- Sur la RB5, rajouter un endpoint de `connect` avec le protocole `udp`, et le port `7447`, et
rajouter un listener sur l'interface éthernet: `udp/169.254.1:0`

```json
"connect": {
  "endpoints": [
    "udp/169.254.4.2:7447"
  ]
},
"listen": {
  "endpoints": [
    ...,
    "udp/169.254.4.1:0"
  ]
},

Sur Ubuntu, il faut créer un service qui se lancera au démarage:

```bash
sudo nano /etc/systemd/system/multicast-lo.service
```

Et y écrire:

```bash
[Unit]
Description=Enable Multicast on Loopback

[Service]
Type=oneshot
ExecStart=/usr/sbin/ip link set lo multicast on

[Install]
WantedBy=multi-user.target
```

Ensuite il faut activer le service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable multicast-lo.service
sudo systemctl start multicast-lo.service
```
