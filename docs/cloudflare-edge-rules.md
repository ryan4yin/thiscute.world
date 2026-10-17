# Cloudflare Edge Rules

Production is **GitHub Pages behind Cloudflare**, not Vercel. The files in this repository
cannot set response headers or redirect requests by hostname on GitHub Pages, so the rules
below live in the Cloudflare dashboard. `vercel.json` is kept for a fallback Vercel
deployment, but it does not affect the current production site.

## Redirect Rule

Create a **Rules → Redirect Rules** rule for the legacy domains and `www`:

```txt
(http.host eq "www.thiscute.world") or
(http.host eq "writefor.fun") or
(http.host eq "www.writefor.fun") or
(http.host eq "ryan4yin.space") or
(http.host eq "www.ryan4yin.space")
```

- Type: **Dynamic**
- Target URL: `concat("https://thiscute.world", http.request.uri.path)`
- Status code: `308`
- Preserve query string: enabled

## Response Headers

Create a **Rules → Transform Rules → Modify Response Header** rule for all incoming
requests:

```txt
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: DENY
Permissions-Policy: camera=(), microphone=(), geolocation=()
Content-Security-Policy-Report-Only: default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://platform.twitter.com https://utteranc.es; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://*.algolia.net https://*.algolianet.com https://*.google-analytics.com https://*.googletagmanager.com; frame-src https://utteranc.es https://platform.twitter.com https://player.bilibili.com; media-src 'self' https:; object-src 'none'; base-uri 'self'; form-action 'self'
```

`X-Content-Type-Options` and `Referrer-Policy` are already set upstream.

## Verify

```bash
curl -sS -o /dev/null -D - https://www.thiscute.world/ | grep -i location
curl -sS -o /dev/null -D - https://thiscute.world/ | grep -iE 'strict-transport|x-frame|permissions-policy|content-security'
```
