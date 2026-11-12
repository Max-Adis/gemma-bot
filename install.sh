#!/usr/bin/env bash
# ==============================================================================
# Script d'installation automatique en 1 ligne pour GemmAI
# Usage : curl -fsSL https://.../install.sh | bash
# ==============================================================================

set -e

# Couleurs ANSI
BLEU="\033[94m"
ROUGE="\033[91m"
VERT="\033[92m"
JAUNE="\033[93m"
CYAN="\033[96m"
GRIS="\033[90m"
BOLD="\033[1m"
RESET="\033[0m"

echo -e "${BLEU}${BOLD}"
echo "    ██████╗ ███████╗███╗   ███╗███╗   ███╗ █████╗ ██╗"
echo "   ██╔════╝ ██╔════╝████╗ ████║████╗ ████║██╔══██╗██║"
echo "   ██║  ███╗█████╗  ██╔████╔██║██╔████╔██║███████║██║"
echo "   ██║   ██║██╔══╝  ██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║"
echo "   ╚██████╔╝███████╗██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║"
echo "    ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝"
echo -e "${RESET}"
echo -e "   ${CYAN}${BOLD}Installateur Automatique GemmAI${RESET}"
echo -e "   ${GRIS}Agent Développeur Autonome • Local & Offline${RESET}\n"

# 1. Vérification de Python 3
echo -e "${BLEU}➜${RESET} Vérification de l'environnement..."
if ! command -v python3 &> /dev/null; then
    echo -e "${ROUGE}✖ Erreur : Python 3 est requis mais n'est pas installé.${RESET}"
    exit 1
fi
echo -e "  ${VERT}✔ Python 3 détecté : $(python3 --version)${RESET}"

# 2. Dossier d'installation de GemmAI
INSTALL_DIR="$HOME/.gemmai"
BIN_DIR="/usr/local/bin"

if [ ! -w "$BIN_DIR" ]; then
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
fi

echo -e "\n${BLEU}➜${RESET} Configuration des fichiers dans ${CYAN}$INSTALL_DIR${RESET}..."
mkdir -p "$INSTALL_DIR"

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
if [ -f "$SOURCE_DIR/agent.py" ]; then
    cp "$SOURCE_DIR/agent.py" "$INSTALL_DIR/agent.py"
fi

chmod +x "$INSTALL_DIR/agent.py"

# 3. Création du binaire global 'gemmai'
echo -e "${BLEU}➜${RESET} Configuration de la commande globale ${BOLD}gemmai${RESET}..."

if [ "$BIN_DIR" = "/usr/local/bin" ]; then
    if [ "$EUID" -eq 0 ]; then
        ln -sf "$INSTALL_DIR/agent.py" "$BIN_DIR/gemmai"
    else
        sudo ln -sf "$INSTALL_DIR/agent.py" "$BIN_DIR/gemmai" 2>/dev/null || {
            BIN_DIR="$HOME/.local/bin"
            mkdir -p "$BIN_DIR"
            ln -sf "$INSTALL_DIR/agent.py" "$BIN_DIR/gemmai"
        }
    fi
else
    ln -sf "$INSTALL_DIR/agent.py" "$BIN_DIR/gemmai"
fi

# Vérifier si ~/.local/bin est dans le PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    SHELL_RC="$HOME/.bashrc"
    [ -n "$ZSH_VERSION" ] && SHELL_RC="$HOME/.zshrc"
    echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$SHELL_RC"
fi

# 4. Vérification d'Ollama et du modèle
echo -e "\n${BLEU}➜${RESET} Vérification du moteur IA local..."
if ! command -v ollama &> /dev/null; then
    echo -e "  ${JAUNE}Installation automatique d'Ollama...${RESET}"
    curl -fsSL https://ollama.com/install.sh | sh
fi
echo -e "  ${VERT}✔ Ollama est disponible.${RESET}"

if command -v ollama &> /dev/null; then
    if ! ollama list 2>/dev/null | grep -q "gemma:2b"; then
        echo -e "  ${CYAN}Téléchargement du modèle Gemma 2B (une seule fois)...${RESET}"
        ollama pull gemma:2b
    else
        echo -e "  ${VERT}✔ Modèle 'gemma:2b' prêt.${RESET}"
    fi
fi

echo -e "\n${VERT}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${VERT}${BOLD}🎉 GemmAI a été installé avec succès !${RESET}"
echo -e "${GRIS}Commande disponible : $BIN_DIR/gemmai${RESET}"
echo -e "${VERT}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "\nPour lancer l'agent, tape simplement dans ton terminal :"
echo -e "  ${BLEU}\033[1mgemmai\033[0m\n"
