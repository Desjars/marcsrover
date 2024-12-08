# Setup de l'ordinateur de développement

Le développement du projet peut se faire sur n'importe quel OS, même si je recommande vivement linux.

## Installation de `uv`

Sur Linux ou MacOS.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Sur windows.

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Récupération du projet

```bash
cd ~/Documents
git clone https://github.com/desjars/marcsrover
cd marcsrover
uv sync --extra host
```
