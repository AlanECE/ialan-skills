# Anatomie d'un Skill Pro

Un skill robuste s'organise en 4 piliers. Chaque pilier a un rôle précis.

---

## 1. Le Routeur — `SKILL.md`

C'est le **cerveau** du skill. Le seul fichier obligatoire.

Responsabilités :
- Définir le frontmatter (triggers d'activation)
- Orchestrer le flux de travail (Avant / Pendant / Après)
- Pointer vers les fichiers de référence quand nécessaire
- Rester léger : **< 500 lignes** — idéalement 200-300

Ce qu'il ne contient PAS :
- Documentation technique exhaustive → `references/`
- Code exécutable → `scripts/`
- Templates de sortie complexes → `assets/`

Règle : si tu scrolles plus de 3 écrans pour lire SKILL.md, il est trop long. Déporte.

---

## 2. Le Dossier Référence — `references/`

Contient la **documentation lourde** que l'agent lit uniquement quand le contexte l'exige.

Exemples :
- Spécifications d'API (endpoints, paramètres, réponses)
- Règles métier détaillées (ex: strategy-rules.md)
- Documentation légale ou réglementaire
- Tables de correspondance, codes d'erreur

Pourquoi séparer :
- Économise des tokens (le SKILL.md ne charge pas 2000 lignes d'API docs à chaque appel)
- Permet de mettre à jour la doc sans toucher au routeur
- L'agent ne lit que ce dont il a besoin

Convention de nommage : des noms descriptifs en kebab-case.
```
references/
├── endpoints.md        ← Doc API
├── strategy-rules.md   ← Règles métier
├── error-codes.md      ← Codes d'erreur
└── examples.md         ← Exemples annotés
```

---

## 3. Le Dossier Scripts — `scripts/`

Contient le **code exécutable** que l'agent peut lancer pour des calculs précis.

Quand utiliser des scripts :
- Calculs mathématiques complexes (indicateurs techniques, statistiques)
- Transformations de données (parsing, formatage)
- Automations (appels API en boucle, batch processing)

Pourquoi du code plutôt que du prompt :
- Les LLMs font des erreurs d'arithmétique. Les scripts non.
- Résultats reproductibles et vérifiables.
- Plus rapide qu'un raisonnement étape par étape.

Convention :
```
scripts/
├── calculate.py       ← Calculs principaux
├── validate.sh        ← Vérifications
└── transform.py       ← Transformations de données
```

Chaque script doit :
- Avoir un header avec description et usage
- Accepter des arguments en ligne de commande
- Retourner un code de sortie approprié (0 = OK, 1 = erreur)
- Écrire les erreurs sur stderr

---

## 4. Le Dossier Assets — `assets/`

Contient les **templates, modèles et exemples** que l'agent utilise pour formater ses sorties.

Exemples :
- Templates de rapport (markdown, HTML)
- Modèles de sortie JSON
- Exemples de style ou de ton
- Templates d'email

Pourquoi des assets :
- L'agent reproduit un pattern fourni beaucoup mieux qu'il n'invente un format
- Garantit la cohérence entre les exécutions
- Facilite les modifications (changer le template sans toucher au routeur)

Convention :
```
assets/
├── report-template.md  ← Template de rapport
├── output-schema.json  ← Structure de sortie attendue
└── style-guide.md      ← Guide de style
```

---

## Résumé

```
{skill-name}/
├── SKILL.md              ← Routeur léger — orchestration
├── references/           ← Documentation lourde — lecture à la demande
│   └── *.md
├── scripts/              ← Code exécutable — calculs et automation
│   └── *.py / *.sh
└── assets/               ← Templates et modèles — formatage
    └── *.md / *.html / *.json
```

La règle d'or : **SKILL.md donne les ordres, les dossiers fournissent les outils.**
