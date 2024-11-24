Intel n'est pas très sympathique avec Python et les autres plateformes que windows, et donc ils proposent des wheels pour des
vieilles versions de Python, et tout ce qui touche à autre chose que Windows x86 est compliqué à installer.

Précédemment nous avons build depuis les sources mais sur une carte comme la RB5 ou une raspberry pi, c'est très long (plusieurs heures).

Donc nous regroupons ici les wheels, que nous avons build soit à la main soit avec des CI/CD, pour les partager avec vous.

- [x] Wheel pour Python3.12.6 pour Linux x86_64
- [ ] Wheel pour Python3.12.6 pour Linux aarch64 (RB5 ou RPI)
- [x] Wheel pour Python3.12.6 et Windows x86_64
- [ ] Wheel pour Python3.12.6 et MacOS aarch64

Ensuite le fichier `pyproject.toml` se charge d'installer la bonne wheel en fonction de la plateforme :

```toml
[tool.uv.sources]
pyrealsense2 = [
    { path = "pyrealsense2/pyrealsense2-2.55.1-cp312-cp312-linux_x86_64.whl", marker = "platform_system == 'Linux' and platform_machine == 'x86_64'" },
    { path = "pyrealsense2/pyrealsense2-2.55.1-cp312-cp312-linux_x86_64.whl", marker = "platform_system == 'Linux' and platform_machine == 'aarch64'" },
    { path = "pyrealsense2/pyrealsense2-2.55.1-cp312-cp312-linux_x86_64.whl", marker = "platform_system == 'Linux' and platform_machine != 'aarch64' and platform_machine != 'x86_64'" },
    { path = "pyrealsense2/pyrealsense2-2.55.1-cp312-cp312-linux_x86_64.whl", marker = "platform_system == 'Darwin' and platform_machine == 'aarch64'" },
    { path = "pyrealsense2/pyrealsense2-2.55.1-cp312-cp312-linux_x86_64.whl", marker = "platform_system == 'Darwin' and platform_machine != 'aarch64'" },
    { path = "pyrealsense2/pyrealsense2-2.55.1-cp312-cp312-linux_x86_64.whl", marker = "platform_system == 'Windows'" },

    { path = "pyrealsense2/pyrealsense2-2.55.1-cp312-cp312-linux_x86_64.whl", marker = "platform_system != 'Darwin' and platform_system != 'Linux' and platform_system != 'Windows'" },
]
```
