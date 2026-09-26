# Grok Bot setup checklist — Midnight GEO Pro Pack v1.2.0

Grok has no bulk import. Do this once per seat.

1. Create bot **midnight-chief** from the matching card in `bot-cards.md`.
2. Create bot **midnight-probe** from the matching card in `bot-cards.md`.
3. Create bot **midnight-audit** from the matching card in `bot-cards.md`.
4. Create bot **midnight-passages** from the matching card in `bot-cards.md`.
5. Create bot **midnight-entity** from the matching card in `bot-cards.md`.
6. Create bot **midnight-map** from the matching card in `bot-cards.md`.
7. Create bot **midnight-acquire** from the matching card in `bot-cards.md`.
8. Create bot **midnight-report** from the matching card in `bot-cards.md`.
9. Create bot **midnight-support** from the matching card in `bot-cards.md`.
10. For each bot, enable only the skills in `enable-lists.md`.
11. Paste the Instructions block as the bot's standing prompt. Do not add ranking guarantees.
12. Point the chief at the other eight names so it can route.
13. Confirm midnight-support's prompt still matches pack-root `SUPPORT.md`.
14. Smoke: ask midnight-chief "who runs a ChatGPT citation probe?" — it should name midnight-probe, not offer to run /geo itself.

On Grok, every bot on an account shares one cloud computer. Names are labels, not a security boundary.
