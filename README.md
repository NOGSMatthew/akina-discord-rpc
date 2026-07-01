<div align="center">

<img src="banner2.png" alt="Akina RPC Banner" width="100%"/>

# Akina RPC

**Discord Rich Presence automatique pour la communauté Akina**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Discord](https://img.shields.io/badge/Discord-Rich%20Presence-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.com)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D4?style=flat-square&logo=windows&logoColor=white)](https://microsoft.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

[**Site officiel**](https://donuts-club.com/akina.php) • [**Discord**](https://discord.gg/akina) • [**Télécharger**](https://github.com/NOGSMatthew/akina-discord-rpc/releases/)

</div>

---

## ✦ Aperçu

**Akina RPC** est une application Windows qui affiche automatiquement un **statut Discord personnalisé** (Rich Presence) lorsque vous êtes connecté.  
Elle s'installe en un clic, se lance silencieusement au démarrage du PC et ne nécessite aucune configuration manuelle.



---

## ✦ Fonctionnalités

- 🟣 **Installateur graphique** moderne avec progression en temps réel
- 🔄 **Lancement automatique** au démarrage Windows (registre + dossier Startup)
- 🔇 **Zéro fenêtre** — fonctionne entièrement en arrière-plan via `pythonw.exe`
- 🐍 **Installation Python automatique** si absent sur la machine
- 📦 **pypresence** installé automatiquement via pip
- 🗑️ **Désinstallateur** inclus — suppression propre en un clic
- 💻 Compatible **Windows 10 / 11**

---

## ✦ Installation

### Méthode recommandée — Exécutable

1. Télécharger le dernier `.exe` dans [**Releases**](https://github.com/NOGSMatthew/akina-discord-rpc/releases/)
2. Lancer `AkinaRPC_Installer.exe`
3. Cliquer sur **Installer Akina RPC**
4. C'est tout ✔

> Python n'est **pas requis** — l'installateur le télécharge automatiquement si nécessaire.

---

### Méthode manuelle — Source

```bash
# Cloner le dépôt
git clone https://github.com/ton-user/akina-rpc.git
cd akina-rpc

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'installateur
python installer.py
