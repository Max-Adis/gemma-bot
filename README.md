# 🤖 GemmAI : Agent Développeur Autonome Local & Offline

> **Compétition Officielle Kaggle : "The Gemma 4 Developer Agent" ($100k Prize)**  
> **Lead Technique :** Max_Adis  
> **Modèle :** Google Gemma (2B / 7B) quantifié 4-bit • CPU-Only • 100% Hors-Ligne • Max 16 Go RAM

[![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Offline First](https://img.shields.io/badge/offline-100%25-green.svg)](#)
[![Kaggle 100k](https://img.shields.io/badge/Kaggle-The%20Gemma%204%20Agent-orange.svg)](#)

---

## ⚡ Installation Rapide en 1 Ligne (Multiplateforme)

### 🐧 Linux & 🍎 macOS
Ouvrez un terminal et collez :
```bash
curl -fsSL https://raw.githubusercontent.com/Max-Adis/gemma-bot/main/install.sh | bash
```

### 🪟 Windows (PowerShell)
Ouvrez PowerShell (ou Windows Terminal) et collez :
```powershell
irm https://raw.githubusercontent.com/Max-Adis/gemma-bot/main/install.ps1 | iex
```

---

## 🚀 Démarrage

Une fois installé, lancez simplement :
```bash
gemmai
```

---

## 🌟 Fonctionnalités Clés & Super-Pouvoirs

* ⚡ **Architecture Directe (Style Gemini CLI) :** Inférence et streaming ANSI en temps réel, génération directe de fichiers sans boucles de pensée verbeuses.
* 🔄 **Boucle d'Auto-Correction (Self-Healing) :** Capture automatique des erreurs de syntaxe ou des Tracebacks d'exécution et réparation du code en circuit fermé sans intervention humaine.
* ⏪ **Rollback Instantané (`/undo`) :** Checkpoints Git automatiques avant chaque action. Annulation instantanée sans risque de perte de code.
* 📊 **Diffs Couleur Visuels :** Rendu visuel immédiat dans le terminal des lignes modifiées (vert pour les ajouts, rouge pour les suppressions).
* 🔒 **Triple Vérification d'Écriture :** Validation de présence physique sur disque, test de taille, comparaison du contenu relecture/écriture et compilation `python3 -m py_compile`.
* 🧠 **Analyse Contextuelle de Code :** Détection automatique des fichiers du projet mentionnés et injection intelligente dans la réflexion.
* 🛡️ **Filtrage d'Intention :** Distinction stricte entre conversation/salutations polies et véritables actions de développement système.
* 🔀 **Bascule de Modèle à Chaud (`/model`) :** Changez de modèle Ollama en direct sans redémarrer le script.

---

## ⌨️ Commandes Utiles dans l'Invite GemmAI

| Commande | Action |
| :--- | :--- |
| `/files` ou `/ls` | Affiche l'arborescence des fichiers du projet |
| `/undo` | Annule immédiatement les dernières modifications (Rollback Git) |
| `/model <nom>` | Affiche ou change le modèle local actif |
| `/clear` | Réinitialise l'historique de la conversation |
| `/help` | Affiche l'aide interactive |
| `quitter` | Quitte GemmAI |

---

## 📄 Documentation & Rapport Technique

Consultez le rapport d'ingénierie complet et la feuille de route stratégique pour la compétition Kaggle :  
👉 **[Rapport_Travaux_et_Objectifs_GemmAI.pdf](Rapport_Travaux_et_Objectifs_GemmAI.pdf)**

---

## 📜 Licence
Projet open source développé par **Max_Adis** dans le cadre de la compétition Kaggle 2026.
