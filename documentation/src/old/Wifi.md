# Wifi

Pour ajouter une connexion Wifi à votre carte RB5, un système linux doit être installé et l'outil `adb` doit être présent sur votre ordinateur.

Ensuite il faut suivre ces étapes:

```bash
adb pull /data/misc/wifi/wpa_supplicant.conf
```

Puis éditez le fichier `wpa_supplicant.conf` pour ajouter votre réseau wifi (il sera présent sur votre ordinateur à l'endroit où vous avez
éxécuté la commande précedente), de la forme:

```python
network={
ssid="NomDuWifi"
 key_mgmt=WPA-PSK
 pairwise=TKIP CCMP
 group=TKIP CCMP
 psk="MotDePasseDuWifi"
}
```

Enfin, envoyez le fichier modifié sur la carte RB5 avec la commande:

```bash
adb push wpa_supplicant.conf /data/misc/wifi/
adb reboot
```

Vous devez refaire ces étapes pour connecter à un nouveau réseau wifi.
