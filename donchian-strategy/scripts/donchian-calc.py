#!/usr/bin/env python3
"""
Donchian Channel Calculator
Calcule les niveaux Donchian 20-High et 20-Low à partir de daily bars Alpaca.

Usage:
  python donchian-calc.py --symbol BTC/USD --period 20

Requiert: ALPACA_API_KEY et ALPACA_SECRET_KEY en variables d'environnement.
"""

import os
import sys
import json
import argparse
import urllib.request

ALPACA_DATA_URL = "https://data.alpaca.markets"

def get_crypto_bars(symbol: str, limit: int = 25) -> list:
    """Récupère les daily bars crypto depuis Alpaca."""
    url = f"{ALPACA_DATA_URL}/v1beta3/crypto/us/bars?symbols={symbol}&timeframe=1Day&limit={limit}"
    req = urllib.request.Request(url)
    req.add_header("APCA-API-KEY-ID", os.environ["ALPACA_API_KEY"])
    req.add_header("APCA-API-SECRET-KEY", os.environ["ALPACA_SECRET_KEY"])

    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)

    # Les bars sont sous la clé du symbole
    key = symbol.replace("/", "%2F") if symbol not in data.get("bars", {}) else symbol
    bars = data.get("bars", {}).get(symbol, [])
    if not bars:
        # Essayer avec d'autres formats de clé
        for k, v in data.get("bars", {}).items():
            if k.replace("/", "") == symbol.replace("/", ""):
                bars = v
                break
    return bars


def calc_donchian(bars: list, period: int = 20) -> dict:
    """Calcule Donchian High/Low sur les N dernières barres."""
    if len(bars) < period:
        raise ValueError(f"Pas assez de barres: {len(bars)} < {period}")

    recent = bars[-period:]
    high = max(bar["h"] for bar in recent)
    low = min(bar["l"] for bar in recent)
    close = bars[-1]["c"]

    return {
        "donchian_high": high,
        "donchian_low": low,
        "close": close,
        "period": period,
        "bars_used": len(recent),
    }


def generate_signal(donchian: dict, has_position: bool) -> str:
    """Génère le signal de trading."""
    if not has_position and donchian["close"] > donchian["donchian_high"]:
        return "ACHAT"
    elif has_position and donchian["close"] < donchian["donchian_low"]:
        return "VENTE"
    return "AUCUN"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Donchian Channel Calculator")
    parser.add_argument("--symbol", default="BTC/USD", help="Symbole crypto (ex: BTC/USD)")
    parser.add_argument("--period", type=int, default=20, help="Période Donchian (défaut: 20)")
    parser.add_argument("--has-position", action="store_true", help="Flag si position ouverte")
    args = parser.parse_args()

    try:
        bars = get_crypto_bars(args.symbol, limit=args.period + 5)
        donchian = calc_donchian(bars, args.period)
        signal = generate_signal(donchian, args.has_position)

        print(f"📈 {args.symbol}")
        print(f"   Prix: ${donchian['close']:,.2f}")
        print(f"   Donchian {args.period}-high: ${donchian['donchian_high']:,.2f}")
        print(f"   Donchian {args.period}-low: ${donchian['donchian_low']:,.2f}")
        print(f"   🎯 Signal: {signal}")

    except Exception as e:
        print(f"❌ Erreur: {e}", file=sys.stderr)
        sys.exit(1)
