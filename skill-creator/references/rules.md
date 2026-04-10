# Les 5 Règles d'Or — Rédaction de Skills

## Règle 1 : Impératif + Raison

Les LLMs ne sont pas là pour recevoir des suggestions. Donne des directives froides à l'impératif.
Mais ajoute toujours le "pourquoi" — les modèles performent mieux quand ils comprennent l'objectif.

❌ Mauvais :
```
Tu pourrais vérifier les positions s'il te plaît ?
```

✅ Bon :
```
Vérifie les positions avant chaque trade, car un doublon fausse le calcul de sizing.
```

La structure : **[Verbe impératif] [quoi faire], [car/pour/afin de] [pourquoi].**

---

## Règle 2 : Négation + Alternative

Biais cognitif des LLMs : interdire un concept sans alternative le garde actif dans la génération.
Dis toujours ce qu'il faut faire À LA PLACE.

❌ Mauvais :
```
N'utilise pas /v2/stocks/ pour la crypto.
```

✅ Bon :
```
N'utilise jamais /v2/stocks/ pour la crypto, utilise /v1beta3/crypto/us/ à la place.
```

La structure : **Ne [jamais/pas] [interdit], [utilise/fais/préfère] [alternative] à la place.**

---

## Règle 3 : Structure Chronologique (Avant / Pendant / Après)

Évite les listes de tirets sans hiérarchie. Structure le flux de travail dans l'ordre temporel.

```markdown
## # Avant l'action
→ Ce qu'il faut lire, vérifier, récupérer.
→ Les pré-conditions.

## # Pendant l'action
→ Les règles strictes d'exécution.
→ Les cas de figure et comment les gérer.

## # Après l'action
→ Le format de sortie exact.
→ Les vérifications finales.
→ La gestion des erreurs.
```

Pourquoi ça marche :
- L'agent sait QUAND appliquer chaque instruction.
- Pas de confusion entre préparation et exécution.
- La sortie est définie avant l'action, pas après coup.

---

## Règle 4 : Code et Patterns > Prose

Un skill n'est pas un essai littéraire. Insère des exemples concrets.

Pour forcer un format de sortie :
```
📊 RÉSUMÉ
- {SYMBOL} | qty: {qty} | P/L: ${pnl} ({pnl_pct}%)
```

Pour forcer une structure de données :
```json
{
  "signal": "ACHAT",
  "symbol": "BTC/USD",
  "price": 71800.00,
  "donchian_high": 73136.86,
  "donchian_low": 64939.09
}
```

Pour forcer une logique :
```python
if not has_position and close > donchian_high:
    signal = "ACHAT"
elif has_position and close < donchian_low:
    signal = "VENTE"
else:
    signal = "AUCUN"
```

Règle d'or : **une IA reproduit un pattern fourni beaucoup mieux qu'elle n'invente ce que tu veux.**

---

## Règle 5 : Description "Pushy" dans le Frontmatter

Le frontmatter décide si le skill s'active automatiquement ou reste dormant. Il doit être chirurgical.

❌ Vague (ne se déclenchera jamais correctement) :
```yaml
description: "Aide avec le trading."
```

✅ Pushy (activation précise) :
```yaml
description: |
  Stratégie Donchian Channel Breakout automatisée pour crypto (BTC/USD, ETH/USD).
  Se déclenche dès que l'utilisateur mentionne : Donchian, breakout, signal trading,
  stratégie crypto, cron trading, vérifier les signaux, ou toute demande liée au
  système de trading automatisé Donchian.
```

La structure :
1. **Ligne 1** : Ce que fait le skill en une phrase complète.
2. **Ligne 2** : "Se déclenche dès que l'utilisateur mentionne : [liste exhaustive de triggers]"

Sois généreux sur les triggers : mets les synonymes, les variantes, les expressions naturelles.

---

## Récapitulatif

| # | Règle | Pattern |
|---|-------|---------|
| 1 | Impératif + raison | "[Verbe] [quoi], car [pourquoi]." |
| 2 | Négation + alternative | "Ne [pas] [X], [fais Y] à la place." |
| 3 | Chronologie | Avant / Pendant / Après |
| 4 | Code > Prose | Templates, JSON, Python, exemples |
| 5 | Description pushy | "[Ce que ça fait]. Se déclenche dès que [triggers]." |
