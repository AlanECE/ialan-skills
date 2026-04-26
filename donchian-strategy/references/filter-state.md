# Filter State Tracking

Ce fichier track l'état des filtres pour éviter les signaux non désirés.

## Structure

```json
{
  "last_closed": {
    "BTC/USD": "2026-04-20T10:00:00Z",
    "ETH/USD": null,
    "SOLUSD": null
  },
  "cooldown_hours": 12,
  "time_stop_hours": 24,
  "time_stop_min_profit_pct": 2.0,
  "atr_threshold": 1.0,
  "volume_ratio_threshold": 1.5
}
```

## Utilisation

- `last_closed[SYMBOL]` = timestamp de la dernière fermeture de position
- Si `now - last_closed < cooldown_hours` → signal bloqué
- Mettre à jour après chaque fermeture de position

## Fonctions helper

### is_cooldown_active(symbol, now)
```
last = last_closed[symbol]
IF last IS NULL → return False
elapsed_hours = (now - last) / 3600
return elapsed_hours < cooldown_hours
```

### is_time_stop_triggered(position_opened_at, pnl_pct, now)
```
elapsed_hours = (now - position_opened_at) / 3600
return elapsed_hours > time_stop_hours AND pnl_pct < time_stop_min_profit_pct
```
