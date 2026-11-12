#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas personnalisé pour ajouter les en-têtes et la numérotation 'Page X sur Y'."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # En-tête (page 2 et suivantes)
        if self._pageNumber > 1:
            self.drawString(42, 808, "GemmAI — Agent Développeur Autonome • Compétition Kaggle 2026")
            self.drawRightString(553, 808, "Lead Technique : Max_Adis")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(42, 802, 553, 802)

        # Pied de page (toutes les pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(42, 35, 553, 35)
        
        self.drawString(42, 24, "Confidentiel & Propriétaire • Projet GemmAI Kaggle ($100k)")
        page_text = f"Page {self._pageNumber} sur {page_count}"
        self.drawRightString(553, 24, page_text)
        self.restoreState()

def build_pdf(filename="/home/maxadis/Téléchargements/GEMMA BOT/Rapport_Travaux_et_Objectifs_GemmAI.pdf"):
    # Marges optimisées : 42 pt (~1.5 cm)
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=42,
        rightMargin=42,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    
    # Palette de couleurs pro
    c_primary = colors.HexColor("#1E3A8A")    # Bleu Marine profond
    c_secondary = colors.HexColor("#0284C7")  # Bleu Cyan vif
    c_dark = colors.HexColor("#0F172A")       # Texte sombre quasi-noir
    c_gray = colors.HexColor("#475569")       # Gris texte secondaire
    c_bg_light = colors.HexColor("#F8FAFC")   # Fond carte clair
    c_border = colors.HexColor("#E2E8F0")     # Bordure subtile
    c_success = colors.HexColor("#059669")    # Vert succès
    c_accent = colors.HexColor("#D97706")     # Ambre/Or

    # Styles typographiques compacts & élégants
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary,
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=c_secondary,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        leftIndent=10,
        spaceAfter=2
    )

    card_text_style = ParagraphStyle(
        'CardText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_primary
    )

    meta_val_style = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    story = []

    # ── BANNIÈRE EN-TÊTE ──────────────────────────────────────────────────────
    story.append(Paragraph("GEMMAI : AGENT DÉVELOPPEUR AUTONOME", title_style))
    story.append(Paragraph("Rapport d'Ingénierie, Travaux Réalisés sur le Modèle & Objectifs Visés", subtitle_style))
    
    # Tableau de cadrage / métadonnées
    meta_data = [
        [
            Paragraph("<b>Cadre du Projet :</b>", meta_label_style),
            Paragraph("Compétition Kaggle <i>« The Gemma 4 Developer Agent »</i>", meta_val_style),
            Paragraph("<b>Cagnotte Globale :</b>", meta_label_style),
            Paragraph("<b>100 000 $ USD</b>", meta_val_style)
        ],
        [
            Paragraph("<b>Lead Technique :</b>", meta_label_style),
            Paragraph("Max_Adis (Maker, Développeur & Ingénieur)", meta_val_style),
            Paragraph("<b>Échéance Finale :</b>", meta_label_style),
            Paragraph("<b>25 Novembre 2026</b>", meta_val_style)
        ],
        [
            Paragraph("<b>Modèle Exploité :</b>", meta_label_style),
            Paragraph("Gemma (2B / 7B) quantifié 4-bit (Offline / CPU)", meta_val_style),
            Paragraph("<b>Contrainte Matérielle :</b>", meta_label_style),
            Paragraph("Grand public (Max 16 Go RAM, 0 API Cloud)", meta_val_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[105, 175, 110, 121])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 4))

    # ── 1. SYNTHÈSE EXÉCUTIVE ET VISION ───────────────────────────────────────
    story.append(Paragraph("1. Synthèse Exécutive & Vision Stratégique", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=c_primary, spaceBefore=1, spaceAfter=4))
    
    story.append(Paragraph(
        "Le projet <b>GemmAI</b> a été conçu pour répondre au défi de la compétition officielle Kaggle dotée de <b>100 000 $</b> : "
        "développer un <b>agent de génie logiciel autonome fonctionnant hors ligne</b> sur du matériel grand public (16 Go RAM maximum, mode CPU). "
        "Propulsé par la famille de modèles ouverts <b>Gemma de Google</b>, GemmAI agit comme un ingénieur autonome capable d'explorer un dépôt Git, "
        "d'écrire et modifier du code source, d'exécuter des tests en console, et d'auto-corriger ses bugs en boucle fermée sans intervention humaine.",
        body_style
    ))

    # ── 2. TRAVAUX ET MUTATION ARCHITECTURALE DU MODÈLE ───────────────────────
    story.append(Paragraph("2. Bilan des Travaux Réalisés sur le Modèle & le Moteur", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=c_primary, spaceBefore=1, spaceAfter=4))

    story.append(Paragraph("A. Élimination des Limites du Paradigme ReAct Classique", h2_style))
    story.append(Paragraph(
        "Sur les modèles compacts (SLM) comme Gemma 2B, le paradigme ReAct verbeux traditionnel provoquait des dysfonctionnements critiques : "
        "1) <b>Syndrome du perroquet</b> : recopie bête des exemples du prompt, 2) <b>Boucles infinies</b> d'exploration sur répertoires vides, "
        "et 3) <b>Plantages de parsing</b> dus aux conflits de guillemets imbriqués dans les chaînes de caractères.",
        body_style
    ))

    story.append(Paragraph("B. Transition vers l'Architecture Directe « Style Gemini CLI »", h2_style))
    story.append(Paragraph(
        "Nous avons opéré une <b>refonte architecturale complète</b> en adoptant une approche par action directe inspirée de <i>Gemini CLI</i> et <i>Claude Code</i> :",
        body_style
    ))
    
    comparaison_data = [
        [
            Paragraph("<b>Critère</b>", meta_label_style),
            Paragraph("<b>Architecture Précédente (ReAct lourd)</b>", meta_label_style),
            Paragraph("<b>Architecture GemmAI Actuelle (Gemini CLI)</b>", meta_label_style)
        ],
        [
            Paragraph("<b>Format de sortie</b>", meta_label_style),
            Paragraph("JSON strict complexe ou eval() instable", card_text_style),
            Paragraph("<b>Blocs markdown étiquetés directs</b> (```fichier:...) et streaming propre", card_text_style)
        ],
        [
            Paragraph("<b>Contexte Projet</b>", meta_label_style),
            Paragraph("Outil manuel à relancer à chaque itération", card_text_style),
            Paragraph("<b>Injection dynamique automatique</b> du dossier et des fichiers existants", card_text_style)
        ],
        [
            Paragraph("<b>Fiabilité parsing</b>", meta_label_style),
            Paragraph("Vulnérable aux erreurs de syntaxe Python", card_text_style),
            Paragraph("<b>Tolérant à 100%</b> grâce au <i>Smart Match</i> contextuel de secours", card_text_style)
        ],
        [
            Paragraph("<b>Temps de réponse</b>", meta_label_style),
            Paragraph("10 itérations lentes et répétitives", card_text_style),
            Paragraph("<b>Action immédiate</b> en une fraction de seconde avec retour visuel clair", card_text_style)
        ],
        [
            Paragraph("<b>Gestion intention</b>", meta_label_style),
            Paragraph("Exécution confuse même sur un simple 'salut'", card_text_style),
            Paragraph("<b>Filtrage intelligent :</b> Discussion polie vs Mode Développeur actif", card_text_style)
        ]
    ]
    comp_table = Table(comparaison_data, colWidths=[95, 205, 211])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(comp_table)

    # ── 3. L'ARSENAL TECHNIQUE & LES SUPER-POUVOIRS ───────────────────────────
    story.append(Spacer(1, 4))
    story.append(Paragraph("3. L'Arsenal Technique & Fonctionnalités Déployées", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=c_primary, spaceBefore=1, spaceAfter=4))

    features_data = [
        [
            Paragraph("<b>🔄 Auto-Correction Autonome (Self-Healing Loop)</b><br/>"
                      "En cas d'erreur de commande Bash ou de code Python (Traceback, SyntaxError), GemmAI capture l'erreur "
                      "et réinterroge le modèle en circuit fermé pour réécrire et re-tester le fichier corrigé sans intervention humaine.", card_text_style),
            Paragraph("<b>⏪ Restauration Instantanée (/undo)</b><br/>"
                      "Un point de contrôle Git automatique est créé avant chaque opération. L'utilisateur peut taper <code>/undo</code> "
                      "à tout instant pour réinitialiser le projet à son état antérieur exact (garantie zéro perte de travail).", card_text_style)
        ],
        [
            Paragraph("<b>📊 Visualisation Diff Couleur (Style Git)</b><br/>"
                      "Lors de toute réécriture d'un fichier existant, GemmAI affiche un diff unifié haute lisibilité : "
                      "<font color='#059669'>lignes ajoutées en vert (+)</font>, <font color='#DC2626'>lignes supprimées en rouge (-)</font>.", card_text_style),
            Paragraph("<b>🧠 Analyse & Injection Contextuelle de Code</b><br/>"
                      "Quand l'utilisateur mentionne un fichier (ex: <i>analyse script.py</i>), l'agent lit automatiquement le fichier "
                      "sur le disque et injecte son contenu dans le prompt pour une compréhension immédiate du problème.", card_text_style)
        ],
        [
            Paragraph("<b>🔒 Triple Vérification d'Écriture</b><br/>"
                      "Chaque fichier écrit est audité : 1) Présence réelle sur disque, 2) Taille non nulle, 3) Relecture et comparaison exacte "
                      "du contenu, 4) Compilation syntaxique via <code>python3 -m py_compile</code>.", card_text_style),
            Paragraph("<b>🔀 Commande /model Dynamique</b><br/>"
                      "Possibilité d'interroger Ollama et de basculer à chaud entre <code>gemma:2b</code>, <code>gemma2:2b</code> ou d'autres modèles "
                      "sans jamais redémarrer ni modifier le script.", card_text_style)
        ]
    ]
    feat_table = Table(features_data, colWidths=[255, 256])
    feat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(feat_table)

    # ── 4. DISTRIBUTION ET PORTABILITÉ SOLO ───────────────────────────────────
    story.append(Spacer(1, 4))
    story.append(Paragraph("4. Stratégie de Déploiement & Portabilité Solo (Zéro Dépendance)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=c_primary, spaceBefore=1, spaceAfter=4))
    
    story.append(Paragraph(
        "• <b>L'installateur One-Line (Script <code>install.sh</code>) :</b> Permet à n'importe quel développeur sous Linux/macOS "
        "d'installer l'agent en une commande unique (<code>curl -fsSL https://.../install.sh | bash</code>). Le script configure "
        "l'environnement, vérifie le moteur IA, télécharge le modèle Gemma et crée l'exécutable global <code>/usr/local/bin/gemmai</code>.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>L'Application Standalone Solo (Format GGUF + llama-cpp) :</b> Afin de s'affranchir totalement d'Ollama pour l'environnement Kaggle, "
        "l'agent peut intégrer le moteur C++ léger <code>llama-cpp-python</code> avec les poids quantifiés en 4-bit dans un fichier unique (.gguf). "
        "Un binaire compilé via <b>PyInstaller</b> permet d'exécuter GemmAI en solo absolu sans nécessiter l'installation de Python ni de serveur tiers.",
        bullet_style
    ))

    # ── 5. FEUILLE DE ROUTE STRATÉGIQUE KAGGLE ($100K) ────────────────────────
    story.append(Spacer(1, 4))
    story.append(Paragraph("5. Objectifs Visés & Feuille de Route Stratégique (Échéance Nov 2026)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=c_primary, spaceBefore=1, spaceAfter=4))

    roadmap_data = [
        [
            Paragraph("<b>Phase</b>", meta_label_style),
            Paragraph("<b>Objectifs & Livrables Techniques</b>", meta_label_style),
            Paragraph("<b>Statut</b>", meta_label_style)
        ],
        [
            Paragraph("<b>Phase 1 : Cœur Agent</b>", meta_label_style),
            Paragraph("Architecture interactive directe type Gemini CLI, triple vérification de fichier, streaming ANSI, commande globale.", card_text_style),
            Paragraph("<font color='#059669'><b>✔ TERMINÉ</b></font>", card_text_style)
        ],
        [
            Paragraph("<b>Phase 2 : Robustesse & UX</b>", meta_label_style),
            Paragraph("Boucle d'auto-correction (Self-Healing), Rollback Git instantané (/undo), diffs visuels unifiés, filtrage conversationnel.", card_text_style),
            Paragraph("<font color='#059669'><b>✔ TERMINÉ</b></font>", card_text_style)
        ],
        [
            Paragraph("<b>Phase 3 : Packaging Solo</b>", meta_label_style),
            Paragraph("Script d'installation automatisé <code>install.sh</code>, intégration du runtime local autonome pour exécution hors ligne.", card_text_style),
            Paragraph("<font color='#D97706'><b>EN COURS</b></font>", card_text_style)
        ],
        [
            Paragraph("<b>Phase 4 : Benchmarking SWE</b>", meta_label_style),
            Paragraph("Évaluation sur des jeux de test Kaggle (résolution de bugs logiciels réels sur dépôts Git) et optimisation des métriques de succès.", card_text_style),
            Paragraph("<font color='#64748B'><b>PLANIFIÉ</b></font>", card_text_style)
        ],
        [
            Paragraph("<b>Phase 5 : Fine-Tuning QLoRA</b>", meta_label_style),
            Paragraph("Adaptation fine des poids de Gemma 2B/7B sur des traces de raisonnement développeur pour maximiser l'autonomie sur cas extrêmes.", card_text_style),
            Paragraph("<font color='#64748B'><b>PLANIFIÉ</b></font>", card_text_style)
        ],
        [
            Paragraph("<b>Phase 6 : Soumission Finale</b>", meta_label_style),
            Paragraph("Dépôt officiel du Notebook Kaggle et de la documentation complète pour le grand prix de <b>100 000 $ USD</b>.", card_text_style),
            Paragraph("<font color='#1E3A8A'><b>OBJECTIF FINAL (25 Nov 2026)</b></font>", card_text_style)
        ]
    ]
    rm_table = Table(roadmap_data, colWidths=[115, 296, 100])
    rm_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(rm_table)

    # ── SIGNATURE ─────────────────────────────────────────────────────────────
    story.append(Spacer(1, 8))
    sign_text = (
        "<b>Document rédigé par :</b> Max_Adis • Lead Technique & Ingénieur Développeur<br/>"
        "<i>Projet GemmAI — Tous droits réservés • Compétition Kaggle 2026</i>"
    )
    story.append(Paragraph(sign_text, ParagraphStyle(
        'SignStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_gray,
        alignment=1
    )))

    # Génération du document PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF généré avec succès : {filename}")

if __name__ == "__main__":
    build_pdf()
