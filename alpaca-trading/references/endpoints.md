# Alpaca API — Référence Endpoints Complète

## Base URLs

| Environnement | URL | Usage |
|---------------|-----|-------|
| Paper Trading | `https://paper-api.alpaca.markets` | Simulation (défaut) |
| Live Trading | `https://api.alpaca.markets` | Réel |
| Market Data | `https://data.alpaca.markets` | Données de marché |

---

## Trading Endpoints (`/v2/`)

### Compte
```
GET /v2/account
```
Réponse clés : `equity`, `cash`, `buying_power`, `portfolio_value`, `status`

### Positions
```
GET /v2/positions                    → Toutes les positions
GET /v2/positions/{symbol}           → Position spécifique
DELETE /v2/positions/{symbol}        → Fermer une position
DELETE /v2/positions                 → Fermer TOUTES les positions
```

### Ordres
```
GET /v2/orders                       → Liste des ordres
GET /v2/orders/{order_id}            → Ordre spécifique
POST /v2/orders                      → Passer un ordre
DELETE /v2/orders/{order_id}         → Annuler un ordre
DELETE /v2/orders                    → Annuler TOUS les ordres
```

#### Body POST /v2/orders — Ordre simple
```json
{
  "symbol": "BTCUSD",
  "qty": "0.15",
  "side": "buy",
  "type": "market",
  "time_in_force": "gtc"
}
```

#### Body POST /v2/orders — Bracket (TP + SL)
```json
{
  "symbol": "AAPL",
  "qty": "10",
  "side": "buy",
  "type": "limit",
  "time_in_force": "gtc",
  "limit_price": "180.00",
  "order_class": "bracket",
  "take_profit": { "limit_price": "200.00" },
  "stop_loss": { "stop_price": "170.00" }
}
```

### Assets
```
GET /v2/assets                       → Tous les actifs tradables
GET /v2/assets/{symbol}              → Détails d'un actif
```

---

## Market Data — Crypto (`/v1beta3/crypto/us/`)

⚠️ **Toujours utiliser `/v1beta3/crypto/us/`** pour la crypto. Jamais `/v2/stocks/`.

### Daily Bars
```
GET /v1beta3/crypto/us/bars?symbols=BTC/USD&timeframe=1Day&limit=25
```
Paramètres :
- `symbols` : `BTC/USD`, `ETH/USD` (avec slash)
- `timeframe` : `1Min`, `5Min`, `15Min`, `1Hour`, `1Day`
- `limit` : nombre de barres (max 10000)
- `start` / `end` : ISO 8601 (optionnel)

Réponse (chaque barre) :
```json
{
  "t": "2026-04-09T05:00:00Z",
  "o": 70500.00,
  "h": 71800.00,
  "l": 69900.00,
  "c": 71200.00,
  "v": 1234.56,
  "n": 5678,
  "vw": 70850.00
}
```
- `o` = open, `h` = high, `l` = low, `c` = close
- `v` = volume, `n` = nombre de trades, `vw` = volume-weighted average

### Latest Bar
```
GET /v1beta3/crypto/us/latest/bars?symbols=BTC/USD
```

### Latest Quote
```
GET /v1beta3/crypto/us/latest/quotes?symbols=BTC/USD
```

### Snapshot
```
GET /v1beta3/crypto/us/snapshots?symbols=BTC/USD
```

---

## Market Data — Actions (`/v2/stocks/`)

### Daily Bars
```
GET /v2/stocks/{symbol}/bars?timeframe=1Day&limit=25
```

### Latest Bar
```
GET /v2/stocks/{symbol}/bars/latest
```

### Latest Quote
```
GET /v2/stocks/{symbol}/quotes/latest
```

---

## Table des symboles

| Contexte | Format | Exemple |
|----------|--------|---------|
| Market Data Crypto | Avec slash | `BTC/USD`, `ETH/USD` |
| Ordres Crypto | Sans slash | `BTCUSD`, `ETHUSD` |
| Actions (partout) | Ticker standard | `AAPL`, `MSFT`, `GOOGL` |

---

## Codes d'erreur courants

| Code | Signification | Action |
|------|---------------|--------|
| 200 | OK | — |
| 403 | Forbidden | Vérifier les clés API |
| 404 | Not Found | Vérifier le symbole ou l'endpoint |
| 422 | Unprocessable | Paramètres invalides (qty, symbol...) |
| 429 | Rate Limited | Attendre et retry |
