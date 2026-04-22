"""
╔══════════════════════════════════════════════════════════╗
║          CREW 2 — ASSISTANT E-COMMERCE                   ║
║          CrewAI + Ollama (100% local, 100% gratuit)      ║
╚══════════════════════════════════════════════════════════╝

INSTALLATION :
    pip install crewai crewai-tools langchain-community

PRÉREQUIS :
    ollama run mistral   (ou ollama/qwen2.5-coder:7b)

UTILISATION :
    python ProductAssistant.py
"""

from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama

# ─────────────────────────────────────────
# 1. CONFIGURATION DU MODÈLE LOCAL
# ─────────────────────────────────────────
llm = Ollama(
    model="ollama/qwen2.5-coder:7b",        # Changez par "mistral" si vous préférez
    base_url="http://localhost:11434",
    temperature=0.7
)

# ─────────────────────────────────────────
# 2. DÉFINITION DES AGENTS
# ─────────────────────────────────────────

analyste_produit = Agent(
    role="Analyste Produit E-commerce",
    goal="Analyser les fiches produits et identifier les points faibles à améliorer",
    backstory="""Tu es un expert en e-commerce avec 10 ans d'expérience.
    Tu sais identifier pourquoi une fiche produit ne convertit pas :
    description trop courte, manque de bénéfices, mauvais titre, etc.
    Tu fournis une analyse détaillée et actionnable.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

redacteur_produit = Agent(
    role="Rédacteur Fiche Produit",
    goal="Rédiger des descriptions produits qui convainquent et font acheter",
    backstory="""Tu es copywriter spécialisé en e-commerce.
    Tu maîtrises les techniques de copywriting : AIDA, bénéfices vs caractéristiques,
    preuves sociales, urgence. Tu rédiges des fiches qui augmentent le taux de conversion.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

gestionnaire_prix = Agent(
    role="Gestionnaire de Prix et Stratégie",
    goal="Analyser le positionnement prix et suggérer des stratégies pour maximiser les ventes",
    backstory="""Tu es expert en pricing e-commerce. Tu analyses la concurrence,
    les marges, et suggères des stratégies de prix : promotions, bundles, 
    prix psychologiques, upsell/cross-sell pour augmenter le panier moyen.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

gestionnaire_avis = Agent(
    role="Gestionnaire Avis et Relation Client",
    goal="Rédiger des réponses professionnelles aux avis clients et améliorer la réputation",
    backstory="""Tu es expert en gestion de la réputation en ligne.
    Tu sais répondre aux avis négatifs avec diplomatie, remercier les avis positifs,
    et transformer les clients mécontents en ambassadeurs de la marque.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# ─────────────────────────────────────────
# 3. DÉFINITION DES TÂCHES
# ─────────────────────────────────────────

def creer_taches_ecommerce(
    nom_produit: str,
    description_actuelle: str,
    prix: str,
    categorie: str,
    avis_clients: list,
    concurrents: list = None
):
    concurrents_str = "\n".join(concurrents) if concurrents else "Non fournis"
    avis_str = "\n".join([f"- {avis}" for avis in avis_clients])

    tache_analyse = Task(
        description=f"""
        Analyse cette fiche produit e-commerce et identifie tous les points à améliorer.

        PRODUIT : {nom_produit}
        CATÉGORIE : {categorie}
        PRIX ACTUEL : {prix}
        
        DESCRIPTION ACTUELLE :
        {description_actuelle}
        
        CONCURRENTS :
        {concurrents_str}

        Fournis :
        1. Score de la fiche actuelle sur 10 (avec justification)
        2. Liste des 5 problèmes principaux
        3. Ce que font mieux les concurrents
        4. Les bénéfices manquants à mettre en avant
        5. Recommandations prioritaires
        """,
        agent=analyste_produit,
        expected_output="Rapport d'analyse détaillé avec score, problèmes identifiés et recommandations"
    )

    tache_redaction = Task(
        description=f"""
        En te basant sur l'analyse, réécris complètement la fiche produit pour maximiser les conversions.

        PRODUIT : {nom_produit}
        PRIX : {prix}
        CATÉGORIE : {categorie}

        Structure obligatoire :
        
        📌 TITRE PRODUIT (60 caractères max, accrocheur avec mot-clé)
        
        🎯 ACCROCHE (1 phrase qui résume le bénéfice principal)
        
        📝 DESCRIPTION COURTE (150 mots)
        - Bénéfices principaux (pas juste les caractéristiques)
        - Pour qui c'est fait
        - Ce qui le différencie
        
        📋 DESCRIPTION LONGUE (400 mots)
        - Histoire/contexte du produit
        - Bénéfices détaillés avec preuves
        - Cas d'utilisation concrets
        - Réponses aux objections courantes
        
        ✅ BULLET POINTS (5 à 7 points forts)
        
        ❓ FAQ PRODUIT (3 questions/réponses)
        
        🛒 APPEL À L'ACTION
        """,
        agent=redacteur_produit,
        expected_output="Fiche produit complète et optimisée prête à copier-coller",
        context=[tache_analyse]
    )

    tache_prix = Task(
        description=f"""
        Analyse le positionnement prix et propose une stratégie complète.

        PRODUIT : {nom_produit}
        PRIX ACTUEL : {prix}
        CATÉGORIE : {categorie}
        CONCURRENTS : {concurrents_str}

        Fournis :
        1. Analyse du prix actuel (trop cher / trop bas / correct ?)
        2. Fourchette de prix recommandée avec justification
        3. Stratégie de prix psychologique (ex: 29,99€ au lieu de 30€)
        4. Ideas de bundles et offres groupées
        5. Stratégie de promotions (quand, combien, comment)
        6. Suggestions d'upsell et cross-sell
        7. Programme de fidélité possible
        """,
        agent=gestionnaire_prix,
        expected_output="Stratégie de pricing complète avec recommandations actionnables",
        context=[tache_analyse]
    )

    tache_avis = Task(
        description=f"""
        Rédige des réponses professionnelles pour chaque avis client.

        PRODUIT : {nom_produit}

        AVIS CLIENTS :
        {avis_str}

        Pour chaque avis, fournis :
        - La réponse complète (ton professionnel, empathique, constructif)
        - Si avis négatif : excuse + solution concrète + invitation à recontacter
        - Si avis positif : remerciement personnalisé + invitation à revenir
        - Maximum 150 mots par réponse
        
        Aussi fournis :
        - 3 façons d'encourager plus d'avis positifs
        - Template d'email post-achat pour demander un avis
        """,
        agent=gestionnaire_avis,
        expected_output="Réponses aux avis + stratégie pour générer plus d'avis positifs",
        context=[tache_redaction]
    )

    return [tache_analyse, tache_redaction, tache_prix, tache_avis]


# ─────────────────────────────────────────
# 4. LANCEMENT DU CREW
# ─────────────────────────────────────────

def lancer_crew_ecommerce(produit_data: dict):
    print(f"\n{'='*60}")
    print(f"🛍️  DÉMARRAGE DE L'ASSISTANT E-COMMERCE")
    print(f"📦 Produit : {produit_data['nom_produit']}")
    print(f"💰 Prix    : {produit_data['prix']}")
    print(f"{'='*60}\n")

    taches = creer_taches_ecommerce(**produit_data)

    crew = Crew(
        agents=[analyste_produit, redacteur_produit, gestionnaire_prix, gestionnaire_avis],
        tasks=taches,
        process=Process.sequential,
        verbose=True
    )

    resultat = crew.kickoff()

    # Sauvegarde automatique
    nom_fichier = f"ecommerce_{produit_data['nom_produit'][:30].replace(' ', '_')}.txt"
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(f"PRODUIT: {produit_data['nom_produit']}\n")
        f.write(f"PRIX: {produit_data['prix']}\n")
        f.write("="*60 + "\n\n")
        f.write(str(resultat))

    print(f"\n✅ Résultat sauvegardé dans : {nom_fichier}")
    return resultat


# ─────────────────────────────────────────
# 5. EXEMPLES D'UTILISATION
# ─────────────────────────────────────────

if __name__ == "__main__":

    # ✏️ MODIFIEZ CES INFORMATIONS AVEC VOTRE PRODUIT
    mon_produit = {
        "nom_produit": "Tee shirt",
        "categorie": "Vêtements / Mode",
        "prix": "29,99€",

        # Votre description actuelle (même mauvaise, le crew va l'améliorer)
        "description_actuelle": """
            Tee shirt en coton 100%.
            Manches courtes.
            Disponible en blanc, noir et gris.
            Matière : coton 100%.
        """,

        # Listez vos concurrents et leurs prix (optionnel)
        "concurrents": [
            "Decathlon Quechua 30L - 35€",
            "The North Face Surge - 120€",
            "Osprey Stratos 24 - 160€"
        ],

        # Collez ici de vrais avis de vos clients
        "avis_clients": [
            "⭐⭐⭐⭐⭐ Excellent sac, très solide et vraiment imperméable !",
            "⭐⭐ La fermeture éclair a lâché après 2 mois, déçu du rapport qualité/prix",
            "⭐⭐⭐⭐ Bon produit mais la livraison a pris 2 semaines, un peu long",
            "⭐⭐⭐⭐⭐ Parfait pour ma randonnée en Écosse, pas une goutte d'eau !"
        ]
    }

    resultat = lancer_crew_ecommerce(mon_produit)
    print("\n" + "="*60)
    print("📦 RÉSULTAT FINAL :")
    print("="*60)
    print(resultat)