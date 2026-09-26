# Studio print launch

Status: All four physical print listings are published on [Ko-fi](https://ko-fi.com/spacechakra/shop) at $35 USD, with high-quality inkjet paper, dispatch in 5–7 business days, $7 U.S. shipping ($1 per additional print), and international shipping quoted before purchase. Worldwide checkout is disabled to avoid unquoted international orders. The exact paper finish remains flexible pending a local test. The website now links directly to each live product. No paid subscription was activated.

## Recommended first offering

Start with four open-edition prints, produced to order, signed by Santiago, unframed, and shipped flat. Use one paper stock and one standard sheet size. Preserve each artwork's aspect ratio with a white border; do not crop every piece to fill the same rectangle. Use a descriptive product name such as “Dancing Dragon — Signed Studio Print.” Avoid claiming archival life or calling a print a limited edition until the materials and edition rules support those claims.

Single-print launch price: $35, with shipping charged separately. A $60 two-print bundle remains a later option and is not currently offered. These are starting prices, not a claim about market demand. Inspect a physical proof before fulfilling paid orders; the initial listing images are explicitly labeled digital artwork previews. Consider a higher-priced hand-embellished version only if the extra time is covered by the price.

`assets/data/prints.js` stores product prices and checkout URLs. Only actual HTTPS Ko-fi `/s/` product links become Buy buttons. `docs/ko-fi-print-listings.json` contains the prepared listing text, shipping terms, and image paths; upload images are in the ignored `_archive_shop_uploads` folder. Never replace a missing product link with a donation-page link.

## Initial selection and source readiness

| Artwork | Available source pixels | Proposed image treatment |
| --- | --- | --- |
| Dancing Dragon | 3500 × 5250 | Portrait, preserve the complete drawing |
| Calm Blue Ocean | 4922 × 4922 | Square image inside a standard sheet |
| Angel vs Devil Pattern | 3105 × 3106 | Square image inside a standard sheet |
| Wild Style | 4600 × 7000 | Portrait, preserve the complete composition |

These dimensions are sufficient for a small-format proof at 300 pixels per inch without enlargement. Pixel dimensions alone do not establish print quality: inspect sharpness, photography, color, dust, and existing borders in the actual print.

Hold Alien Guitar, Minotaur, San Diablo Rock Legend, and The Sun and the Lioness for larger-original research. Current website source files are respectively 1086 × 1448, 1086 × 1448, 1016 × 1547, and 765 × 527 pixels. Do not use website thumbnails or assume artificial enlargement restores missing detail.

## Paper and proofing

1. Use the confirmed HP ENVY 6055e with 8.5 × 11-inch letter sheets. HP lists borderless printing up to this size and support for photo and matte inkjet papers, but start with bordered proofs. Do not treat a 4 × 6-inch media-weight limit as blanket approval for equally heavy letter-size paper.
2. First test HP Premium Plus Satin 8.5 × 11-inch photo paper (CR667A) against a compatible smooth matte inkjet stock from a small sampler. HP lists CR667A as an inkjet photo paper optimized for its inks; verify feeding and print quality on the actual ENVY before buying stock. Choose one finish after proofing. Heavy cotton fine-art papers are not automatically compatible with this printer.
3. Print one representative dark, colorful piece and one fine-line piece. Check shadows, gradients, neutral grays, fine lines, and ink handling after the manufacturer's drying interval.
4. Record the paper, driver media setting, quality setting, scale, and color-management choice. Avoid applying two competing color corrections. Preserve the full artwork and test the border against an actual frame/mat.
5. Sign the approved print, photograph it in natural light, then use that photograph in the external product listing. Do not imply a digital gallery preview is a photograph of the shipped object.

HP states that Instant Ink counts photo and text pages the same, rather than charging according to ink coverage. Include test sheets, spoiled prints, your subscription allocation, and any additional-page blocks in the actual cost per accepted print. Cheap ink does not by itself establish fade resistance.

## Illustrative per-order economics

These are placeholders to replace with invoices and a packed-mailer shipping quote. Labor is explicitly included. No monthly sales volume or profitability is assumed.

| One-print order | USD |
| --- | ---: |
| Print price | 35.00 |
| Shipping collected | 7.00 |
| Total collected, excluding tax | 42.00 |
| Paper, allocated ink, and spoilage allowance | -2.25 |
| Sleeve, backing, rigid mailer, and label | -1.75 |
| Postage allowance | -6.50 |
| Fees modeled at 8% of total + $0.30 | -3.66 |
| Labor: 15 minutes at $25/hour | -6.25 |
| Contribution after these costs | **21.59** |

That contribution is before equipment, fixed overhead, taxes, refunds, and unexpected replacements. The 8% model combines Ko-fi's published 5% shop fee with an illustrative 3% processor fee; actual processor terms differ. Fees can apply to shipping collected, so do not calculate them only on the artwork price. A bundled order shares packaging and postage but must be costed separately.

## Fulfillment

Santiago has chosen U.S. and international shipping. Use a small initial order cap and quote international destinations individually until actual packed costs and supported services are established. Weigh and measure one fully packed order before setting shipping. Use a protective sleeve, clean backing, and a rigid mailer; test resistance to bending and moisture. Photograph the packing method. Charge shipping separately and avoid an unverified flat international rate.

Set the production window only after timing the entire process: printing, drying, signing, packaging, correspondence, and mailing. Draft a clear replacement policy for damage and mistakes. Keep each order's product, quantity, payment confirmation, production status, and tracking reference in a private record outside this repository.

## Where to sell

Use this site as the portfolio and discovery page, with payment, shipping-address collection, and order records on an external shop. Ko-fi is a reasonable first option because the site already links Santiago's Ko-fi account and its shop supports physical products, shipping destinations, quantities, and variants. Link each print to its specific listing once the listing exists. Do not point a “Buy” button at an unconfigured shop or collect payment details on this static website.

Redbubble is an optional secondary channel for merchandise and fulfillment convenience. Its manufacturing/base-price model and tier-dependent fees make it less aligned with a signed, artist-fulfilled print offering. It does not remove the need to attract customers. Consider an external professional lab for larger sizes after demand is established rather than buying a larger printer immediately.

Other offers worth testing later: hand-embellished prints, a coordinated two-print set, original small works, digital art collections for personal use, music packs for game developers with clear usage terms, and paid original artwork/music licensing. Start the print shop with original designs; keep the retro label archive separate from this offering.

## Local proof files

Run `python prepare_print_proofs.py` to create four 300-PPI, letter-size PDF proofs in the ignored `_archive_print_proofs` folder. Print at **Actual Size / 100%**, single-sided, without borderless enlargement or fit-to-page scaling. The image area is bounded by 7.5 × 9 inches with its original proportions preserved, and no source image is enlarged. The lower margin leaves space for a real handwritten signature. Review physical proofs before fulfilling orders. These production files are not deployed or committed.

## Sources checked

- [HP ENVY 6055e specifications](https://www.hp.com/bd-en/products/printers/product-details/product-specifications/2100187685)
- [HP Premium Plus Satin letter-size paper](https://www.hp.com/us-en/shop/pdp/hp-premium-plus-soft-gloss-photo-paper-50-sht-letter-85-x-11-in)

- [HP Instant Ink billing and page counting](https://support.hp.com/us-en/document/ish_3259778-1993151-16)
- [Ko-fi shop: physical products and shipping](https://help.ko-fi.com/hc/en-us/articles/360009712917-Ko-fi-Shop-Sell-digital-physical-products)
- [Ko-fi fees](https://help.ko-fi.com/hc/en-us/articles/360002506494-Does-Ko-fi-take-a-fee)
- [Redbubble payment calculation and account fees](https://help.redbubble.com/hc/en-us/articles/202270799-How-is-my-payment-calculated)
- [Red River paper sampler options](https://www.redrivercatalog.com/samples/)
- [itch.io pricing and optional payments](https://itch.io/docs/creators/pricing)
- [GitHub Pages size and usage limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)

GitHub Pages publishes sites up to 1 GB and has a soft bandwidth limit of 100 GB/month. Its usage rules do not permit a site primarily devoted to e-commerce. Keep this site principally a portfolio and use a dedicated external service for the store; revisit hosting if commerce becomes the site's primary purpose.
