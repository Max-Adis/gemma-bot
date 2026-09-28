import os
import subprocess
import ast
import re

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


# ==============================================================================
# 2. LE CERVEAU DE L'AGENT (Boucle ReAct)
# ==============================================================================

def demander_a_gemma(prompt):
    """
    Fonction relais (Placeholder) : 
    Bientôt, elle appellera Ollama avec notre modèle.
    """
    # Ex: On passera ici la commande subprocess vers `ollama run`
    pass

def lancer_agent(objectif):
    """La fameuse boucle Reason + Act (ReAct)"""
    print(f"=== Lancement de l'Agent Gemma ===")
    print(f"Objectif : {objectif}\n")
    
    historique = f"Objectif global: {objectif}\n"
    
    max_iterations = 10
    for i in range(max_iterations):
        print(f"--- Itération {i+1} ---")
        
        # 1. PENSÉE (Reasoning)
        prompt_systeme = (
            "Tu es un agent développeur. Analyse l'historique et décide de la prochaine action.\n"
            "Format de réponse attendu :\n"
            "Pensée: [Ton raisonnement]\n"
            "Action: [nom_outil]([arguments])\n"
        )
        
        # TODO: Relier à la vraie réponse du LLM
        reponse_ia = "Pensée: Je dois analyser le projet.\nAction: extraire_squelette('agent.py')" 
        
        print(reponse_ia)
        
        # 2. ACTION (Extraction de l'outil)
        # TODO: Parser la "reponse_ia" avec des Regex pour lancer appliquer_patch, etc.
        
        # 3. OBSERVATION (Feedback)
        observation = "Observation: (Résultat fictif en attendant le parsing)"
        historique += f"\n{reponse_ia}\n{observation}\n"
        
        # Condition d'arrêt
        if "Action: FIN" in reponse_ia:
            print("Mission accomplie.")
            break
        
        # Pour le test, on coupe à l'itération 1
        break

if __name__ == "__main__":
    print("Initialisation du système...")
    git_checkpoint("Initialisation de l'architecture de l'agent.")
    lancer_agent("Comprendre mon propre code.")
