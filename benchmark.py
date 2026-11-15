#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suite de validation et benchmark reproductible du harnais GemmAI.
Vérifie :
1. Filtre d'intention (conversation vs action système)
2. Extraction explicite ```fichier:... + triple vérification disque/syntaxe
3. Détection contextuelle de secours (Smart Match) + ordre d'exécution bash
4. Modification de fichier existant et diff unifié
5. Capture d'erreur d'exécution (déclencheur Self-Healing)
"""

import os
import shutil
import tempfile
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agent


def executer_benchmarks():
    """Exécute la suite complète de tests du harnais dans un répertoire isolé."""
    dossier_origine = os.getcwd()
    dossier_temp = tempfile.mkdtemp(prefix="gemmai_bench_")
    resultats = []

    try:
        os.chdir(dossier_temp)

        # 1. Test du filtre d'intention
        cas_conv = ["salut", "Bonjour comment vas-tu ?", "qui es-tu ?", "explique les listes en python"]
        cas_dev = ["crée hello.py", "écris un script test.py", "lance python3 app.py", "corrige main.py"]
        ok_intent = all(not agent.requiert_action_systeme(c) for c in cas_conv) and all(
            agent.requiert_action_systeme(d) for d in cas_dev
        )
        resultats.append(("Filtre d'intention (Conv vs Dev)", ok_intent))

        # 2. Test d'écriture explicite + triple vérification
        rep_explicite = "Voici le fichier :\n```fichier:salut.py\nprint('OK_EXPLICITE')\n```\n"
        actions, err, _ = agent.executer_actions_extraites(rep_explicite, "crée salut.py")
        ok_explicite = (
            not err
            and os.path.isfile("salut.py")
            and "OK_EXPLICITE" in open("salut.py", encoding="utf-8").read()
        )
        resultats.append(("Extraction explicite + Triple vérification", ok_explicite))

        # 3. Test Smart Match contextuel + exécution bash ordonnée
        rep_smart = (
            "Création :\n```\ntouch omni_test.py\n```\n"
            "Code :\n```python\nprint('SMART_OK')\n```\n"
            "Test :\n```bash\npython3 omni_test.py\n```\n"
        )
        actions_s, err_s, _ = agent.executer_actions_extraites(rep_smart, "crée omni_test.py")
        ok_smart = (
            not err_s
            and os.path.isfile("omni_test.py")
            and any("SMART_OK" in a for a in actions_s)
        )
        resultats.append(("Smart Match contextuel + Exécution bash", ok_smart))

        # 4. Test modification de fichier existant (diff couleur)
        rep_modif = "```fichier:salut.py\nprint('OK_MODIFIE')\n```\n"
        _, err_m, _ = agent.executer_actions_extraites(rep_modif, "modifie salut.py")
        ok_modif = not err_m and "OK_MODIFIE" in open("salut.py", encoding="utf-8").read()
        resultats.append(("Modification fichier + Diff unifié", ok_modif))

        # 5. Test détection d'erreur pour boucle Self-Healing
        rep_err = "```bash\npython3 fichier_inexistant_xyz.py\n```\n"
        _, err_d, msg_err = agent.executer_actions_extraites(rep_err, "lance fichier_inexistant_xyz.py")
        ok_err = err_d and ("No such file" in msg_err or "ERREUR" in msg_err)
        resultats.append(("Détection d'erreur (Trigger Self-Healing)", ok_err))

    finally:
        os.chdir(dossier_origine)
        shutil.rmtree(dossier_temp, ignore_errors=True)

    print("\n" + "=" * 60)
    print("RÉSULTATS BENCHMARK HARNAIS GEMMAI")
    print("=" * 60)
    succes = 0
    for nom, ok in resultats:
        statut = "PASS" if ok else "FAIL"
        if ok:
            succes += 1
        print(f"  [{statut}] {nom}")
    print("-" * 60)
    print(f"Score total : {succes}/{len(resultats)} tests réussis")
    print("=" * 60 + "\n")
    return succes == len(resultats)


if __name__ == "__main__":
    ok = executer_benchmarks()
    sys.exit(0 if ok else 1)
