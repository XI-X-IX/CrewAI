"""
╔══════════════════════════════════════════════════════════╗
║          CREW 1 — USINE À CONTENU                        ║
║          CrewAI + Ollama (100% local, 100% gratuit)      ║
╚══════════════════════════════════════════════════════════╝

INSTALLATION :
    pip install crewai crewai-tools langchain-community

PRÉREQUIS :
    ollama run qwen2.5-coder:7b   (ou mistral)

UTILISATION :
    python crew1_contenu.py
"""

from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama

# ─────────────────────────────────────────
# 1. CONFIGURATION DU MODÈLE LOCAL
# ─────────────────────────────────────────
llm = Ollama(
    model="ollama/qwen2.5-coder:7b",        # Changez par "mistral" si vous préférez
    base_url="http://localhost:11434",
    temperature=0.7         # 0 = précis, 1 = créatif
)

# ─────────────────────────────────────────
# 2. DÉFINITION DES AGENTS
# ─────────────────────────────────────────

chercheur = Agent(
    role="Chercheur de Contenu",
    goal="Trouver les informations les plus pertinentes et récentes sur le sujet donné",
    backstory="""Tu es un expert en recherche d'information. 
    Tu sais identifier les points clés, les tendances et les angles 
    les plus intéressants pour captiver un public en ligne.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

redacteur = Agent(
    role="Rédacteur de Blog",
    goal="Rédiger des articles de blog engageants, informatifs et optimisés",
    backstory="""Tu es un rédacteur web professionnel avec 10 ans d'expérience.
    Tu écris des articles clairs, structurés avec des titres H2/H3,
    une introduction accrocheuse et une conclusion avec appel à l'action.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

social_media = Agent(
    role="Social Media Manager",
    goal="Créer des posts percutants pour Instagram, LinkedIn et Twitter/X",
    backstory="""Tu es spécialiste des réseaux sociaux. Tu sais adapter 
    le même contenu à chaque plateforme avec le bon ton, les bons hashtags
    et le bon format pour maximiser l'engagement.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

seo_expert = Agent(
    role="Expert SEO",
    goal="Optimiser le contenu pour le référencement naturel (SEO)",
    backstory="""Tu es expert en SEO avec une connaissance approfondie 
    des algorithmes Google. Tu optimises les titres, méta-descriptions,
    mots-clés et la structure des contenus pour maximiser la visibilité.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# ─────────────────────────────────────────
# 3. DÉFINITION DES TÂCHES
# ─────────────────────────────────────────

def creer_taches(sujet: str, public_cible: str, langue: str = "français"):

    tache_recherche = Task(
        description=f"""
        Recherche et analyse le sujet suivant : "{sujet}"
        Public cible : {public_cible}
        
        Fournis :
        1. Les 5 points clés les plus importants sur ce sujet
        2. Les tendances actuelles
        3. Les questions que se pose ce public cible
        4. 3 angles originaux pour aborder ce sujet
        5. Des données/statistiques pertinentes si possible
        """,
        agent=chercheur,
        expected_output="Un rapport de recherche structuré avec points clés, tendances et angles d'approche"
    )

    tache_redaction = Task(
        description=f"""
        En te basant sur la recherche fournie, rédige un article de blog complet en {langue}.
        
        Sujet : "{sujet}"
        Public cible : {public_cible}
        
        Structure obligatoire :
        - Titre accrocheur (avec le mot-clé principal)
        - Introduction (150 mots) : hook + problème + promesse
        - 3 à 5 sections avec titres H2
        - Sous-sections H3 si nécessaire
        - Exemples concrets et pratiques
        - Conclusion avec appel à l'action
        - Longueur : 800 à 1200 mots
        """,
        agent=redacteur,
        expected_output="Un article de blog complet et structuré en markdown",
        context=[tache_recherche]
    )

    tache_social = Task(
        description=f"""
        À partir de l'article de blog rédigé, crée des posts pour les réseaux sociaux en {langue}.
        
        Crée :
        
        📸 INSTAGRAM (1 post)
        - Texte engageant de 150 mots max
        - 15 hashtags pertinents
        - Émojis appropriés
        - Appel à l'action
        
        💼 LINKEDIN (1 post)
        - Texte professionnel de 200 mots
        - Ton expert et inspirant
        - 5 hashtags professionnels
        - Question pour engager la communauté
        
        🐦 TWITTER/X (3 tweets)
        - Tweet principal (280 caractères max)
        - 2 tweets de suivi pour un thread
        - Hashtags pertinents
        """,
        agent=social_media,
        expected_output="Posts formatés et prêts à publier pour Instagram, LinkedIn et Twitter/X",
        context=[tache_redaction]
    )

    tache_seo = Task(
        description=f"""
        Optimise le contenu créé pour le SEO en {langue}.
        
        Fournis :
        1. Titre SEO optimisé (60 caractères max)
        2. Méta-description (155 caractères max)
        3. Liste de 10 mots-clés principaux et secondaires
        4. Suggestions de liens internes/externes
        5. Balises alt pour 3 images suggérées
        6. Score de lisibilité et suggestions d'amélioration
        7. Slug URL recommandé
        """,
        agent=seo_expert,
        expected_output="Rapport SEO complet avec tous les éléments d'optimisation",
        context=[tache_redaction]
    )

    return [tache_recherche, tache_redaction, tache_social, tache_seo]


# ─────────────────────────────────────────
# 4. LANCEMENT DU CREW
# ─────────────────────────────────────────

def lancer_crew(sujet: str, public_cible: str, langue: str = "français"):
    print(f"\n{'='*60}")
    print(f"🚀 DÉMARRAGE DE L'USINE À CONTENU")
    print(f"📝 Sujet       : {sujet}")
    print(f"👥 Public      : {public_cible}")
    print(f"🌍 Langue      : {langue}")
    print(f"{'='*60}\n")

    taches = creer_taches(sujet, public_cible, langue)

    crew = Crew(
        agents=[chercheur, redacteur, social_media, seo_expert],
        tasks=taches,
        process=Process.sequential,  # Les agents travaillent dans l'ordre
        verbose=True
    )

    resultat = crew.kickoff()

    # Sauvegarde automatique du résultat
    nom_fichier = f"contenu_{sujet[:30].replace(' ', '_')}.txt"
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(f"SUJET: {sujet}\n")
        f.write(f"PUBLIC: {public_cible}\n")
        f.write("="*60 + "\n\n")
        f.write(str(resultat))

    print(f"\n✅ Contenu sauvegardé dans : {nom_fichier}")
    return resultat


# ─────────────────────────────────────────
# 5. EXEMPLES D'UTILISATION
# ─────────────────────────────────────────

if __name__ == "__main__":

    # MODIFIEZ CES VALEURS SELON VOS BESOINS
    SUJET = "Comment choisir ses chaussures de running en 2024"
    PUBLIC_CIBLE = "Sportifs débutants entre 25 et 45 ans"
    LANGUE = "français"

    # Lancer le crew
    resultat = lancer_crew(SUJET, PUBLIC_CIBLE, LANGUE)
    print("\n" + "="*60)
    print("📦 RÉSULTAT FINAL :")
    print("="*60)
    print(resultat)