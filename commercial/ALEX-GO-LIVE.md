> **STATUS: DONE (2026-09-27).** Live mode is active on `acct_1SEM05F4AnhghO8O`.
> Live product `prod_VKQMJ9gLUnevmE`, live price `price_1UJlVcF4AnhghO8OyZcShddd` ($99 one-time),
> live link `plink_1UJlWeF4AnhghO8OjmgTjtZb` -> https://buy.stripe.com/00w28r4Ei8lLdH8bYY08g04
> (wired into the site's BUY_URL). Payment redirects to the GitHub release.
> Steps below are kept as the record of what was done.

# Alex — go live (under 2 minutes)

The pack, license, README, GitHub release, and Stripe **test** Payment Link
already exist. Real money needs live Stripe keys. The CLI currently has
sandbox keys only (`Live mode key: not available`).

## Click-by-click

1. Terminal: `stripe login`
2. Browser: approve the Stripe CLI for the **live** MidnightDev account
   (`acct_1SEM05F4AnhghO8O`, alex11bouchard@gmail.com).
3. Terminal:
   `bash commercial/scripts/create-live-payment-link.sh`
4. Copy the printed `LIVE_URL` (`https://buy.stripe.com/...` — no `test_`).
5. Replace the checkout URL in `README.md` (the Buy button) with `LIVE_URL`.
6. Commit + push to `main`. Done.

Do not paste API keys anywhere. Do not turn promo codes on.

## What you do not do

- You do not email the zip. GitHub release is the download.
- You do not create Gumroad/LemonSqueezy.
- You do not refund from chat; Stripe dashboard if needed.

## Test (already works, no login)

https://buy.stripe.com/test_eVq9AT3wX5S5b5I3k5eME00
Card 4242… — see [TEST-CHECKOUT.md](TEST-CHECKOUT.md).
