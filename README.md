# FlightPlanPro
Static site (plain HTML/CSS/JS, no build step, no paid services).

## Deploy
1. Push this folder to a GitHub repo.
2. Cloudflare dashboard > Workers & Pages > Create > Pages > Connect to Git. Project name `flightplanpro`, framework preset *None*, build command empty, output directory `/`.
3. Site goes live at https://flightplanpro.pages.dev (if the name is free).

## Google Search Console (HTML tag method)
1. Add property > URL prefix > `https://flightplanpro.pages.dev/` > HTML tag.
2. Replace the placeholder in every page: `grep -rl PASTE_YOUR_GOOGLE_VERIFICATION_CODE . | xargs sed -i 's/PASTE_YOUR_GOOGLE_VERIFICATION_CODE/YOUR_CODE/'`
3. Deploy, click Verify, then submit `https://flightplanpro.pages.dev/sitemap.xml`.
(HTML file method also works: drop the `google*.html` file in the repo root.)

## Add a tool
Tools are defined in `build.py` (list `T`). Edit it, run `python3 build.py`, commit the output.
