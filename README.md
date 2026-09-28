<p align="center">
  <img src="docs/logo.png" width="220" alt="AgriVoice Logo" />
</p>

<h1 align="center">🌾 AgriVoice</h1>

<p align="center">
  <strong>L'assistant agricole intelligent, 100% hors-ligne et en langues locales (Fon, Yorùbá, Français)</strong><br>
  <em>Développé pour les producteurs agricoles du Bénin et d'Afrique de l'Ouest.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Kotlin-2.0.20-7F52FF?logo=kotlin&logoColor=white" alt="Kotlin" />
  <img src="https://img.shields.io/badge/Jetpack_Compose-Material_3-4285F4?logo=android&logoColor=white" alt="Jetpack Compose" />
  <img src="https://img.shields.io/badge/100%25_Offline-Zero_Cloud-22C55E" alt="Offline" />
  <img src="https://img.shields.io/badge/Languages-Fon_%E2%80%A2_Yor%C3%B9b%C3%A1_%E2%80%A2_FR-F59E0B" alt="Languages" />
</p>

---

## 🎯 Problème & Mission

Dans les zones rurales d'Afrique subsaharienne, l'accès aux conseils agricoles fiables de l'**INRAB** (Institut National des Recherches Agricoles du Bénin) est freiné par :
1. **L'analphabétisme et la barrière de la langue :** Beaucoup de producteurs ne lisent pas le français mais parlent couramment le **Fon** ou le **Yorùbá**.
2. **L'absence de connexion Internet :** Réseau 3G/4G inexistant ou forfait trop cher dans les parcelles.
3. **Le manque d'instantanéité :** Les maladies (taches foliaires, chenilles légionnaires) détruisent les récoltes avant l'arrivée d'un conseiller.

**AgriVoice résout ce problème** avec une application mobile Android native **100% Hors-Ligne** et **Voice-First** (pilotée exclusivement par la voix).

---

## 🌟 Fonctionnalités Clés

* 🎙️ **Onboarding Vocal 100% Inclusif :** L'application parle dès la première seconde d'ouverture. Elle guide l'agriculteur par la voix et par les couleurs (*Vert = Fon, Jaune = Yorùbá, Bleu = Français*). **Zéro besoin de savoir lire !**
* 💬 **Chat Vocal Intelligent :** L'agriculteur pose sa question vocalement en Fon ou Yorùbá et reçoit une réponse audio instantanée avec des puces visuelles claires.
* 🌿 **Diagnostic Maladies & Ravageurs :** Recommandations certifiées INRAB pour le maïs, manioc, soja, coton (dosages bio, extraits de neem, bouillie bordelaise).
* 💰 **Cours des Marchés Locaux :** Tarifs en temps réel à Dantokpa, Parakou, Bohicon (Maïs blanc, Soja, Gari en FCFA).
* 🌦️ **Météo & Calendrier des Semis :** Alertes de pluie et fenêtres optimales de semis.
* 📲 **Partage P2P sans Internet :** Distribution de téléphone à téléphone via **Xender / Bluetooth** dans les coopératives agricoles.

---

## 📱 Aperçu de l'Interface

<p align="center">
  <img src="docs/chat_mockup.png" width="340" alt="Interface de Chat AgriVoice" />
</p>

---

## 🏗️ Architecture du Projet

```text
AGRI_VOICE/
├── docs/
│   ├── logo.png                  # Logo officiel AgriVoice
│   └── chat_mockup.png           # Maquette de l'écran de chat
├── app/
│   ├── src/main/java/com/agrivoice/app/
│   │   ├── MainActivity.kt       # Point d'entrée avec gestion de l'Onboarding Vocal
│   │   ├── data/
│   │   │   └── FonPhraseRepository.kt # Dataset de phrases et dictionnaire Fon
│   │   ├── domain/
│   │   │   └── AgriVoiceEngine.kt     # Cerveau de correspondance d'intentions hors-ligne
│   │   ├── ui/
│   │   │   ├── components/            # TopBar, ChatBubbles, InputBar, BottomNavBar, Chips
│   │   │   ├── screens/               # VoiceOnboarding, Home, Chat, Resources, Profile
│   │   │   └── theme/                 # Palette Material 3 aux couleurs d'AgriVoice & Bénin
│   │   └── res/
│   │       ├── drawable/              # logo_agrivoice.png, farmer_hero.jpg
│   │       └── values/                # strings.xml, themes.xml
└── gradle/
    └── libs.versions.toml             # Version Catalog Android moderne
```

---

## 🚀 Lancement & Installation

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/Max-Adis/AgriVoice.git
   ```
2. **Ouvrir dans Android Studio** (Koala / Ladybug ou supérieur).
3. **Lancer la synchronisation Gradle** (`File -> Sync Project with Gradle Files`).
4. **Exécuter sur votre appareil physique ou émulateur** (`Shift + F10` ou bouton **Run ▶**).

---

## 👥 Équipe WinBanD

Projet créé dans le cadre du **Challenge Cursor X Dev Club** par l'équipe **WinBanD** :
* **Max**
* **Byll**
* **Ibrahim**
* **Esperencia**

---

<p align="center">
  <em>AgriVoice — Donnons une voix à chaque agriculteur. 🌱🇧🇯</em>
</p>
