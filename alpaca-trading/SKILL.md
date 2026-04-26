---
name: alpaca-trading
description: |
  Interface Alpaca Markets pour trader actions et crypto via API REST.
  Se déclenche dès que l'utilisateur mentionne : Alpaca, positions, ordres, account, 
  buying power, portfolio, passer un ordre, market data, daily bars, ou tout terme lié 
  au broker Alpaca.
metadata:
  author: community
  version: "4.0.0"
  tags: [trading, alpaca, crypto, stocks, api, broker]
  openclaw:
    emoji: "📈"
    requires:
      env: ["ALPACA_API_KEY", "ALPACA_SECRET_KEY"]
---

# Alpaca Trading — Skill Broker (v4.0)

Tu es l'interface directe avec Alpaca Markets. Ton rôle : exécuter les opérations de trading via l'API REST ou les outils MCP natifs.

---

## 🎯 Règle #1 : Utiliser les outils MCP en priorité

Tu as accès aux outils MCP Alpaca natifs — utilise-les directement:

| Outil MCP | Usage |
|-----------|-------|
| `get_account_info` | Infos compte (equity, cash, buying_power) |
| `get_all_positions` | Toutes les positions ouvertes |
| `get_open_position` | Position spécifique |
| `place_crypto_order` | Ordre crypto |
| `place_stock_order` | Ordre action/ETF |
| `close_position` | Fermer une position (total ou partiel) |
| `get_orders` | Liste des ordres |
| `get_order_by_id` | Détails d'un ordre |
| `cancel_order_by_id` | Annuler un ordre |
| `get_crypto_bars` | Données OHLCV crypto |
| `get_stock_bars` | Données OHLCV actions |
| `get_crypto_snapshot` | Snapshot prix crypto |
| `get_clock` | Statut du marché (open/closed) |
| `get_calendar` | Calendrier trading |

---

## ⚠️ Formats critiques — NE JAMAIS IGNORER

### Symboles — Source d'erreurs #1

| Contexte | Format | Exemple |
|----------|--------|---------|
| **MCP `get_crypto_bars`** | Avec slash | `BTC/USD`, `ETH/USD`, `SOL/USD` |
| **MCP `place_crypto_order`** | Avec slash | `BTC/USD`, `ETH/USD`, `SOL/USD` |
| **MCP `get_open_position`** | Sans slash | `BTCUSD`, `ETHUSD` |
| **API REST Market Data** | Avec slash | `BTC/USD` |
| **API REST Ordres** | Sans slash | `BTCUSD` |

### Règle de validation des symboles

**TOUJOURS** vérifier qu'un symbole est tradable avant de trader:

```javascript
// Vérifier via get_asset ou la liste des assets
const asset = get_asset("AAPL");
if (!asset.tradable) {
  throw new Error("AAPL n'est pas tradable sur Alpaca");
}
```

### Stop-Limit Orders — Source d'erreurs #2

**TOUJOURS** fournir `stop_price` ET `limit_price`:

```javascript
place_crypto_order(
  symbol="SOL/USD",
  side="sell",
  qty="60",
  type="stop_limit",
  stop_price="80.55",    // Prix déclencheur
  limit_price="80.00",   // Prix limite minimum
  time_in_force="gtc"
)
```

### Sub-Penny Rules — Source d'erreurs #3

**Règles de décimales pour limit_price et stop_price:**

| Prix | Décimales max | Exemple |
|------|---------------|---------|
| `≥ $1.00` | **2 décimales** | `100.25` ✅, `100.251` ❌ |
| `< $1.00` | **4 décimales** | `0.1234` ✅, `0.12345` ❌ |

**Erreur typique:** `invalid limit_price ... sub-penny increment does not fulfill minimum pricing criteria`

### Quantités crypto — Source d'erreurs #4

Toujours en **string** pour la précision décimale:
- ✅ `qty="0.0748"`
- ❌ `qty=0.0748`

### qty vs notional — Source d'erreurs #5

**JAMAIS les deux en même temps:**
- `qty` = nombre de parts/coins
- `notional` = montant en dollars (market orders only)

```javascript
// ✅ Correct — qty seulement
place_crypto_order(symbol="BTC/USD", side="buy", qty="0.15", type="market", time_in_force="gtc")

// ✅ Correct — notional seulement (market orders)
place_crypto_order(symbol="BTC/USD", side="buy", notional="5000", type="market", time_in_force="gtc")

// ❌ INCORRECT — les deux en même temps
place_crypto_order(symbol="BTC/USD", side="buy", qty="0.15", notional="5000", type="market")
```

---

## 📊 Types d'ordres disponibles

| Type | Usage | Paramètres requis |
|------|-------|-------------------|
| `market` | Exécution immédiate | `symbol`, `qty` OU `notional`, `side` |
| `limit` | Prix exact ou mieux | + `limit_price` |
| `stop` | Déclenche au seuil | + `stop_price` |
| `stop_limit` | Stop puis limite | + `stop_price` + `limit_price` |
| `trailing_stop` | Suit le prix | + `trail_percent` OU `trail_price` (un seul) |

---

## ⏰ Time in Force — Compatibilité CRITIQUE

### Tableau de compatibilité complet

| Type | Actions (whole) | Actions (fractional) | Crypto |
|------|-----------------|---------------------|--------|
| `market` | day, gtc, ioc, fok | **day only** | gtc, ioc |
| `limit` | day, gtc, ioc, fok, opg, cls | **day only** | gtc, ioc |
| `stop` | day, gtc | **day only** | — |
| `stop_limit` | day, gtc | **day only** | gtc |
| `trailing_stop` | day, gtc | **day only** | — |

### Règles par type d'actif

**Actions classiques (qty entière):**
- `day` et `gtc` ok pour tous types d'ordres
- `ioc`, `fok` : liquidité urgente, support limité
- `opg`, `cls` : market/limit seulement (ouverture/fermeture)

**Actions fractionnelles:**
- **SEULEMENT `day`** comme TIF
- Pas de `gtc` pour fractionnel!

**Crypto:**
- `gtc` par défaut (marché 24/7)
- `ioc` pour liquidité urgente

---

## 🌙 Extended Hours Trading

**Conditions obligatoires:**

1. `extended_hours=True` sur l'ordre
2. `type="limit"` **UNIQUEMENT**
3. `time_in_force` = `day` OU `gtc`

**Plages horaires:**
- Overnight: 20:00 - 04:00 ET
- Pre-market: 04:00 - 09:30 ET
- After-hours: 16:00 - 20:00 ET

```javascript
// ✅ Correct — extended hours
place_stock_order(
  symbol="SPY",
  side="buy",
  qty="10",
  type="limit",
  limit_price="580.00",
  time_in_force="day",
  extended_hours=true
)

// ❌ INCORRECT — market order en extended hours
place_stock_order(symbol="SPY", side="buy", qty="10", type="market", extended_hours=true)
```

---

## 🔧 Ordres avancés

### Bracket Orders (entrée + TP + SL)

```javascript
place_crypto_order(
  symbol="BTC/USD",
  side="buy",
  qty="0.15",
  type="market",
  time_in_force="gtc",
  order_class="bracket",
  take_profit={limit_price: "72000"},
  stop_loss={stop_price: "63000", limit_price: "62900"}
)
```

**Règles:**
- `take_profit.limit_price` > `stop_loss.stop_price` pour BUY
- `take_profit.limit_price` < `stop_loss.stop_price` pour SELL
- `time_in_force` = `day` ou `gtc` seulement
- Pas de `extended_hours`

### OCO (One-Cancels-Other)

Pour une position **déjà ouverte** — seulement TP + SL:

```javascript
place_crypto_order(
  symbol="BTC/USD",
  side="sell",
  qty="0.15",
  type="limit",
  order_class="oco",
  take_profit={limit_price: "72000"},
  stop_loss={stop_price: "63000", limit_price: "62900"}
)
```

### OTO (One-Triggers-Other)

Entrée + UN seul leg (TP ou SL):

```javascript
place_crypto_order(
  symbol="BTC/USD",
  side="buy",
  qty="0.15",
  type="market",
  order_class="oto",
  stop_loss={stop_price: "63000", limit_price: "62900"}
)
```

### Trailing Stop

**UN SEUL** de `trail_price` OU `trail_percent`:

```javascript
// Trailing en dollars
place_crypto_order(
  symbol="BTC/USD",
  side="sell",
  qty="0.15",
  type="trailing_stop",
  trail_price="1000",  // Stop = high - $1000
  time_in_force="gtc"
)

// Trailing en pourcentage
place_crypto_order(
  symbol="BTC/USD",
  side="sell",
  qty="0.15",
  type="trailing_stop",
  trail_percent="5",  // Stop = high * 0.95
  time_in_force="gtc"
)
```

---

## 💰 Buying Power Management

**Règle:** Chaque ordre qui ouvre une position consomme du buying power.

```javascript
// Avant de trader — TOUJOURS vérifier
const account = get_account_info();

if (account.buying_power < order_value) {
  throw new Error(`Buying power insuffisant: ${account.buying_power} < ${order_value}`);
}

// Ordres ouverts non exécutés = buying power bloqué
// → Annuler les ordres périmés pour libérer
```

---

## 🔑 Client Order ID — Tracing

**TOUJOURS** utiliser `client_order_id` pour:

- Identifier la stratégie/source
- Retry safe (idempotence)
- Debug avec le support Alpaca

```javascript
const clientOrderId = `donchian_${symbol}_${Date.now()}_${Math.random().toString(36).slice(2,8)}`;

place_crypto_order(
  symbol="BTC/USD",
  side="buy",
  qty="0.15",
  type="market",
  time_in_force="gtc",
  client_order_id=clientOrderId
)
```

**Retry safe:** Si timeout, retry avec le **même** `client_order_id` → l'API rejette les doublons.

---

## 📈 Données de marché

### get_crypto_bars — IMPORTANT

**TOUJOURS** ajouter `start` pour avoir assez de données:

```javascript
// ✅ Correct — retourne toutes les barres depuis start
get_crypto_bars(
  symbols="BTC/USD",
  timeframe="1Day",
  start="2025-01-01T00:00:00Z"
)

// ❌ Incorrect — retourne seulement 1 barre sans start
get_crypto_bars(
  symbols="BTC/USD",
  timeframe="1Day"
)
```

### Calcul lookback automatique

```javascript
// Pour un lookback de N jours
const startDate = new Date();
startDate.setDate(startDate.getDate() - days);
const startStr = startDate.toISOString();

get_crypto_bars(
  symbols="BTC/USD,ETH/USD",
  timeframe="1Day",
  start=startStr
)
```

---

## 🛡️ Best Practices — Script automatisé

### Checklist avant chaque ordre

1. **Vérifier le compte** — `get_account_info()` → `status == "ACTIVE"`
2. **Vérifier le buying power** — Suffisant pour l'ordre ?
3. **Vérifier le symbole** — `get_asset(symbol).tradable == true`
4. **Vérifier les positions existantes** — Éviter les doublons
5. **Vérifier le marché** — `get_clock()` pour les actions
6. **Vérifier la compatibilité TIF** — Tableau ci-dessus
7. **Vérifier les décimales** — Sub-penny rules

### Risk Management

1. **Stop Loss obligatoire** — Protéger chaque position
2. **Position sizing** — Ne pas risquer plus de 2-5% du portfolio par trade
3. **Break-even** — Monter le SL à l'entrée après +5%
4. **Take Profit partiel** — Verrouiller des gains à +10%/+15%

### Paper vs Live — Séparation stricte

```javascript
// Config claire pour l'environnement
const IS_PAPER = process.env.ALPACA_PAPER === 'true';

// Interdire le live en dev
if (process.env.NODE_ENV === 'development' && !IS_PAPER) {
  throw new Error("LIVE_TRADING interdit en développement!");
}

const tradingClient = new TradingClient(
  process.env.ALPACA_API_KEY,
  process.env.ALPACA_SECRET_KEY,
  paper: IS_PAPER
);
```

### Streaming vs Polling

**Préférer WebSocket** pour suivre les ordres:

- Moins de latence
- Moins de rate limiting
- Updates temps réel

### Ne JAMAIS

- ❌ Passer un ordre sans vérifier le buying power
- ❌ Utiliser le mauvais format de symbole
- ❌ Oublier `limit_price` dans un `stop_limit`
- ❌ Mettre `qty` ET `notional` en même temps
- ❌ Ignorer les règles de décimales (sub-penny)
- ❌ Utiliser `gtc` pour fractionnel
- ❌ Hardcoder les clés API
- ❌ Ignorer les erreurs 4xx/5xx
- ❌ Retry automatiquement après timeout sans vérifier le statut
- ❌ Passer un ordre `market` en extended hours

---

## 🐛 Troubleshooting

| Erreur | Cause | Solution |
|--------|-------|----------|
| HTTP 400 "request body format is invalid" | Mauvais format symbole | Utiliser `SOL/USD` (avec slash) pour orders |
| HTTP 400 "invalid limit_price..." | Sub-penny violation | 2 décimales si ≥$1, 4 si <$1 |
| HTTP 403 Forbidden | Clés API invalides | Vérifier `ALPACA_API_KEY` et `ALPACA_SECRET_KEY` |
| HTTP 404 Not Found | Position inexistante | Vérifier le symbole (`BTCUSD` pour positions) |
| HTTP 422 Unprocessable | Paramètres invalides | Vérifier qty (string), symbol, prices, TIF |
| HTTP 422 "insufficient buying power" | Pas assez de cash | Réduire la taille ou libérer du buying power |
| `get_crypto_bars` retourne 1 barre | Manque `start` | Ajouter `start="YYYY-MM-DDT00:00:00Z"` |
| Stop-limit rejeté | Manque `limit_price` | Ajouter `limit_price` < `stop_price` (sell) |
| Fractional rejeté avec gtc | Mauvais TIF | Utiliser `time_in_force="day"` |
| Extended hours rejeté | Market order | Utiliser `type="limit"` |

---

## 📤 Format de sortie obligatoire

### Compte et positions

```
💰 Compte
   Status: ACTIVE
   Equity: $XX,XXX
   Cash: $XX,XXX
   Buying Power: $XX,XXX

📊 Positions
   {SYMBOL} | qty: X.XX | entrée: $XX | actuel: $XX | P/L: $XX (X.XX%)
```

### Ordres

```
✅ Ordre exécuté
   ID: {order_id}
   Client ID: {client_order_id}
   {side} {qty} {symbol} @ {type}
   Status: {status}
```

### Erreurs

```
❌ Erreur API
   Code: HTTP {code}
   Message: {message_brut}
   Action: {suggestion}
   X-Request-ID: {request_id}  // Pour le support Alpaca
```

---

## 📚 Références

- **Docs Alpaca:** https://docs.alpaca.markets
- **Orders API:** https://docs.alpaca.markets/docs/orders-at-alpaca
- **Market Data:** https://docs.alpaca.markets/docs/about-market-data-api
- **Références détaillées:** `references/endpoints.md`
