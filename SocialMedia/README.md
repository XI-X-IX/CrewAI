# 🤖 Crew 1 — Usine à Contenu
> CrewAI + Ollama | 100% local | 100% gratuit

---

## Installation (à faire une seule fois)

```bash
# 1. Installer Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Télécharger le modèle (choisissez un seul)
ollama pull mistral           # Meilleur pour le français
ollama pull qwen2.5-coder:7b  # Meilleur pour le code

# 3. Installer les dépendances Python
pip install crewai crewai-tools langchain-community
```

---

## Utilisation

```bash
# Lancer le crew
python crew1_contenu.py
```

---

## Personnaliser votre contenu

Ouvrez `crew1_contenu.py` et modifiez ces 3 lignes tout en bas :

```python
SUJET        = "Votre sujet ici"
PUBLIC_CIBLE = "Votre audience cible"
LANGUE       = "français"
```

### Exemples de sujets :
- `"Les meilleures pratiques SEO en 2024"`
- `"Comment créer une boutique en ligne rentable"`
- `"Guide débutant pour le marketing Instagram"`

---

## Résultat généré

Le crew crée automatiquement un fichier `.txt` avec :
- ✅ Article de blog complet (800-1200 mots)
- ✅ Post Instagram avec hashtags
- ✅ Post LinkedIn professionnel
- ✅ Thread Twitter/X (3 tweets)
- ✅ Rapport SEO complet (titre, méta, mots-clés...)

---

## Les 4 agents

| Agent | Rôle |
|---|---|
| 🔍 Chercheur | Analyse le sujet et trouve les angles |
| ✍️ Rédacteur | Écrit l'article de blog structuré |
| 📱 Social Media | Adapte pour Instagram, LinkedIn, Twitter |
| 🎯 SEO Expert | Optimise pour Google |

---

## Temps estimé pour mon iMac 2013, 32GB RAM

- Avec `mistral` : ~5 à 10 minutes par génération
- Résultat : contenu complet prêt à publier

---

## 🔧 Dépannage

**Erreur "Connection refused"** → Ollama n'est pas lancé
```bash
ollama serve
```

**Erreur "Model not found"** → Le modèle n'est pas téléchargé
```bash
ollama pull mistral
```

**Trop lent** → Réduire la longueur demandée dans les tâches