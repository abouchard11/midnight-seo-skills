#!/usr/bin/env bash
# Create the LIVE $99 Payment Link. Requires `stripe login` with live keys.
# Does not charge anyone. Safe to re-run: idempotency keys are stable.
set -euo pipefail
cd "$(dirname "$0")/../.."

if ! stripe whoami 2>/dev/null | grep -q 'Live mode key'; then
  echo "Need live keys. Run: stripe login" >&2
  echo "Then re-run this script." >&2
  exit 1
fi

# Fail closed if we are still on a sandbox/test context
if stripe products list --limit 1 --live >/dev/null 2>&1; then
  :
else
  echo "stripe --live is not authenticated. stripe login, then retry." >&2
  exit 1
fi

PROD=$(stripe products create --live -c \
  --name "Midnight GEO Pro Pack & Commercial License" \
  --description "Single-seat commercial license for the Midnight GEO / SEO skill suite plus bundled ai-citation-patterns research. One-time \$99. Stripe receipt is the license. Download is automatic from the GitHub release. No ranking guarantees." \
  --url "https://github.com/abouchard11/midnight-seo-skills" \
  --active=true \
  -d "metadata[kanban_task]=t_043179bf" \
  -d "metadata[sku]=midnight-geo-pro-v1" \
  --idempotency "t_043179bf-geo-pro-product-live-v1")
echo "$PROD" | tee /tmp/geo-pro-product.json >/dev/null
# Parse id without dumping keys: look for "id": "prod_
PROD_ID=$(python3 -c 'import json,sys; print(json.load(open("/tmp/geo-pro-product.json"))["id"])')

PRICE=$(stripe prices create --live -c \
  --product "$PROD_ID" \
  --unit-amount 9900 \
  --currency usd \
  --nickname "Midnight GEO Pro \$99 one-time" \
  -d "metadata[sku]=midnight-geo-pro-v1" \
  --idempotency "t_043179bf-geo-pro-price-live-v1")
echo "$PRICE" > /tmp/geo-pro-price.json
PRICE_ID=$(python3 -c 'import json; print(json.load(open("/tmp/geo-pro-price.json"))["id"])')

PLINK=$(stripe payment_links create --live -c \
  --line-items[0][price]="$PRICE_ID" \
  --line-items[0][quantity]=1 \
  --after-completion[type]=redirect \
  --after-completion[redirect][url]="https://github.com/abouchard11/midnight-seo-skills/releases/tag/geo-pro-v1.0.0" \
  --customer-creation=always \
  --billing-address-collection=auto \
  --allow-promotion-codes=false \
  --invoice-creation[enabled]=true \
  --submit-type=pay \
  -d "metadata[sku]=midnight-geo-pro-v1" \
  -d "metadata[kanban_task]=t_043179bf" \
  --idempotency "t_043179bf-geo-pro-plink-live-v1")
echo "$PLINK" > /tmp/geo-pro-plink.json
python3 -c 'import json; d=json.load(open("/tmp/geo-pro-plink.json")); print("LIVE_URL", d.get("url")); print("PLINK", d.get("id")); print("PRICE", "'"$PRICE_ID"'"); print("PROD", "'"$PROD_ID"'")'
rm -f /tmp/geo-pro-product.json /tmp/geo-pro-price.json /tmp/geo-pro-plink.json
