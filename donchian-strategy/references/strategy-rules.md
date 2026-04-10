# Donchian Breakout — Règles Complètes & Risk Management

## Théorie

Le Donchian Channel (Richard Donchian, 1960s) trace le plus haut et le plus bas sur N périodes.
C'est la base du trend following : quand le prix casse un extrême, une nouvelle tendance démarre.

La stratégie des Turtle Traders (1983) utilisait exactement ce principe sur les commodities.
Elle fonctionne particulièrement bien sur les marchés tendanciels — crypto inclus.

### Caractéristiques attendues

| Métrique | Valeur typique | Explication |
|----------|---------------|-------------|
| Win Rate | 40-50% | Beaucoup de faux breakouts — c'est normal |
| Risk/Reward | 1:2 à 1:3 | Les gagnants sont 2-3x plus gros que les perdants |
| Max Drawdown | 10-25% | Périodes de range = pertes consécutives |
| Profit Factor | 1.5-2.5 | Profitable sur le long terme grâce aux gros gains |

---

## Règles de Base (implémentation actuelle)

### Période : 20 jours (non négociable sauf instruction explicite)

### Calcul
```
Donchian 20-High = MAX(high[i] pour i dans les 20 dernières daily bars)
Donchian 20-Low  = MIN(low[i] pour i dans les 20 dernières daily bars)
```

### Signaux
```
ACHAT  : close > Donchian 20-High ET aucune position ouverte
VENTE  : close < Donchian 20-Low ET position ouverte
AUCUN  : dans tous les autres cas
```

### Exécution
- Ordres MARKET uniquement (on veut l'exécution, pas le prix parfait)
- Time in force : GTC (crypto = 24/7)
- Un seul trade par actif à la fois

---

## Risk Management

### Position Sizing

Formule :
```
Taille = (Capital × % risque par trade) / (Prix entrée - Stop Loss)
```

Paramètres recommandés :
- Risque par trade : 1-2% du capital total
- Stop Loss : Donchian 20-Low (pour les longs) — c'est le stop naturel de la stratégie

Exemple :
```
Capital = $100,000
Risque = 2% = $2,000
Prix entrée BTC = $72,000
Donchian 20-Low = $65,000
Distance au stop = $7,000

Taille = $2,000 / $7,000 = 0.286 BTC
```

### Stop Loss (3 options)

1. **Donchian Low (défaut)** — Le 20-Low EST le stop. Quand le prix le casse, on sort. C'est cohérent avec la stratégie.

2. **ATR-Based (plus serré)** — Stop = Entrée - (2 × ATR 14 jours). S'adapte à la volatilité. Plus serré en marché calme.

3. **Percentage fixe (simple)** — Stop à -5% ou -8% sous l'entrée. Simple mais rigide.

### Limites d'exposition

| Profil | Max par position | Max exposure totale |
|--------|-----------------|---------------------|
| Conservateur | 2% du capital | 20% |
| Modéré | 5% du capital | 40% |
| Agressif | 10% du capital | 60% |

### Règles absolues

1. Ne JAMAIS moyenner à la baisse
2. Ne JAMAIS dépasser 2% de risque par trade
3. Couper les pertes vite, laisser courir les gagnants
4. Paper trade minimum 30 jours avant le réel

---

## Filtres Optionnels (améliorations documentées)

Ces filtres ne sont PAS actifs par défaut. Les implémenter uniquement si l'utilisateur le demande.

### 1. Filtre RSI (réduction des faux breakouts)
```
ACHAT autorisé seulement si RSI(14) > 50
Raison : confirme que le momentum est haussier, filtre les breakouts mous
Impact : réduit les faux signaux de ~30-40%
```

### 2. Filtre Volume
```
ACHAT autorisé seulement si volume > SMA(volume, 20)
Raison : un breakout sur faible volume = souvent un piège
Impact : élimine les breakouts sans conviction du marché
```

### 3. Filtre EMA 200 (tendance de fond)
```
ACHAT autorisé seulement si prix > EMA(200)
VENTE autorisée seulement si prix < EMA(200)
Raison : ne jamais trader contre la tendance de fond
Impact : élimine les trades contre-tendance
```

### 4. Confirmation par clôtures consécutives
```
ACHAT après 2 clôtures consécutives au-dessus du 20-High
Raison : coupe les faux breakouts flash en crypto
Impact : entrées tardives mais plus fiables
```

### 5. Ajustement de période
```
Période 10-15 : plus de signaux, plus de bruit → scalping
Période 20 : équilibre (défaut) → swing trading
Période 50-55 : moins de signaux, plus fiables → position trading
```

---

## Faiblesses connues

- **Marché latéral (range)** : la stratégie génère des faux breakouts et perd de l'argent. C'est structurel et attendu.
- **Entrées tardives** : par définition, on achète APRÈS le début du mouvement.
- **Drawdowns** : les séries de pertes en range testent la discipline. C'est là que 90% des traders abandonnent — c'est aussi là qu'il faut tenir.

La force de Donchian n'est pas dans le win rate. C'est dans l'asymétrie : les pertes sont petites et contenues, les gains sont libres de courir.
