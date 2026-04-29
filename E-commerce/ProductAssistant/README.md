#  Crew 2 — Assistant E-commerce
> CrewAI + Ollama | 100% local | 100% gratuit

---

##  Installation (si pas déjà fait)

```bash
pip install crewai crewai-tools langchain-community
ollama pull mistral
```

---

##  Utilisation

```bash
python crew2_ecommerce.py
```

---

##  Personnaliser avec votre produit

Ouvrez `crew2_ecommerce.py` et modifiez le dictionnaire `mon_produit` :

```python
mon_produit = {
    "nom_produit"          : "Nom de votre produit",
    "categorie"            : "Catégorie du produit",
    "prix"                 : "29,99€",
    "description_actuelle" : "Votre description actuelle...",
    "concurrents"          : [
        "Concurrent A - 25€",
        "Concurrent B - 45€",
    ],
    "avis_clients" : [
        " Super produit !",
        " Déçu par la qualité...",
    ]
}
```

---

##  Résultat généré

Le crew crée automatiquement un fichier `.txt` avec :

-  Analyse de votre fiche produit actuelle (score /10)
-  Nouvelle fiche produit complète et optimisée
-  Titre accrocheur + description courte + longue
-  Bullet points + FAQ + appel à l'action
-  Stratégie de prix avec bundles et promotions
-  Réponses professionnelles à chaque avis client
-  Template email pour demander des avis

---

##  Les 4 agents

| Agent | Rôle |
|---|---|
|  Analyste Produit | Évalue et score votre fiche actuelle |
|  Rédacteur Produit | Réécrit la fiche pour convertir |
|  Gestionnaire Prix | Stratégie pricing, bundles, promos |
|  Gestionnaire Avis | Répond aux clients, gère la réputation |

---

##  Astuce — Traiter plusieurs produits

Pour analyser plusieurs produits à la suite, dupliquez le bloc `mon_produit`
et appelez `lancer_crew_ecommerce()` autant de fois que nécessaire :

```python
produit_1 = { "nom_produit": "Produit A", ... }
produit_2 = { "nom_produit": "Produit B", ... }

lancer_crew_ecommerce(produit_1)
lancer_crew_ecommerce(produit_2)
```

---

## ⏱ Temps estimé sur votre iMac 2013

~8 à 15 minutes par produit (4 agents qui travaillent séquentiellement)