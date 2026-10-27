# Andrew's Cyber Brief

## 1. What this changes
Alexa reads static JSON from GitHub Pages. A GitHub Actions workflow fetches your existing Google Apps Script feed twice hourly, validates it, and deploys it. Google Sheets and Apps Script remain the upstream publishing source; Alexa no longer waits for Apps Script during playback. This project does not generate news or independently verify report claims. Hosting changes cannot guarantee Alexa playback.

## 2. Set up GitHub
Create a public repository named `andrews-cyber-brief` with default branch `main`. Extract this ZIP and upload its contents into the repository root. Include `.github/workflows/publish.yml`; a leading-dot folder may be hidden or omitted by browser uploads, so create that exact file using GitHub's Add file > Create new file if necessary. Keep `docs`, `scripts` and `source-url.txt` at the root.

Go to Settings > Pages > Build and deployment > Source and select GitHub Actions. Go to Actions > Refresh and publish briefing > Run workflow. Wait for a green successful deployment. The workflow run supplies your actual Pages address. Schedules can be delayed and GitHub can disable scheduled workflows after prolonged repository inactivity. Check Actions if updates stop.

## 3. Connect and test Alexa
First open `https://YOUR-USERNAME.github.io/andrews-cyber-brief/test.json` and verify it displays JSON. In your existing development skill, edit Andrew's Cyber Brief, replace the Feed URL with this test address, leave Text selected, and Save. Allow up to 30 minutes for Alexa refresh, then request your flash briefing. If the short test plays, switch the URL to `https://YOUR-USERNAME.github.io/andrews-cyber-brief/briefing.json`, save and allow another refresh. Keep the original Apps Script URL for rollback. Do not add a second feed.

If both GitHub feeds are skipped, hosting has not resolved the fault: investigate Amazon account, region, skill activation and Alexa behaviour. GitHub URLs here are templates, not deployed addresses.

## 4. Updates and failure handling
Each run fetches the upstream feed with a 90-second timeout. Empty feeds, missing fields, duplicate IDs, old or future dates, oversized text, invalid JSON and audio streams block deployment. A failed refresh leaves the previous successful Pages deployment in place. Publication dates are preserved, never artificially renewed. Alexa ignores briefing items older than seven days. The separate diagnostic feed has fresh test dates on successful builds and must not remain your production feed.

The committed briefing.json is an initial snapshot; scheduled builds publish refreshed files directly as Pages artifacts, without committing generated changes to this repository. Review the Pages endpoint for the current published version. To change the upstream source, edit source-url.txt. No API tokens or Google credentials are required because the source is public. Public Pages content is accessible to everyone. No Amazon or GitHub account changes have been made by preparing this package.
