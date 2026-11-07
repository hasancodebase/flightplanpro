# FlightPlanPro
Static site (plain HTML/CSS/JS, no build step, no paid services).

## Production domain
The production and canonical domain is https://flightplanpro.net. Cloudflare Pages also assigns the project hostname https://flightplanpro.pages.dev; configure a Cloudflare Bulk Redirect to send that hostname to the custom domain with a permanent 301 redirect, preserving paths and query strings.

## Deploy
1. Push this folder to the GitHub repo.
2. Cloudflare dashboard > Workers & Pages > select project `flightplanpro`; framework preset *None*, build command empty, output directory `/`.
3. The production site is https://flightplanpro.net.

## Google Search Console
1. In the correct Google account, verify the Domain property `flightplanpro.net` (DNS TXT) or URL-prefix property `https://flightplanpro.net/`.
2. Submit https://flightplanpro.net/sitemap.xml.
3. For the move from `https://flightplanpro.pages.dev`, ensure a permanent redirect is active first, then use Search Console's Change of Address tool if available for the old property.

## Add a tool
Tools are defined in `build.py` (list `T`). Edit it, run `python3 build.py`, commit the output.
