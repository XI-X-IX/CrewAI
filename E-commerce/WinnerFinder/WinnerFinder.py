"""
╔══════════════════════════════════════════════════════════╗
║       CREW 3 — PRODUCT WINNER FINDER 🏆                  ║
║       Trouve les produits tendance E-commerce            ║
║       CrewAI + Ollama + Recherche Web                    ║
╚══════════════════════════════════════════════════════════╝

INSTALLATION :
    pip install crewai crewai-tools langchain-community requests beautifulsoup4 python-dotenv

PRÉREQUIS :
    ollama pull qwen2.5-coder:7b || mistral

UTILISATION :
    python WinnerFinder.py
"""

from dotenv import load_dotenv
load_dotenv()
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from langchain_community.llms import Ollama
import os
import json
from datetime import datetime

# ─────────────────────────────────────────
# 1. CONFIGURATION
# ─────────────────────────────────────────

# Option A : Avec Serper (recherche Google gratuite - 2500 recherches/mois)
# Créez un compte GRATUIT sur https://serper.dev pour obtenir votre clé API
# Puis décommentez et remplissez la ligne suivante :
# os.environ["SERPER_API_KEY"] = "VOTRE_CLE_SERPER_ICI"

# Option B : Sans clé API (analyse basée sur les données que vous fournissez)
UTILISER_SERPER = os.environ.get("SERPER_API_KEY") is not None

llm = Ollama(
    model="ollama/mistral",        # Changez par "mistral" si vous préférez
    base_url="http://localhost:11434",
    temperature=0.8,
    timeout=1200,       				# ← Ajoutez cette ligne (1200 secondes = 20 min)
    num_ctx=2048        				# ← Réduit le contexte = plus rapide
)


# Outils de recherche web
search_tool = SerperDevTool() if UTILISER_SERPER else None
scrape_tool = ScrapeWebsiteTool() if UTILISER_SERPER else None

def get_tools():
    tools = []
    if search_tool:
        tools.append(search_tool)
    if scrape_tool:
        tools.append(scrape_tool)
    return tools

# ─────────────────────────────────────────
# 2. DÉFINITION DES AGENTS
# ─────────────────────────────────────────

chasseur_tendances = Agent(
    role="Chasseur de Tendances E-commerce",
    goal="Identifier les produits qui explosent en vente en ce moment sur le marché",
    backstory="""Tu es un expert en dropshipping et e-commerce avec 10 ans d'expérience.
    Tu sais repérer les produits winners avant tout le monde en analysant :
    TikTok trends, Amazon Best Sellers, AliExpress tendances, Google Trends.
    Tu cherches des produits avec forte demande et faible concurrence.""",
    llm=llm,
    tools=get_tools(),
    verbose=True,
    allow_delegation=False
)

analyste_marche = Agent(
    role="Analyste de Marché",
    goal="Analyser la viabilité commerciale et le potentiel de profit de chaque produit",
    backstory="""Tu es analyste financier spécialisé en e-commerce.
    Tu évalues chaque produit selon : marge bénéficiaire, volume de marché,
    saisonnalité, niveau de concurrence, facilité de sourcing.
    Tu notes chaque produit sur 10 avec une justification détaillée.""",
    llm=llm,
    tools=get_tools(),
    verbose=True,
    allow_delegation=False
)

expert_sourcing = Agent(
    role="Expert Sourcing et Fournisseurs",
    goal="Trouver les meilleurs fournisseurs et estimer les coûts réels",
    backstory="""Tu es expert en sourcing sur AliExpress, Alibaba et CJdropshipping.
    Tu connais les prix fournisseurs, les délais de livraison, la qualité des produits.
    Tu calcules les marges réelles en tenant compte de tous les coûts :
    produit + livraison + publicité + frais de plateforme.""",
    llm=llm,
    tools=get_tools(),
    verbose=True,
    allow_delegation=False
)

stratege_lancement = Agent(
    role="Stratège Lancement Produit",
    goal="Créer une stratégie complète pour lancer et vendre le produit winner",
    backstory="""Tu es expert en lancement de produits e-commerce.
    Tu maîtrises les publicités Facebook/TikTok, le marketing d'influence,
    et les stratégies de contenu organique. Tu crées des plans d'action
    concrets avec budget, timeline et KPIs pour réussir le lancement.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# ─────────────────────────────────────────
# 3. DÉFINITION DES TÂCHES
# ─────────────────────────────────────────

def creer_taches_winner(niche: str, budget_lancement: str, plateforme: str):

    date_actuelle = datetime.now().strftime("%B %Y")

    tache_tendances = Task(
        description=f"""
        Trouve les 5 meilleurs produits winners potentiels en {date_actuelle}.
        
        NICHE CIBLÉE : {niche} (ou toutes niches si "general")
        PLATEFORME DE VENTE : {plateforme}
        
        Critères d'un produit winner :
        ✅ Résout un problème réel ou crée une forte émotion
        ✅ Pas encore saturé sur le marché
        ✅ Prix de vente possible entre 20€ et 80€
        ✅ Facile à expliquer en vidéo courte (TikTok/Reels)
        ✅ Effet "wow" ou utilité évidente
        ✅ Tendance en hausse sur les réseaux sociaux
        
        Pour chaque produit, fournis :
        - Nom du produit
        - Description en 2 lignes
        - Pourquoi c'est un winner potentiel
        - Où tu as détecté la tendance (TikTok, Amazon, etc.)
        - Score de tendance estimé /10
        """,
        agent=chasseur_tendances,
        expected_output="Liste de 5 produits winners potentiels avec analyse de tendance"
    )

    tache_analyse = Task(
        description=f"""
        Analyse en profondeur les 5 produits identifiés et sélectionne le TOP 3.
        
        Pour chaque produit, évalue :
        
        📊 SCORE DE MARCHÉ (sur 10) selon :
        - Taille du marché potentiel
        - Niveau de concurrence actuel (faible/moyen/élevé)
        - Saisonnalité (produit evergreen ou saisonnier ?)
        - Tendance (montante / plateau / descendante)
        
        💰 POTENTIEL DE PROFIT :
        - Prix de vente estimé
        - Marge brute estimée (%)
        - Volume de ventes mensuel possible
        - Chiffre d'affaires mensuel potentiel
        
        ⚠️ RISQUES :
        - Problèmes potentiels (retours, SAV, saisonnalité)
        - Concurrents déjà établis
        
        Classe les 3 meilleurs et explique pourquoi.
        """,
        agent=analyste_marche,
        expected_output="Analyse détaillée des 5 produits avec classement TOP 3 justifié",
        context=[tache_tendances]
    )

    tache_sourcing = Task(
        description=f"""
        Pour le produit #1 classé (le meilleur winner), trouve le sourcing complet.
        
        BUDGET DISPONIBLE : {budget_lancement}
        
        Fournis :
        
        🏭 FOURNISSEURS RECOMMANDÉS :
        - 3 fournisseurs sur AliExpress/Alibaba avec liens de recherche
        - Prix unitaire estimé fournisseur
        - Délai de livraison vers la France/Europe
        - MOQ (quantité minimale de commande)
        - Note qualité estimée
        
        💸 CALCUL DE MARGE RÉELLE :
        - Prix fournisseur : X€
        - Frais de livraison : X€
        - Frais plateforme (Shopify/Amazon) : X€
        - Budget pub estimé par vente : X€
        - COÛT TOTAL PAR VENTE : X€
        - PRIX DE VENTE RECOMMANDÉ : X€
        - MARGE NETTE : X€ (X%)
        
        📦 ALTERNATIVES :
        - Agent dropshipping recommandé (CJdropshipping, Zendrop...)
        - Possibilité de faire du print-on-demand ?
        """,
        agent=expert_sourcing,
        expected_output="Plan de sourcing complet avec calcul de marge détaillé pour le produit #1",
        context=[tache_analyse]
    )

    tache_strategie = Task(
        description=f"""
        Crée un plan de lancement complet pour le produit winner #1.
        
        BUDGET : {budget_lancement}
        PLATEFORME : {plateforme}
        
        Fournis :

        🎯 POSITIONNEMENT :
        - Nom de boutique/marque suggéré
        - Message marketing principal (1 phrase)
        - Cible client précise (persona)
        
        📱 STRATÉGIE CONTENU ORGANIQUE (gratuit) :
        - 5 idées de vidéos TikTok/Reels
        - Script du 1er TikTok (30 secondes)
        - Stratégie hashtags
        - Fréquence de publication recommandée
        
        💰 STRATÉGIE PUBLICITAIRE (si budget) :
        - Budget pub recommandé pour tester
        - Type de publicité (Facebook Ads, TikTok Ads, Google)
        - Audience cible pour les pubs
        - KPIs à surveiller (ROAS, CPC, CTR cibles)
        
        📅 PLAN D'ACTION SUR 30 JOURS :
        - Semaine 1 : Actions à faire
        - Semaine 2 : Actions à faire
        - Semaine 3 : Actions à faire
        - Semaine 4 : Actions à faire
        
        🎯 OBJECTIFS RÉALISTES :
        - Mois 1 : X ventes
        - Mois 3 : X€ de CA
        - Mois 6 : X€ de CA
        """,
        agent=stratege_lancement,
        expected_output="Plan de lancement complet sur 30 jours avec stratégie marketing détaillée",
        context=[tache_sourcing]
    )

    return [tache_tendances, tache_analyse, tache_sourcing, tache_strategie]


# ─────────────────────────────────────────
# 4. LANCEMENT DU CREW
# ─────────────────────────────────────────

def lancer_winner_finder(niche: str, budget: str, plateforme: str):
    print(f"\n{'='*60}")
    print(f"🏆 DÉMARRAGE DU PRODUCT WINNER FINDER")
    print(f"🎯 Niche    : {niche}")
    print(f"💰 Budget   : {budget}")
    print(f"🛒 Plateforme: {plateforme}")
    if not UTILISER_SERPER:
        print(f"⚠️  Mode hors-ligne (pas de clé Serper)")
        print(f"   → Ajoutez SERPER_API_KEY pour la recherche web réelle")
    print(f"{'='*60}\n")

    taches = creer_taches_winner(niche, budget, plateforme)

    crew = Crew(
        agents=[chasseur_tendances, analyste_marche, expert_sourcing, stratege_lancement],
        tasks=taches,
        process=Process.sequential,
        verbose=True
    )

    resultat = crew.kickoff()

    # Sauvegarde avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    nom_fichier = f"winner_{niche[:20].replace(' ', '_')}_{timestamp}.txt"
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(f"NICHE: {niche}\n")
        f.write(f"BUDGET: {budget}\n")
        f.write(f"PLATEFORME: {plateforme}\n")
        f.write(f"DATE: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("="*60 + "\n\n")
        f.write(str(resultat))

    print(f"\n✅ Résultat sauvegardé dans : {nom_fichier}")
    return resultat


# ─────────────────────────────────────────
# 5. LANCEMENT
# ─────────────────────────────────────────

if __name__ == "__main__":

    # ✏️ MODIFIEZ CES 3 PARAMÈTRES

    # Niche (exemples: "maison et décoration", "sport et fitness",
    #                   "animaux", "beauté", "bébé", "général")
    NICHE = "general"

    # Votre budget pour lancer (pub + stock)
    BUDGET = "500chf"

    # Votre plateforme de vente
    PLATEFORME = "Shopify + TikTok Shop"  # ou "Amazon FBA", "Etsy", "Leboncoin"

    resultat = lancer_winner_finder(NICHE, BUDGET, PLATEFORME)

    print("\n" + "="*60)
    print("🏆 RÉSULTAT FINAL — VOTRE PRODUIT WINNER :")
    print("="*60)
    print(resultat)