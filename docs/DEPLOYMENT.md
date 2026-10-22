# Cloudflare deployment

Target hostname: `virtuoso.ethanwu.me`. Custom-domain activation is pending authenticated access to the Cloudflare account managing `ethanwu.me`.

The app is entirely static; it needs no server, API key, database, or user-score storage. The self-hosted IBM Plex Mono fonts are licensed under the SIL Open Font License; see `web/fonts/OFL.txt`.

## Workers

The root `wrangler.jsonc` deploys the contents of `web/` as static assets. After signing into the correct Cloudflare account, run `npx wrangler deploy` from the repository root. Add `virtuoso.ethanwu.me` under the Worker's Settings → Domains & Routes → Custom Domain. Let Cloudflare create the subdomain record; do not replace unrelated `ethanwu.me` records.

## Pages direct upload

Create a Pages application called `virtuoso`, upload the contents of `web/` (or the prepared static ZIP), then add `virtuoso.ethanwu.me` in Custom domains. Select the existing `ethanwu.me` zone to create the required DNS record. Verify HTTPS and score analysis at the custom hostname before claiming deployment complete.

The existing private Sites publication remains available during the move. The requested Cloudflare-hosted portfolio deployment will be public when activated; score files still stay in the visitor's browser.
