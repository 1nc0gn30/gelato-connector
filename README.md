<p align="center">
  <img src="assets/hero-banner.svg" alt="Gelato Connector: Gelato API client, local-hub shipping engine, multi-currency margin engine and MCP server" width="100%" />
</p>

# Gelato Connector

Zero-dependency Python 3.10+ toolkit for Gelato print-on-demand work: a bundled product reference catalog, a local-production shipping engine over 10 Gelato hub countries, a multi-currency (USD/EUR/GBP) margin calculator for Etsy, Shopify and direct checkout, an artwork print-spec auditor, a Gelato order-payload builder, a loopback HTTP workstation, and a 6-tool MCP stdio server.

- Zoth Studio v2 dossier: https://zoth.nullai.tech/tools/gelato-connector
- Local workstation: `http://127.0.0.1:8116`
- Runtime dependencies: none (Python standard library only)
- License: MIT

## What It Does

- **Catalog lookup**: 7 bundled products (acrylic and aluminum prints, framed canvas, organic tee, 15oz mug, enamel camp mug, hardcover journal) with USD/EUR/GBP base costs and print specs.
- **Shipping engine**: for a destination with a bundled hub (US, CA, UK, DE, FR, IT, ES, NL, AU, JP) it quotes local-production cost, carrier and 2-4 day transit (1-2 express). Other destinations get a cross-border quote (7-14 days). Each quote reports the saving versus a cross-border baseline.
- **Margin engine**: base cost in the chosen currency plus shipping, channel fees (Etsy 6.5% transaction + 3% + $0.25 payment + listing fee; Shopify and direct checkout 2.9% + $0.30), net profit, margin %, break-even price and recommended price tiers, per channel.
- **Artwork auditor**: pixel size and effective DPI against the product's recommended DPI (300 DPI = print ready).
- **Order payload builder**: Gelato order JSON (`orderType`, references, currency by destination, shipping address, item with `productUid` and file URL).
- **Shop info**: with `GELATO_API_KEY` set, verifies the key with `GET https://product.gelatoapis.com/v3/catalogs`. Without a key it returns `api_connected: false` and a configuration hint; it never fabricates account data.

Catalog prices, hub lead times and shipping costs are bundled reference values for planning. Confirm current figures in your Gelato dashboard before pricing products.

## How It Works

```text
src/gelato_connector/
├── catalog.py          # Bundled product reference data + slug lookup
├── shipping_engine.py  # LOCAL_HUBS table (10 countries) and shipping quotes
├── margin_engine.py    # Per-channel fees, net profit, break-even, price tiers
├── artwork_auditor.py  # Effective DPI and print-readiness grade
├── client.py           # Stdlib Gelato client (live only when GELATO_API_KEY is set) + order payload builder
├── mcp_server.py       # MCP stdio server (JSON-RPC 2.0: initialize, tools/list, tools/call)
├── server.py           # Loopback HTTP API + static workstation from public/
└── cli.py              # `gelato-connector` entry point
bin/gelato-connector       # Runs the CLI from a checkout without installing
bin/gelato-connector-tui   # Terminal summary + benchmark of the real margin/shipping engines
public/                    # Browser workstation (margin calculator, DPI auditor, hub table, payload builder)
```

The HTTP server binds to `127.0.0.1` unless you pass `--host` or set `ZOTH_BIND_HOST` to an IP literal, and rejects browser `POST` requests from non-local origins.

## Install

```bash
git clone https://github.com/1nc0gn30/gelato-connector.git
cd gelato-connector
python3 -m pip install -e .

# Start the workstation on http://127.0.0.1:8116
python3 server.py --host 127.0.0.1 --port 8116
# or, after installing:
gelato-connector serve --port 8116
# or, without installing:
./bin/gelato-connector serve
```

`npm start` runs the same `python3 server.py --host 127.0.0.1 --port 8116`.

## Configuration

| Variable | Required | Purpose |
| :--- | :--- | :--- |
| `GELATO_API_KEY` | No | Gelato API key (dashboard: Developer > API Keys). Enables live key verification and live catalog listing. |
| `ZOTH_BIND_HOST` | No | IP literal to bind instead of `127.0.0.1`. |
| `PORT` | No | Backend port used by the optional Electron shell (`electron/main.cjs`, default 8116). |

## CLI Reference

```bash
gelato-connector --help
gelato-connector --version
gelato-connector --json                  # status as JSON
gelato-connector status [--json] [--port 8116]
gelato-connector serve [--host 127.0.0.1] [--port 8116]
gelato-connector mcp
gelato-connector catalog [--category Apparel]
gelato-connector shipping --product acrylic_print_16x24 --country DE [--express]
gelato-connector margins --product acrylic_print_16x24 --price 68 --currency USD --country US
gelato-connector audit --product acrylic_print_16x24 --width 4800 --height 7200 [--name art.png]

gelato-connector-tui [--json] [--product acrylic_print_16x24] [--price 68] [--iterations 50]
```

## MCP Reference

```json
{
  "mcpServers": {
    "gelato-connector": { "command": "gelato-connector", "args": ["mcp"] }
  }
}
```

| Tool | Description |
| :--- | :--- |
| `gelato_search_catalog` | Search the bundled catalog by keyword or category |
| `gelato_get_shipping_quote` | Local-hub or cross-border shipping quote for a product and destination |
| `gelato_calculate_margins` | Fees, net profit, margin and break-even for one channel and currency |
| `gelato_audit_print_spec` | Effective DPI and print-readiness check |
| `gelato_create_order_payload` | Gelato order JSON for a product, file URL and address |
| `gelato_get_shop_info` | Live key verification, or `api_connected: false` with a configuration hint |

## REST Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health`, `/api/health` | Status, version, bound port, `apiConfigured` |
| `GET` | `/api/stats` | Product count and hub-country count |
| `GET` | `/api/products[?category=]` | Product list |
| `GET` | `/api/products/<id>` | Single product (404 if unknown) |
| `GET` | `/api/hubs` | Bundled hub table |
| `POST` | `/api/margins` | `{productId, retailPrice, currency, destinationCountry}` |
| `POST` | `/api/shipping` | `{productId, destinationCountry, isExpress, quantity}` |
| `POST` | `/api/audit` | `{productId, widthPx, heightPx, fileName}` |
| `POST` | `/api/create-payload` | `{productId, imageUrl, recipientName, addressLine, city, country, postalCode}` |

## Port

`127.0.0.1:8116`, matching the `gelato-connector` entry in Zoth Studio v2 `tools.json`, and used as the default by `server.py`, the CLI, `package.json` scripts and `electron/main.cjs`. On ZothOS v3.4.0 the `gelato-connector` and `gelato-connector-tui` commands are installed to `/usr/local/bin/`. `pod-smart-router` (:8117) probes this connector at `127.0.0.1:8116` (`/health`, `/api/products`) when routing orders.

## Testing

```bash
python3 -m pytest -q          # or: npm test
gitleaks dir --no-banner .
```

Tests start the HTTP server on an ephemeral port (`port=0`) and make no external network calls.

## License

MIT. Copyright (c) 2026 [1nc0gn30](https://1nc0gn30.si) and [NullAI](https://nullai.tech). See [LICENSE](LICENSE).

Free and open-source. Optional support: [Buy Us a Coffee (Stripe)](https://buy.stripe.com/3cIfZg27PdKo2D64Ocfw40X).
