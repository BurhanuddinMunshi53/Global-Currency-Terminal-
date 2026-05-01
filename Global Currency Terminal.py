import requests
import json
import os
import time
import sys
import random

# --- STARK INDUSTRIES COLOR PROTOCOL ---
class Colors:
    HOLO   = '\033[38;5;51m'   # Electric Cyan
    NEON   = '\033[38;5;45m'   # Deep Hologram Blue
    CORE   = '\033[38;5;159m'  # Arc Reactor White
    GHOST  = '\033[38;5;244m'  # Faded Blueprint Gray
    WARN   = '\033[38;5;196m'  # Signal Red
    ACCENT = '\033[38;5;226m'  # Gold Accent
    BOLD   = '\033[1m'
    RESET  = '\033[0m'

BOLD, RESET = Colors.BOLD, Colors.RESET

# --- API NODES ---
API_URL = "https://open.er-api.com/v6/latest/"
METALS_API = "https://api.gold-api.com/price"

# --- GLOBAL GEOPOLITICAL MATRIX (ALL 195+ NODES) ---
GLOBAL_MAP = {
    "AFRICA": {"Algeria": "DZD", "Angola": "AOA", "Benin": "XOF", "Botswana": "BWP", "Burkina Faso": "XOF", "Burundi": "BIF", "Cabo Verde": "CVE", "Cameroon": "XAF", "Central African Rep": "XAF", "Chad": "XAF", "Comoros": "KMF", "Congo": "XAF", "Djibouti": "DJF", "Egypt": "EGP", "Equatorial Guinea": "XAF", "Eritrea": "ERN", "Eswatini": "SZL", "Ethiopia": "ETB", "Gabon": "XAF", "Gambia": "GMD", "Ghana": "GHS", "Guinea": "GNF", "Ivory Coast": "XOF", "Kenya": "KES", "Lesotho": "LSL", "Liberia": "LRD", "Libya": "LYD", "Madagascar": "MGA", "Malawi": "MWK", "Mali": "XOF", "Mauritania": "MRU", "Mauritius": "MUR", "Morocco": "MAD", "Mozambique": "MZN", "Namibia": "NAD", "Niger": "XOF", "Nigeria": "NGN", "Rwanda": "RWF", "Senegal": "XOF", "Seychelles": "SCR", "Sierra Leone": "SLE", "Somalia": "SOS", "South Africa": "ZAR", "South Sudan": "SSP", "Sudan": "SDG", "Tanzania": "TZS", "Togo": "XOF", "Tunisia": "TND", "Uganda": "UGX", "Zambia": "ZMW", "Zimbabwe": "ZWL"},
    "ASIA": {"Afghanistan": "AFN", "Armenia": "AMD", "Azerbaijan": "AZN", "Bahrain": "BHD", "Bangladesh": "BDT", "Bhutan": "BTN", "Brunei": "BND", "Cambodia": "KHR", "China": "CNY", "Georgia": "GEL", "Hong Kong": "HKD", "India": "INR", "Indonesia": "IDR", "Iran": "IRR", "Iraq": "IQD", "Israel": "ILS", "Japan": "JPY", "Jordan": "JOD", "Kazakhstan": "KZT", "Kuwait": "KWD", "Kyrgyzstan": "KGS", "Laos": "LAK", "Lebanon": "LBP", "Macao": "MOP", "Malaysia": "MYR", "Maldives": "MVR", "Mongolia": "MNT", "Myanmar": "MMK", "Nepal": "NPR", "North Korea": "KPW", "Oman": "OMR", "Pakistan": "PKR", "Palestine": "ILS", "Philippines": "PHP", "Qatar": "QAR", "Saudi Arabia": "SAR", "Singapore": "SGD", "South Korea": "KRW", "Sri Lanka": "LKR", "Syria": "SYP", "Taiwan": "TWD", "Tajikistan": "TJS", "Thailand": "THB", "Turkey": "TRY", "Turkmenistan": "TMT", "UAE": "AED", "Uzbekistan": "UZS", "Vietnam": "VND", "Yemen": "YER"},
    "EUROPE": {"Albania": "ALL", "Andorra": "EUR", "Austria": "EUR", "Belarus": "BYN", "Belgium": "EUR", "Bosnia": "BAM", "Bulgaria": "BGN", "Croatia": "EUR", "Cyprus": "EUR", "Czech Republic": "CZK", "Denmark": "DKK", "Estonia": "EUR", "Finland": "EUR", "France": "EUR", "Germany": "EUR", "Greece": "EUR", "Hungary": "HUF", "Iceland": "ISK", "Ireland": "EUR", "Italy": "EUR", "Latvia": "EUR", "Liechtenstein": "CHF", "Lithuania": "EUR", "Luxembourg": "EUR", "Malta": "EUR", "Moldova": "MDL", "Monaco": "EUR", "Montenegro": "EUR", "Netherlands": "EUR", "North Macedonia": "MKD", "Norway": "NOK", "Poland": "PLN", "Portugal": "EUR", "Romania": "RON", "Russia": "RUB", "Serbia": "RSD", "Slovakia": "EUR", "Slovenia": "EUR", "Spain": "EUR", "Sweden": "SEK", "Switzerland": "CHF", "Ukraine": "UAH", "United Kingdom": "GBP"},
    "AMERICAS": {"Antigua": "XCD", "Argentina": "ARS", "Bahamas": "BSD", "Barbados": "BBD", "Belize": "BZD", "Bolivia": "BOB", "Brazil": "BRL", "Canada": "CAD", "Chile": "CLP", "Colombia": "COP", "Costa Rica": "CRC", "Cuba": "CUP", "Dominica": "XCD", "Dominican Rep": "DOP", "Ecuador": "USD", "El Salvador": "USD", "Grenada": "XCD", "Guatemala": "GTQ", "Guyana": "GYD", "Haiti": "HTG", "Honduras": "HNL", "Jamaica": "JMD", "Mexico": "MXN", "Nicaragua": "NIO", "Panama": "PAB", "Paraguay": "PYG", "Peru": "PEN", "St Lucia": "XCD", "Suriname": "SRD", "Trinidad": "TTD", "USA": "USD", "Uruguay": "UYU", "Venezuela": "VES"},
    "OCEANIA": {"Australia": "AUD", "Fiji": "FJD", "Kiribati": "AUD", "Marshall Islands": "USD", "Micronesia": "USD", "Nauru": "AUD", "New Zealand": "NZD", "Palau": "USD", "Papua New Guinea": "PGK", "Samoa": "WST", "Solomon Islands": "SBD", "Tonga": "TOP", "Tuvalu": "AUD", "Vanuatu": "VUV"}
}

# --- CINEMATIC ANIMATION ENGINE ---

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def spectral_glitch(text, speed=0.01):
    """Spectral decryption - Best used for labels/briefs."""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#$@&"
    for char in text:
        for _ in range(4):
            color = random.choice([Colors.NEON, Colors.HOLO, Colors.CORE])
            sys.stdout.write(f"{color}{random.choice(chars)}{RESET}")
            sys.stdout.flush()
            time.sleep(speed/4)
            sys.stdout.write('\b')
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def draw_hud(title):
    clear()
    sig = hex(random.randint(0x100000, 0xFFFFFF)).upper()
    print(f"{Colors.HOLO}╔" + "═"*62 + "╗")
    print(f"║ {Colors.CORE}{BOLD}{title:^60}{RESET}{Colors.HOLO} ║")
    print(f"╠" + "═"*62 + "╣")
    print(f"║ {Colors.GHOST}LINK: {Colors.CORE}SATELLITE{Colors.GHOST} | NODE: {Colors.CORE}{sig}{Colors.GHOST} | MODE: {Colors.HOLO}OMNI ZENITH{Colors.HOLO} ║")
    print(f"╚" + "═"*62 + f"╝{RESET}")

def laser_scan(label):
    sys.stdout.write(f" {Colors.NEON}» {Colors.GHOST}{label:<25} {RESET}")
    width = 25
    for i in range(width + 1):
        bar = f"{Colors.HOLO}█" * i + f"{Colors.GHOST}▒" * (width - i)
        sys.stdout.write(f"\r {Colors.NEON}» {Colors.GHOST}{label:<25} {bar} {Colors.CORE}{i*4}%{RESET}")
        sys.stdout.flush()
        time.sleep(0.02)
    print(f" {Colors.CORE} SUCCESS{RESET}")

# --- TACTICAL OMNI MODULES ---

def mod_01_global_market_stream():
    draw_hud("GLOBAL MARKET DATA STREAM")
    spectral_glitch(" Brief: Pulling 195 node valuations from global satellites...")
    try:
        r = requests.get(f"{API_URL}USD", timeout=10).json()
        rates = r.get("rates", {})
        for cont, countries in GLOBAL_MAP.items():
            print(f"\n {Colors.HOLO}╾╼ {Colors.CORE}{cont}{Colors.HOLO} " + "─"*(44-len(cont)) + "┐")
            for name, code in sorted(countries.items()):
                val = rates.get(code, 0.0)
                print(f"  {Colors.NEON}◈ {Colors.GHOST}{name:<25} {Colors.CORE}{val:>11.2f} {code}{RESET}")
    except: print(f" {Colors.WARN}!! DATA UPLINK BROKEN{RESET}")

def mod_02_precious_metal_vault():
    """STABLE RENDER: Purged 'm', 'z', and corruption artifacts."""
    draw_hud("PRECIOUS METALS SECURE VAULT")
    laser_scan("SPOT PRICE EXTRACTION")
    try:
        # Secure Pull
        g = float(requests.get(f"{METALS_API}/XAU").json().get("price", 0))
        s = float(requests.get(f"{METALS_API}/XAG").json().get("price", 0))
        p = float(requests.get(f"{METALS_API}/XPT").json().get("price", 0))
        pd = float(requests.get(f"{METALS_API}/XPD").json().get("price", 0))
        
        print(f"\n {Colors.NEON}─── LIVE METAL VALUATIONS ───{RESET}")
        
        # PROTOCOL: Label uses Glitch / Value uses Pulse for zero-corruption
        labels = ["GOLD ASSET", "SILVER ASSET", "PLATINUM ASSET", "PALLADIUM ASSET"]
        vals = [g, s, p, pd]
        cols = [Colors.ACCENT, Colors.GHOST, Colors.CORE, Colors.HOLO]
        
        for label, val, col in zip(labels, vals, cols):
            # Print label with animation
            sys.stdout.write(f" {Colors.HOLO}◈ ")
            for char in f"{label:<18}":
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.01)
            
            # Print value with static pulse (Fixes the "m/z" corruption)
            print(f" {col}${val:>12,.2f}{RESET}")
            time.sleep(0.1)
        
        print(f"\n {Colors.GHOST}Analysis: Physical asset verification complete.{RESET}")
    except:
        print(f" {Colors.WARN}!! VAULT ACCESS DENIED: NODE ERROR{RESET}")

def mod_03_high_precision_parity():
    draw_hud("HIGH PRECISION PARITY CALC")
    spectral_glitch(" Brief: Computational node for exact currency arbitrage math.")
    try:
        s = input(f" {Colors.HOLO}Source Code: {RESET}").upper().strip()
        t = input(f" {Colors.HOLO}Target Code: {RESET}").upper().strip()
        v_in = input(f" {Colors.HOLO}Input Value: {RESET}")
        v = float(v_in)
        r = requests.get(f"{API_URL}{s}").json()
        res = v * r['rates'][t]
        print(f"\n {Colors.NEON}─── COMPUTATION COMPLETE ───{RESET}")
        print(f" {Colors.CORE}{v:,.2f} {s} = {res:,.2f} {t}{RESET}")
    except: print(f" {Colors.WARN}!! CALCULATION FAILURE{RESET}")

def mod_04_geospatial_node_search():
    draw_hud("GEOSPATIAL NODE SEARCH")
    q = input(f" {Colors.HOLO}Search Country or Code: {RESET}").lower().strip()
    laser_scan("SCANNING GLOBAL DIRECTORY")
    for cont, countries in GLOBAL_MAP.items():
        for name, code in countries.items():
            if q in name.lower() or q in code.lower():
                print(f" {Colors.NEON}▶ {Colors.CORE}{name:<25}{RESET} {Colors.GHOST}NODE: {code}{RESET} | {cont}")

def mod_05_market_volatility_radar():
    draw_hud("MARKET VOLATILITY RADAR")
    spectral_glitch(" Brief: Measuring systemic risk and variance in regional nodes.")
    for n in ["USD/EUR", "GBP/USD", "JPY/USD", "INR/USD"]:
        lvl = random.choice(["SECURE", "VOLATILE", "CRITICAL"])
        color = Colors.CORE if lvl == "SECURE" else Colors.WARN
        print(f" {Colors.GHOST}NODE: {n:<12} {RESET} STATUS: {color}{lvl:<10}{RESET} | Entropy check nominal.")
        time.sleep(0.1)

def mod_06_inflation_risk_alerts():
    draw_hud("INFLATION RISK ALERTS")
    spectral_glitch(" Brief: Tracking rapid purchasing power decay and devaluation.")
    risks = {"ARS": "98%", "VES": "352%", "TRY": "65%", "LBP": "122%"}
    for node, pct in risks.items():
        print(f" {Colors.WARN}⚠ {node:<6}{RESET} {Colors.GHOST}Decline Factor: {RESET}{Colors.WARN}{pct}{RESET} | CRITICAL DEPTH")

def mod_07_central_bank_rates():
    draw_hud("CENTRAL BANK INTEREST RATES")
    spectral_glitch(" Brief: Monitoring benchmark rates affecting global liquidity.")
    rates = {"FED": "5.50%", "ECB": "4.50%", "RBI": "6.50%", "BOE": "5.25%"}
    for bank, val in rates.items():
        print(f" {Colors.HOLO}BANK: {bank:<8} {RESET} RATE: {Colors.CORE}{val}{RESET}")

def mod_08_liquidity_diagnostics():
    draw_hud("LIQUIDITY DEPTH DIAGNOSTICS")
    laser_scan("MEASURING TRANSACTION FRICTION")
    hubs = ["London Hub", "New York Hub", "Singapore Hub", "Tokyo Hub"]
    for h in hubs:
        print(f" {Colors.GHOST}NODE: {h:<18} {RESET} {Colors.CORE}LIQUIDITY: OPTIMAL{RESET}")

def mod_09_strength_momentum_map():
    draw_hud("STRENGTH AND MOMENTUM MAP")
    spectral_glitch(" Brief: Highlighting bullish momentum vs bearish decay.")
    print(f" {Colors.CORE}BULLISH MOMENTUM{RESET}: {Colors.HOLO}USD, CHF, SGD, AED{RESET}")
    print(f" {Colors.WARN}BEARISH DECAY   {RESET}: {Colors.WARN}JPY, ARS, TRY, RUB{RESET}")

def mod_10_terminal_diagnostics():
    draw_hud("TERMINAL SYSTEM DIAGNOSTICS")
    laser_scan("CORE INTEGRITY CHECK")
    laser_scan("SATELLITE SYNC SPEED")
    spectral_glitch(f" {Colors.CORE}✓ ARCH: OMNI ZENITH v14.2{RESET}")
    spectral_glitch(f" {Colors.CORE}✓ ENCRYPTION: STARK LEVEL 10{RESET}")

# --- MAIN HUB ---

def main():
    clear()
    spectral_glitch(f"{Colors.HOLO}AetherOS v14.2 Omni Terminal Booting...{RESET}")
    laser_scan("ESTABLISHING SATELLITE LINK")
    
    while True:
        draw_hud("AETHER OMNI TERMINAL")
        menu = [
            "GLOBAL MARKET STREAM", "PRECIOUS METAL VAULT", "HIGH PRECISION PARITY", 
            "GEOSPATIAL NODE SEARCH", "MARKET VOLATILITY RADAR", "INFLATION RISK ALERTS", 
            "CENTRAL BANK RATES", "LIQUIDITY DIAGNOSTICS", "STRENGTH MOMENTUM MAP", 
            "TERMINAL DIAGNOSTICS"
        ]
        for i, item in enumerate(menu, 1):
            print(f" {Colors.CORE}{i:02} {Colors.NEON}╾╼{RESET} {Colors.HOLO}{item}{RESET}")
        
        print(f"\n {Colors.WARN}XX {Colors.NEON}╾╼{RESET} {Colors.GHOST}SYSTEM DISCONNECT{RESET}")
        cmd = input(f"\n {Colors.HOLO}STARK ROOT@AETHER: {RESET}").upper().strip()
        
        if cmd in ['1', '01']: mod_01_global_market_stream()
        elif cmd in ['2', '02']: mod_02_precious_metal_vault()
        elif cmd in ['3', '03']: mod_03_high_precision_parity()
        elif cmd in ['4', '04']: mod_04_geospatial_node_search()
        elif cmd in ['5', '05']: mod_05_market_volatility_radar()
        elif cmd in ['6', '06']: mod_06_inflation_risk_alerts()
        elif cmd in ['7', '07']: mod_07_central_bank_rates()
        elif cmd in ['8', '08']: mod_08_liquidity_diagnostics()
        elif cmd in ['9', '09']: mod_09_strength_momentum_map()
        elif cmd in ['10']: mod_10_terminal_diagnostics()
        elif cmd == 'XX':
            clear()
            print("\n" * 3)
            spectral_glitch(f" {Colors.HOLO}>>> INITIATING GLOBAL DISCONNECT PROTOCOL...{RESET}", 0.02)
            time.sleep(0.5)
            spectral_glitch(f" {Colors.CORE}Sir, all nodes are secured. Satellite link severed.{RESET}")
            spectral_glitch(f" {Colors.CORE}AetherOS dormant.{RESET}")
            time.sleep(0.4)
            spectral_glitch(f" {Colors.WARN}>>> [ SYSTEM OFFLINE. GOODNIGHT MR STARK. ]{RESET}", 0.01)
            print("\n" * 3)
            break
        input(f"\n {Colors.GHOST} [ PRESS ENTER TO RE-SYNC HUD ] {RESET}")

if __name__ == "__main__":
    main()
