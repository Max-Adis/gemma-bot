#!/usr/bin/env python3
import os
import subprocess
import ast
import re
import json
import urllib.request
import sys
import shutil
import difflib

# Configuration du modèle actif
MODELE_ACTIF = "gemma:2b"

# ==============================================================================
# 0. INTERFACE CLI (Couleurs & Bannière)
# ==============================================================================

# Codes de couleur ANSI
class Couleurs:
    BLEU      = "\033[34m"
    BLEU_VIF  = "\033[94m"
    CYAN      = "\033[96m"
    VERT      = "\033[92m"
    JAUNE     = "\033[93m"
    ROUGE     = "\033[91m"
    GRIS      = "\033[90m"
    BLANC     = "\033[97m"
    BOLD      = "\033[1m"
    RESET     = "\033[0m"

def largeur_visuelle(texte):
    """
    Calcule la largeur visuelle réelle d'une chaîne dans le terminal.
    Les caractères Unicode de type 'boîte' (box-drawing) et 'bloc' (block)
    comptent pour 1 colonne chacun dans la plupart des terminaux Linux.
    """
    # On strip les espaces pour mesurer le contenu pur, puis on rajoute les espaces
    return len(texte)

def centrer_avec_couleur(texte, largeur_totale, couleur="", reset=""):
    """Centre un texte dans largeur_totale colonnes, puis applique la couleur."""
    lv = largeur_visuelle(texte)
    pad_gauche = max(0, (largeur_totale - lv) // 2)
    return " " * pad_gauche + couleur + texte + reset

def afficher_banniere():
    """Affiche la bannière GemmAI : GEMM en bleu, AI en rouge vif, parfaitement centrée."""
    W = shutil.get_terminal_size((100, 24)).columns

    # Chaque ligne est un tuple : (partie GEMM = bleu, partie AI = rouge)
    lignes = [
        ("   ██████╗ ███████╗███╗   ███╗███╗   ███╗", " █████╗ ██╗"),
        ("  ██╔════╝ ██╔════╝████╗ ████║████╗ ████║", "██╔══██╗██║"),
        ("  ██║  ███╗█████╗  ██╔████╔██║██╔████╔██║", "███████║██║"),
        ("  ██║   ██║██╔══╝  ██║╚██╔╝██║██║╚██╔╝██║", "██╔══██║██║"),
        ("  ╚██████╔╝███████╗██║ ╚═╝ ██║██║ ╚═╝ ██║", "██║  ██║██║"),
        ("   ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝", "╚═╝  ╚═╝╚═╝"),
    ]
    st1 = "Agent Développeur Autonome  •  Local & Offline"
    st2 = "Propulsé par Gemma 2B via Ollama  •  CPU Mode"

    # Centrage global basé sur la largeur totale d'une ligne
    largeur_totale = max(len(g) + len(a) for g, a in lignes)
    pad_global = max(0, (W - largeur_totale) // 2)
    indent = " " * pad_global

    print()
    for gemm, ai in lignes:
        print(f"{indent}{Couleurs.BLEU_VIF}{Couleurs.BOLD}{gemm}{Couleurs.ROUGE}{ai}{Couleurs.RESET}")
    print(centrer_avec_couleur(st1, W, Couleurs.CYAN, Couleurs.RESET))
    print(centrer_avec_couleur(st2, W, Couleurs.GRIS, Couleurs.RESET))
    print()

# ==============================================================================
# 1. OUTILS DE HAUTE PRÉCISION ET SÉCURITÉ (L'Arsenal)
# ==============================================================================

def executer_terminal(commande):
    """Exécute une commande bash et retourne le résultat (ou l'erreur)."""
    try:
        resultat = subprocess.run(
            commande, shell=True, check=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return resultat.stdout
    except subprocess.CalledProcessError as e:
        return f"ERREUR (Code {e.returncode}):\n{e.stderr}"

def git_checkpoint(message="Auto-checkpoint avant action"):
    """Crée un point de sauvegarde local pour pouvoir annuler en cas de casse."""
    # On s'assure d'abord qu'on est bien dans un dépôt git
    if not os.path.exists(".git"):
        executer_terminal("git init")
    
    executer_terminal("git add .")
    res = executer_terminal(f'git commit -m "{message}"')
    if "ERREUR" in res and "nothing to commit" not in res.lower():
        return f"Échec du checkpoint: {res}"
    return "Checkpoint Git créé avec succès. Sécurité assurée."

def git_rollback():
    """Annule toutes les modifications depuis le dernier checkpoint."""
    return executer_terminal("git reset --hard HEAD")

def extraire_squelette(chemin_fichier):
    """
    Scanne un fichier Python sans tout lire.
    Ne renvoie que les noms des classes et fonctions (économise la RAM/contexte).
    """
    if not os.path.exists(chemin_fichier):
        return f"Erreur: Le fichier {chemin_fichier} n'existe pas."
    
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            contenu = f.read()
        
        tree = ast.parse(contenu)
        squelette = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                squelette.append(f"Fonction : {node.name} (Ligne {node.lineno})")
            elif isinstance(node, ast.ClassDef):
                squelette.append(f"Classe : {node.name} (Ligne {node.lineno})")
                
        return "\n".join(squelette) if squelette else "Fichier analysé (aucune fonction/classe trouvée)."
    except SyntaxError as e:
        return f"Erreur de syntaxe dans le fichier : {e}"
    except Exception as e:
        return str(e)

def appliquer_patch(chemin_fichier, ancien_texte, nouveau_texte):
    """Applique une modification ultra précise sur un fichier."""
    if not os.path.exists(chemin_fichier):
        return f"Erreur: Fichier introuvable."
    
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        contenu = f.read()
        
    if ancien_texte not in contenu:
        return "Erreur: L'ancien texte n'a pas été trouvé exactement tel quel dans le fichier. Patch annulé."
        
    nouveau_contenu = contenu.replace(ancien_texte, nouveau_texte, 1)
    
    with open(chemin_fichier, "w", encoding="utf-8") as f:
        f.write(nouveau_contenu)
        
    # Validation syntaxique à blanc
    verif = executer_terminal(f"python3 -m py_compile {chemin_fichier}")
    if "ERREUR" in verif:
        git_rollback() # Filet de sécurité !
        return f"Patch annulé ! L'injection a causé une erreur de syntaxe :\n{verif}"
        
    return "Patch appliqué et validé syntaxiquement avec succès."

def lire_fichier_lignes(chemin_fichier, ligne_debut, ligne_fin):
    """
    Lit uniquement un fragment d'un fichier (ex: ligne 50 à 100).
    Critique pour ne pas saturer la mémoire à court terme (16 Go) de Gemma.
    """
    if not os.path.exists(chemin_fichier):
        return f"Erreur: Le fichier {chemin_fichier} n'existe pas."
    
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            lignes = f.readlines()
            
        debut_idx = max(0, ligne_debut - 1)
        fin_idx = min(len(lignes), ligne_fin)
        
        extrait = lignes[debut_idx:fin_idx]
        return f"--- {chemin_fichier} (Lignes {ligne_debut} à {ligne_fin}) ---\n" + "".join(extrait)
    except Exception as e:
        return f"Erreur lors de la lecture : {e}"

def lister_arborescence_propre(chemin="."):
    """
    Scanne les dossiers en filtrant les bruits (.git, __pycache__, node_modules)
    pour donner à l'agent une vision claire du dépôt.
    """
    ignorés = {".git", "__pycache__", "node_modules", "venv", ".env"}
    arborescence = []
    
    for racine, dossiers, fichiers in os.walk(chemin):
        dossiers[:] = [d for d in dossiers if d not in ignorés]
        
        profondeur = racine.replace(chemin, '').count(os.sep)
        indent = "  " * profondeur
        dossier_nom = os.path.basename(racine)
        if dossier_nom == "" or dossier_nom == ".":
            dossier_nom = "Projet"
            
        arborescence.append(f"{indent}📂 {dossier_nom}/")
        
        for fichier in fichiers:
            if not fichier.endswith(".pyc"):
                arborescence.append(f"{indent}  📄 {fichier}")
                
    resultat = "\n".join(arborescence).strip()
    return resultat if resultat else f"Le dossier '{chemin}' est totalement vide ou n'existe pas."

def chercher_mot_cle(mot_cle, chemin="."):
    """
    Recherche globale d'une variable ou fonction (type Grep).
    Permet à l'agent de trouver toutes les utilisations d'une fonction avant de la modifier.
    """
    commande = f'grep -rnw "{chemin}" -e "{mot_cle}" --exclude-dir=.git --exclude-dir=__pycache__'
    resultat = executer_terminal(commande)
    if "ERREUR" in resultat or not resultat.strip():
        return f"Mot-clé '{mot_cle}' introuvable."
    
    lignes_trouvees = resultat.strip().split('\n')
    if len(lignes_trouvees) > 20:
        return "\n".join(lignes_trouvees[:20]) + f"\n... et {len(lignes_trouvees) - 20} autres résultats ignorés."
    return "\n".join(lignes_trouvees)

def afficher_diff_couleur(ancien_texte, nouveau_texte, nom_fichier):
    """Affiche un joli diff unifié en couleurs ANSI dans le terminal."""
    diff = list(difflib.unified_diff(
        ancien_texte.splitlines(),
        nouveau_texte.splitlines(),
        fromfile=f"a/{nom_fichier}",
        tofile=f"b/{nom_fichier}",
        lineterm=""
    ))
    if not diff:
        return
    print(f"\n{Couleurs.CYAN}Diff des modifications ({nom_fichier}) :{Couleurs.RESET}")
    for ligne in diff:
        if ligne.startswith("+++") or ligne.startswith("---"):
            print(f"{Couleurs.BOLD}{ligne}{Couleurs.RESET}")
        elif ligne.startswith("@@"):
            print(f"{Couleurs.CYAN}{ligne}{Couleurs.RESET}")
        elif ligne.startswith("+"):
            print(f"{Couleurs.VERT}{ligne}{Couleurs.RESET}")
        elif ligne.startswith("-"):
            print(f"{Couleurs.ROUGE}{ligne}{Couleurs.RESET}")
        else:
            print(f"{Couleurs.GRIS}{ligne}{Couleurs.RESET}")
    print()

def ecrire_fichier(chemin_fichier, contenu):
    """
    Crée un fichier et vérifie son existence réelle sur le disque avant de confirmer.
    Affiche un diff couleur si le fichier existait déjà.
    """
    try:
        # Lire l'ancien contenu si le fichier existe pour générer le diff
        ancien_contenu = None
        if os.path.exists(chemin_fichier):
            try:
                with open(chemin_fichier, "r", encoding="utf-8") as f:
                    ancien_contenu = f.read()
            except Exception:
                ancien_contenu = None

        # Créer les dossiers parents si nécessaire
        dossier = os.path.dirname(chemin_fichier)
        if dossier and not os.path.exists(dossier):
            os.makedirs(dossier)
        
        # Écriture
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            f.write(contenu)
        
        # ── Vérification 1 : le fichier existe-t-il sur le disque ?
        if not os.path.exists(chemin_fichier):
            return f"ÉCHEC : le fichier '{chemin_fichier}' n'a pas été créé sur le disque."
        
        # ── Vérification 2 : la taille est-elle cohérente ?
        taille_reelle = os.path.getsize(chemin_fichier)
        if taille_reelle == 0 and len(contenu) > 0:
            return f"ÉCHEC : le fichier '{chemin_fichier}' existe mais est vide (0 octets)."
        
        # ── Vérification 3 : relecture et comparaison du contenu
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            contenu_relu = f.read()
        if contenu_relu != contenu:
            return f"ÉCHEC : le contenu relu ne correspond pas à ce qui a été écrit."
        
        # Affichage du diff couleur si modification d'un fichier existant
        if ancien_contenu is not None and ancien_contenu != contenu:
            afficher_diff_couleur(ancien_contenu, contenu, os.path.basename(chemin_fichier))

        # ── Vérification syntaxique Python (bonus)
        if chemin_fichier.endswith(".py"):
            verif = executer_terminal(f"python3 -m py_compile {chemin_fichier}")
            if "Error" in verif or "ERREUR" in verif:
                return f"Fichier créé et vérifié sur disque, mais erreur de syntaxe Python : {verif}"
        
        return f"Fichier '{chemin_fichier}' créé avec succès et vérifié sur disque ({taille_reelle} octets)."
    
    except Exception as e:
        return f"Erreur lors de la création du fichier : {e}"

# ==============================================================================
# 2. LE CERVEAU DE L'AGENT (Boucle ReAct)
# ==============================================================================

def render_markdown_terminal(texte):
    """
    Convertit le Markdown basique en codes ANSI pour le terminal.
    **texte** → GRAS   |   `texte` → CYAN (style code)
    Evite d'afficher les ** bruts à l'écran.
    """
    # **texte** ou __texte__ → gras ANSI
    texte = re.sub(r'\*\*(.*?)\*\*', lambda m: f"{Couleurs.BOLD}{m.group(1)}{Couleurs.RESET}", texte)
    texte = re.sub(r'__(.*?)__', lambda m: f"{Couleurs.BOLD}{m.group(1)}{Couleurs.RESET}", texte)
    # `texte` → cyan style code
    texte = re.sub(r'`([^`]+)`', lambda m: f"{Couleurs.CYAN}{m.group(1)}{Couleurs.RESET}", texte)
    return texte

def lister_ou_changer_modele(arg=""):
    """Permet de voir ou changer le modèle Ollama actif."""
    global MODELE_ACTIF
    arg = arg.strip()
    if arg:
        MODELE_ACTIF = arg
        print(f"\n{Couleurs.VERT}✔ Modèle actif défini sur : {Couleurs.BOLD}{MODELE_ACTIF}{Couleurs.RESET}\n")
        return
        
    try:
        url = "http://localhost:11434/api/tags"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            modeles = [m.get("name") for m in data.get("models", [])]
            print(f"\n{Couleurs.CYAN}Modèles Ollama installés :{Couleurs.RESET}")
            for m in modeles:
                if m == MODELE_ACTIF:
                    print(f"  {Couleurs.VERT}● {Couleurs.BOLD}{m} (actif){Couleurs.RESET}")
                else:
                    print(f"  {Couleurs.GRIS}○ {m}{Couleurs.RESET}")
            print(f"\n{Couleurs.GRIS}Pour changer de modèle : /model <nom_modele>{Couleurs.RESET}\n")
    except Exception:
        print(f"\n{Couleurs.JAUNE}Modèle actif actuel : {MODELE_ACTIF} (Ollama non accessible){Couleurs.RESET}\n")

def demander_a_gemma(prompt):
    """
    Interroge le modèle Gemma via l'API locale d'Ollama avec un effet Streaming.
    Affiche le Markdown converti en temps réel (** → gras, ` → cyan).
    """
    global MODELE_ACTIF
    url = "http://localhost:11434/api/generate"
    data = {
        "model": MODELE_ACTIF,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.2,
        }
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    reponse_complete = ""
    tampon = ""
    try:
        with urllib.request.urlopen(req) as response:
            print(f"\n{Couleurs.BLEU_VIF}✦ GemmAI ({MODELE_ACTIF}) :{Couleurs.RESET}\n")
            for ligne in response:
                if ligne:
                    chunk = json.loads(ligne.decode('utf-8'))
                    texte = chunk.get("response", "")
                    reponse_complete += texte
                    tampon += texte
                    
                    if "\n" in tampon or chunk.get("done"):
                        affichage = render_markdown_terminal(tampon)
                        print(affichage, end="", flush=True)
                        tampon = ""
                    
                    if chunk.get("done"):
                        break
            print("\n")
            return reponse_complete
    except Exception as e:
        return f"Erreur de communication avec Ollama : {e}"

def executer_actions_extraites(texte, objectif=""):
    """
    Détecte et applique automatiquement les actions contenues dans la réponse :
    - Fichiers à créer/écraser
    - Commandes bash à exécuter
    Retourne (actions_effectuees, a_echoue, derniere_erreur)
    """
    actions_effectuees = []
    fichiers_ecrits = set()
    erreur_survenue = False
    derniere_erreur = ""

    # 1. Extraction explicite des fichiers (ex: ```fichier:nom.ext ou ```file:nom.ext ou ```langage:nom.ext)
    pattern_fichiers_explicites = r'```(?:fichier:|file:|[a-zA-Z0-9_-]+:)([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)\n(.*?)```'
    for nom_fichier, contenu in re.findall(pattern_fichiers_explicites, texte, re.DOTALL):
        nom_fichier = nom_fichier.strip()
        if nom_fichier.lower() in ("bash", "sh", "zsh", "python", "py", "json", "yaml", "yml", "markdown", "md"):
            continue
            
        print(f"\n{Couleurs.CYAN}📁 Écriture du fichier : {Couleurs.BOLD}{nom_fichier}{Couleurs.RESET}")
        res = ecrire_fichier(nom_fichier, contenu)
        if "succès" in res:
            print(f"  {Couleurs.VERT}✔ {res}{Couleurs.RESET}")
        else:
            print(f"  {Couleurs.ROUGE}✖ {res}{Couleurs.RESET}")
            erreur_survenue = True
            derniere_erreur = res
        actions_effectuees.append(f"Fichier '{nom_fichier}' : {res}")
        fichiers_ecrits.add(nom_fichier.lower())

    # 2. Détection contextuelle de secours (ex: bloc python sans tag explicite)
    if not fichiers_ecrits:
        candidats_fichiers = re.findall(r'\b([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]{1,5})\b', objectif)
        if not candidats_fichiers:
            candidats_fichiers = re.findall(r'(?:fichier|file|dans|création de|créer)\s+([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]{1,5})', texte, re.IGNORECASE)

        if candidats_fichiers:
            cible = candidats_fichiers[0]
            blocs_code = re.findall(r'```(?:python|py|json|html|css|javascript|js)?\n(.*?)```', texte, re.DOTALL)
            blocs_valides = [b for b in blocs_code if not b.strip().startswith("touch ") and not b.strip().startswith("cat ") and not b.strip().startswith("python3 ")]
            if blocs_valides:
                contenu_a_ecrire = blocs_valides[-1].strip()
                print(f"\n{Couleurs.CYAN}📁 Détection automatique du fichier : {Couleurs.BOLD}{cible}{Couleurs.RESET}")
                res = ecrire_fichier(cible, contenu_a_ecrire)
                if "succès" in res:
                    print(f"  {Couleurs.VERT}✔ {res}{Couleurs.RESET}")
                else:
                    print(f"  {Couleurs.ROUGE}✖ {res}{Couleurs.RESET}")
                    erreur_survenue = True
                    derniere_erreur = res
                actions_effectuees.append(f"Fichier '{cible}' : {res}")
                fichiers_ecrits.add(cible.lower())

    # 3. Extraction et exécution des commandes bash (TOUJOURS APRÈS l'écriture des fichiers !)
    pattern_bash = r'```(?:bash|sh)\n(.*?)```'
    commandes = re.findall(pattern_bash, texte, re.DOTALL)
    
    for bloc_cmd in commandes:
        lignes = [l.strip() for l in bloc_cmd.strip().splitlines() if l.strip() and not l.strip().startswith("#")]
        for cmd in lignes:
            if cmd.startswith("touch ") and any(cmd.lower().endswith(f) for f in fichiers_ecrits):
                continue
                
            print(f"\n{Couleurs.JAUNE}⚡ Exécution : {Couleurs.BOLD}{cmd}{Couleurs.RESET}")
            res = executer_terminal(cmd)
            sortie = res.strip()
            if "ERREUR" in res or "Error" in res or "No such file" in res or "SyntaxError" in res:
                erreur_survenue = True
                derniere_erreur = sortie
                print(f"{Couleurs.ROUGE}{sortie[:600]}{Couleurs.RESET}")
            elif sortie:
                print(f"{Couleurs.GRIS}{sortie[:600]}{Couleurs.RESET}")
            else:
                print(f"  {Couleurs.VERT}✔ Exécuté sans sortie d'erreur.{Couleurs.RESET}")
            actions_effectuees.append(f"Commande '{cmd}' : {sortie if sortie else 'OK'}")

    return actions_effectuees, erreur_survenue, derniere_erreur

def extraire_contexte_fichiers_demandes(objectif):
    """
    Lit automatiquement le contenu des fichiers existants mentionnés dans l'objectif
    pour que Gemma puisse analyser, corriger ou expliquer du code existant.
    """
    fichiers = re.findall(r'\b([a-zA-Z0-9_\-/\\]+\.[a-zA-Z0-9]{1,5})\b', objectif)
    extraits = []
    for f in set(fichiers):
        if os.path.isfile(f):
            try:
                with open(f, "r", encoding="utf-8") as fic:
                    lignes = fic.readlines()
                if len(lignes) <= 100:
                    contenu = "".join(lignes)
                else:
                    contenu = "".join(lignes[:100]) + f"\n... [tronqué, {len(lignes)} lignes au total]"
                extraits.append(f"CONTENU DU FICHIER '{f}' :\n```{contenu}```")
            except Exception:
                pass
    return "\n\n".join(extraits)

def requiert_action_systeme(objectif):
    """
    Vérifie si la demande de l'utilisateur implique une modification réelle du système :
    - création/modification de fichier
    - exécution d'une commande bash
    Si l'utilisateur pose juste une question, salue ou discute, on n'applique aucune action sur le disque !
    """
    obj = objectif.lower()
    declencheurs = [
        "crée", "cree", "créer", "creer", "écris", "ecris", "écrire", "ecrire",
        "ajoute", "ajouter", "génère", "genere", "générer", "generer",
        "modifie", "modifier", "supprime", "supprimer", "efface",
        "lance", "lancer", "exécute", "execute", "exécuter", "executer",
        "teste", "tester", "compile", "compiler", "run", "build", "test",
        "corrige", "corriger", "fix", "patch", "applique", "appliquer",
        "installe", "installer", "pip", "git", "bash", "touch", "mkdir"
    ]
    a_nom_fichier = bool(re.search(r"\b[a-zA-Z0-9_\-]+\.(py|js|ts|html|css|json|sh|txt|md|cpp|c|go|rs)\b", obj))
    a_verbe_action = any(re.search(rf"\b{d}\b", obj) for d in declencheurs)
    return a_verbe_action or a_nom_fichier

def construire_prompt(objectif, historique_dialogue):
    """Construit un prompt clair, compact et contextualisé pour Gemma."""
    arbo = lister_arborescence_propre(".")
    if not arbo or "vide" in arbo.lower() or "n'existe pas" in arbo.lower():
        info_dossier = "Le dossier actuel est vide."
    else:
        lignes_arbo = [l for l in arbo.splitlines() if l.strip()][:15]
        info_dossier = "Fichiers du projet actuel :\n" + "\n".join(lignes_arbo)

    contexte_fichiers = extraire_contexte_fichiers_demandes(objectif)
    if contexte_fichiers:
        info_dossier += f"\n\n{contexte_fichiers}"

    prompt = (
        "Tu es GemmAI, un assistant développeur IA interactif en ligne de commande (comme Gemini CLI).\n"
        "Tu réponds aux questions, écris du code et aides l'utilisateur dans son projet.\n\n"
        f"CONTEXTE DU PROJET :\n"
        f"Répertoire : {os.getcwd()}\n"
        f"{info_dossier}\n\n"
        "RÈGLES FONDAMENTALES (STRICTES) :\n"
        "1. Si l'utilisateur te salue ou pose une question générale, RÉPONDS UNIQUEMENT EN TEXTE SIMPLE. Ne crée AUCUN fichier et ne lance AUCUNE commande !\n"
        "2. Pour CRÉER ou MODIFIER un fichier (seulement si demandé) : utilise un bloc avec le nom du fichier :\n"
        "```fichier:nom_du_fichier.ext\n"
        "# code ici\n"
        "```\n"
        "3. Pour EXÉCUTER une commande terminal (seulement si demandé) : utilise un bloc bash :\n"
        "```bash\n"
        "commande\n"
        "```\n"
        "4. Sois direct, concis et ne fais que ce qui est explicitement demandé.\n\n"
        f"DEMANDE DE L'UTILISATEUR : {objectif}\n\n"
        "GEMMAI :"
    )
    
    if historique_dialogue:
        prompt += "\nHISTORIQUE RÉCENT :\n"
        for role, msg in historique_dialogue[-4:]:
            prompt += f"{role}: {msg}\n"

    return prompt

def lancer_agent(objectif, historique_dialogue=None):
    """
    Moteur interactif style Gemini CLI avec Auto-Correction (Self-Healing).
    """
    if historique_dialogue is None:
        historique_dialogue = []
        
    prompt = construire_prompt(objectif, historique_dialogue)
    reponse_ia = demander_a_gemma(prompt).strip()
    
    if "Erreur de communication" in reponse_ia:
        print(f"\n{Couleurs.ROUGE}❌ Le serveur Ollama n'est pas accessible.{Couleurs.RESET}")
        print(f"{Couleurs.JAUNE}💡 Lance 'ollama serve' dans un autre terminal.{Couleurs.RESET}\n")
        return

    # Si la demande est une simple discussion ou question théorique, AUCUNE action n'est exécutée sur le disque !
    if not requiert_action_systeme(objectif):
        historique_dialogue.append(("Utilisateur", objectif))
        historique_dialogue.append(("GemmAI", reponse_ia[:250]))
        return
        
    actions, a_echoue, derniere_erreur = executer_actions_extraites(reponse_ia, objectif)
    
    # ── BOUCLE D'AUTO-CORRECTION (Self-Healing Loop) ──────────────────────────
    max_essais_correction = 2
    essai = 0
    while a_echoue and derniere_erreur and essai < max_essais_correction:
        essai += 1
        print(f"\n{Couleurs.JAUNE}🔄 Détection d'erreur : GemmAI lance l'auto-correction autonome (Essai {essai}/{max_essais_correction})...{Couleurs.RESET}")
        prompt_correction = (
            f"L'exécution précédente a échoué avec l'erreur suivante :\n{derniere_erreur[:400]}\n\n"
            "Corrige le code pour résoudre ce problème. Fournis directement le bloc ```fichier:nom_du_fichier avec le code corrigé complet, "
            "suivi du bloc ```bash pour tester.\n\n"
            "CORRECTION :"
        )
        reponse_correction = demander_a_gemma(prompt_correction).strip()
        actions_corr, a_echoue, derniere_erreur = executer_actions_extraites(reponse_correction, objectif)
        actions.extend(actions_corr)
        if not a_echoue:
            print(f"\n{Couleurs.VERT}✔ Auto-correction réussie !{Couleurs.RESET}")
            break
    # ──────────────────────────────────────────────────────────────────────────
    
    # Mémoriser dans l'historique
    historique_dialogue.append(("Utilisateur", objectif))
    resume = " ; ".join(actions) if actions else "Réponse fournie"
    historique_dialogue.append(("GemmAI", reponse_ia[:250]))
    
    if actions:
        if a_echoue:
            print(f"\n{Couleurs.JAUNE}⚠️ Des erreurs subsistent après tentative d'auto-correction.{Couleurs.RESET}")
        else:
            print(f"\n{Couleurs.VERT}{Couleurs.BOLD}✅ Mission accomplie avec succès !{Couleurs.RESET}")

if __name__ == "__main__":
    REPERTOIRE_PROJET = os.getcwd()
    afficher_banniere()
    
    print(f"{Couleurs.GRIS}  Répertoire de travail : {Couleurs.BLEU_VIF}{REPERTOIRE_PROJET}{Couleurs.RESET}")
    print(f"{Couleurs.GRIS}  Commandes utiles : /clear, /files, /undo (annuler), /model (changer de modèle), 'quitter'{Couleurs.RESET}\n")
    
    os.chdir(REPERTOIRE_PROJET)
    historique_session = []
    
    while True:
        try:
            objectif = input(f"{Couleurs.BLEU_VIF}{Couleurs.BOLD}GemmAI >{Couleurs.RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{Couleurs.GRIS}Au revoir !{Couleurs.RESET}\n")
            sys.exit(0)
            
        if not objectif:
            continue
            
        cmd_bas = objectif.lower()
        if cmd_bas in ("quitter", "exit", "quit", "/bye", "/q"):
            print(f"\n{Couleurs.GRIS}Au revoir !{Couleurs.RESET}\n")
            break
        elif cmd_bas in ("/clear", "/reset"):
            historique_session.clear()
            print(f"\n{Couleurs.VERT}✔ Historique de session réinitialisé.{Couleurs.RESET}\n")
            continue
        elif cmd_bas in ("/files", "/ls"):
            arbo = lister_arborescence_propre(".")
            print(f"\n{Couleurs.CYAN}📁 Fichiers du projet :{Couleurs.RESET}\n{arbo}\n")
            continue
        elif cmd_bas.startswith("/model"):
            parties = objectif.split(maxsplit=1)
            arg_modele = parties[1] if len(parties) > 1 else ""
            lister_ou_changer_modele(arg_modele)
            continue
        elif cmd_bas in ("/undo", "/rollback"):
            print(f"\n{Couleurs.JAUNE}⏪ Annulation des modifications...{Couleurs.RESET}")
            res = git_rollback()
            executer_terminal("git clean -fd")
            print(f"{Couleurs.VERT}✔ Projet restauré à son état précédent.{Couleurs.RESET}\n")
            continue
        elif cmd_bas in ("/help", "/?"):
            print(f"\n{Couleurs.CYAN}Aide GemmAI :{Couleurs.RESET}")
            print("  - Pose n'importe quelle question ou donne un ordre de dev (ex: 'crée hello.py')")
            print("  - /files : Liste les fichiers du projet")
            print("  - /undo  : Annule les dernières modifications (Git rollback instantané)")
            print("  - /model : Affiche ou change le modèle actif (ex: /model gemma:2b)")
            print("  - /clear : Efface la mémoire de la conversation")
            print("  - quitter : Quitter l'application\n")
            continue
        
        # Checkpoint Git automatique de sécurité avant chaque opération
        git_checkpoint(f"Checkpoint GemmAI : {objectif[:50]}")
        lancer_agent(objectif, historique_session)
        print(f"\n{Couleurs.GRIS}{'─' * 60}{Couleurs.RESET}\n")
