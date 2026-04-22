# 🏆 Crew 3 — Product Winner Finder
> Trouve les produits e-commerce tendance | CrewAI + Ollama

---

## 📦 Installation

```bash
pip install crewai crewai-tools langchain-community requests beautifulsoup4
ollama pull mistral
```

---

## 🔑 Activer la recherche web RÉELLE (recommandé)

Sans clé API, le crew analyse depuis sa connaissance du marché.
**Avec Serper**, il fait de vraies recherches Google en temps réel.

1. Créez un compte GRATUIT sur **[serper.dev](https://serper.dev)**
   → 2 500 recherches/mois gratuites
2. Copiez votre clé API
3. Ajoutez-la avant de lancer :

```bash
export SERPER_API_KEY="votre_cle_ici"
python crew3_winner_finder.py
```

---

## 🚀 Utilisation

```bash
python crew3_winner_finder.py
```

---

## ✏️ Personnaliser

Modifiez ces 3 lignes dans le fichier :

```python
NICHE      = "maison et décoration"   # ou "général" pour toutes niches
BUDGET     = "500€"
PLATEFORME = "Shopify + TikTok Shop"
```

### Niches populaires à tester :
- `"maison et décoration"`
- `"sport et fitness"`
- `"animaux de compagnie"`
- `"beauté et soin"`
- `"bébé et enfants"`
- `"gadgets high-tech"`
- `"général"` (toutes niches)

### Plateformes supportées :
- `"Shopify + TikTok Shop"`
- `"Amazon FBA"`
- `"Etsy"`
- `"WooCommerce"`

---

## 📁 Ce que vous obtenez

✅ **5 produits winners potentiels** détectés sur le marché actuel  
✅ **Analyse de viabilité** avec score /10 pour chaque produit  
✅ **TOP 3 classé** avec justification détaillée  
✅ **Plan de sourcing complet** pour le produit #1 :
   - 3 fournisseurs recommandés
   - Calcul de marge réelle (coût → prix vente → bénéfice)  
✅ **Stratégie de lancement sur 30 jours** :
   - Scripts TikTok/Reels
   - Stratégie pub Facebook/TikTok Ads
   - Plan d'action semaine par semaine
   - Objectifs de CA réalistes

---

## ⚙️ Les 4 agents

| Agent | Rôle |
|---|---|
| 🔍 Chasseur de Tendances | Détecte les produits qui montent |
| 📊 Analyste de Marché | Score et classe les produits |
| 🏭 Expert Sourcing | Trouve fournisseurs + calcule les marges |
| 🚀 Stratège Lancement | Plan marketing 30 jours |

---

## 💡 Astuce — Relancer régulièrement

Les tendances changent vite ! Relancez ce crew :
- **1x par semaine** pour rester à jour
- Chaque résultat est sauvegardé avec la date et l'heure

---

## ⏱️ Temps estimé

- Sans Serper : ~10 minutes
- Avec Serper (recherche web réelle) : ~15-20 minutes