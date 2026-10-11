# Gelato Connector 🌍

> Autonomous Gelato Open API v2 Connector, Localized 32-Country Print-on-Demand Router, Multi-Currency Margin Engine, and Antigravity MCP Suite.  
> **100% Python Standard Library — Zero External Runtime Dependencies.**  
> Engineered by **Neal Frazier Tech** ([@1nc0gn30](https://github.com/1nc0gn30)) • [NullAI Platform](https://nullai.tech)

---

## 🌟 Sovereign Capabilities

- **Zero-Dependency Architecture**: Built 100% on the Python 3.10+ standard library (`http.server`, `urllib.request`, `json`, `argparse`). Zero external pip packages, zero telemetry leaks.
- **Localized 32-Country Routing**: Automatically routes production to the nearest local factory in 32 nations (US, UK, Germany, France, Italy, Canada, Australia, Japan), slashing cross-border freight costs and cutting carbon emissions by up to 67%.
- **Zero Customs Duties**: Eliminates European and UK import duties and VAT clearance delays by printing directly inside domestic borders.
- **Multi-Currency Margin Engine**: Full formula calculation across USD ($), EUR (€), and GBP (£) for Etsy, Shopify, and Direct Web3 transactions.
- **Museum-Grade Print Auditor**: Validates image dimensions, 300+ DPI resolution, and bleed area tolerances (e.g. 3mm on Acrylic/Aluminum, 5mm on Wood Canvas).
- **Antigravity MCP Suite**: 6 native JSON-RPC 2.0 tools for Claude, Antigravity, and autonomous AI agents.
- **Dual Checkout Cash Registers**: Direct Stripe payment link ($19 lifetime founding member pricing) + DePay Solana Widget.

---

## 🚀 Quickstart

### 1. Run the HTTP & REST Daemon
```bash
./bin/gelato-connector serve --port 8116
```
Visit `http://localhost:8116` in your browser.

### 2. Antigravity MCP Server (Stdio)
```bash
./bin/gelato-connector mcp
```

### 3. CLI Commands
```bash
# System status
./bin/gelato-connector info

# List localized catalog products
./bin/gelato-connector catalog

# Calculate shipping quote for Germany
./bin/gelato-connector shipping --product acrylic_print_16x24 --country DE

# Calculate multi-channel margins in EUR
./bin/gelato-connector margins --product acrylic_print_16x24 --price 68.00 --currency EUR --country DE

# Audit artwork resolution
./bin/gelato-connector audit --product acrylic_print_16x24 --width 4800 --height 7200
```

---

## 🛠️ MCP Tools

1. `gelato_search_catalog`: Search Gelato catalog products (acrylic glass, aluminum Dibond, framed canvas, organic tees, mugs, journals).
2. `gelato_get_shipping_quote`: Calculate localized shipping rates, transit times, and duty savings across 32 countries.
3. `gelato_calculate_margins`: Compute production costs, shipping, fees, net margins, and break-even prices in USD, EUR, or GBP.
4. `gelato_audit_print_spec`: Audit artwork pixel resolution, aspect ratio, and bleed compliance.
5. `gelato_create_order_payload`: Generate validated Gelato order creation payload.
6. `gelato_get_shop_info`: Retrieve connected shop status and production capabilities.

---

## 📜 License & Sovereign Directives
Engineered by **Neal Frazier Tech** ([@1nc0gn30](https://github.com/1nc0gn30)) • NullAI Platform.
All rights reserved.

## Network exposure

The server binds to `127.0.0.1` by default. To reach it from other devices,
opt in explicitly with `--host 0.0.0.0` (or set `ZOTH_BIND_HOST=0.0.0.0`; an IP
in `HOST` is also honoured, a plain hostname is ignored) and only on a trusted
network.
