# Yu Li's Academic Homepage

This repository contains the source code for Yu Li's Jekyll-based academic homepage at [me.bflame.top](https://me.bflame.top/), with [GitHub Pages](https://bflameswift.github.io/) retained as a separate mirror.

The site is built on top of Academic Pages and has been customized into a single-page personal website with section-based navigation, a customized sidebar, publication badges, conference logos, and visitor counters.

## Current Site Content

The homepage currently includes:

- About Me
- Research Interests
- News
- Education
- Research Experiences
- Selected Publications
- Academic Services
- Contact
- Visitor Counter

The sidebar currently includes:

- Profile photo
- Location
- Email
- Google Scholar
- GitHub
- WeChat QR preview

## Main Customizations

Compared with the upstream Academic Pages template, this site currently uses:

- Single-page anchor navigation instead of multi-page profile navigation
- Customized homepage content in `_pages/about.md`
- Custom styling in `assets/css/main.scss`
- SVG logos for PKU, BUAA, MSRA, NeurIPS, and AAAI
- Publication badges for GitHub, GitHub stars, and Hugging Face
- Visitor statistics via Busuanzi and ClustrMaps

## Repository Structure

The most important files for daily editing are:

- `_pages/about.md`: homepage content
- `_config.yml`: site metadata, sidebar profile, analytics, social links
- `_data/navigation.yml`: top navigation items
- `assets/css/main.scss`: homepage and sidebar styling
- `_includes/author-profile.html`: custom sidebar rendering
- `_includes/head/custom.html`: favicon and head-level custom tags
- `images/`: avatars, logos, QR codes, favicon assets

## Local Development

This repository is intended to be edited and previewed locally without Docker.

### Requirements

- Ruby
- Bundler
- Node.js

### Install Dependencies

```bash
bundle install
```

If you hit gem permission issues, install gems into the local project directory:

```bash
bundle config set --local path 'vendor/bundle'
bundle install
```

### Run Locally

```bash
scripts/serve-local.sh
```

Then open:

```text
http://localhost:4000
```

If you edit `_config.yml`, stop and restart the local server.

## Content Update Notes

Common edits are straightforward:

- Update biography, news, education, experiences, publications, and contact information in `_pages/about.md`
- Update sidebar identity and links in `_config.yml`
- Replace images and SVG assets in `images/`
- Adjust layout and presentation in `assets/css/main.scss`

## Deployment

### JD Cloud

Build the custom-domain version with the overlay configuration:

```bash
bundle exec jekyll build --config _config.yml,_config_jdcloud.yml --destination local/me-bflame-build
```

The overlay sets the canonical domain and the ICP footer. The generated output is ignored by Git. Only generated site files should be uploaded, never the repository or its local dependencies.

The Nginx virtual host serves `/var/www/me.bflame.top/current`, pointing to a versioned directory under `/var/www/me.bflame.top/releases/`. The configuration is `/etc/nginx/conf.d/me.bflame.top.conf`. Deploy a fresh release directory, verify its files, switch the `current` symlink, and check the public homepage and assets. Preserve the previous release for rollback. Configuration updates require a backup, `nginx -t`, reload, and public verification.

TLS uses the existing server Certbot installation, a separate `me.bflame.top` certificate, HTTP webroot `/var/www/letsencrypt`, and the existing renewal timer and Nginx reload hook. Check renewal with `certbot renew --cert-name me.bflame.top --dry-run`.

The initial deployment on 2026-10-10 uses release `20261010-initial`. DNS is an A record for `me`, default route, TTL 600 seconds. Backups and deployment candidates live under `/var/www/me.bflame.top/backups/20261010-initial/` and `/var/www/me.bflame.top/staging/`. The hostname has its own virtual host and certificate; existing apex and other services retain their configuration.

GitHub pushes do not automatically update the JD Cloud release; build and deploy it separately after content changes.

### GitHub Pages mirror

GitHub Pages retains the site content but redirects visitors to `https://me.bflame.top/`, preserving the path, query and fragment when JavaScript is available. A no-JavaScript refresh and a manual link are also provided. `_config_jdcloud.yml` disables this behavior for the JD Cloud build, preventing a redirect loop. No GitHub custom-domain binding or DNS change is needed.

The `Backup` branch preserves the GitHub Pages version from before this migration (`0b07c05`). All earlier commits remain in history. To stop redirecting, set `github_pages_redirect_to: false` in `_config.yml` and rebuild/publish GitHub Pages; restoring the whole backup is unnecessary for that change.

This site is deployed with GitHub Pages from this repository:

- Repository: `BFlameSwift/bflameswift.github.io`
- URL: `https://bflameswift.github.io/`

After content changes:

```bash
git add .
git commit -m "Your commit message"
git push origin master
```

Once GitHub Pages finishes deploying, the live site will update automatically.

## Visitor history

`_data/visitor_history.yml` preserves the 2026-10-10 Busuanzi response for the former GitHub domain: 1,608 site page views and 879 reported site visitors. This is a dated provider snapshot; diagnostic requests may affect the count. The new domain is counted separately. The JD Cloud footer adds the archived page-view baseline to live new-domain page views; the archival date and explanation remain in this documentation rather than the public page. Visitor counts remain domain-specific because the same visitor may appear on both domains.

The legacy ClustrMaps widget identifier is retained in the archive and source. Its HTTPS endpoint failed validation during migration, so the JD overlay temporarily disables that widget. This preserves its configuration, but does not constitute an export or successful recovery of the map provider's historical data. No provider account or historical data was reset.

Recovery checks on 2026-10-10: Google public DNS and the server resolver returned `127.0.0.1` for the old hostname; the original image hostname `www.clustrmaps.com` also resolves to loopback. Git history recovered the original detail URL, `https://clustrmaps.com/site/1c9ad`, from commit `c5bcf6b`. Reusing the widget identifier or short identifier at the candidate MapMyVisitors service returned 404; continuity of accounts/data is unverified. The Internet Archive availability endpoint reported no snapshot for the exact widget URL; subsequent detail/image archive checks were rate-limited. A bounded Chrome history search found no matching links. No replacement widget was created. Map history cannot currently be retrieved through these inspected endpoints; a provider-side recovery or an owner-held export remains necessary.

## Daily page views

The JD deployment publishes `/stats/daily.json` from a dedicated Nginx date-only log, starting on 2026-10-12. It counts successful HTML GET requests (200/304), excludes assets, empty user agents and common bot/tool user agents, and stores no client IP, URL, query or user agent in this dedicated log. It is a page-request metric, not unique visitors, and differs from Busuanzi's browser-based cumulative metric. Earlier days have no data and render as a dash; the first day is partial.

`scripts/daily-stats/aggregate.py` retains private historical aggregates under `/var/lib/me-bflame-stats/history.json`, handles existing log rotation, and atomically publishes the last seven days under `/var/www/me.bflame.top/shared/stats/daily.json`. The `me-daily-stats.timer` refreshes every five minutes. Shared stats are independent of versioned site releases; content deployment must preserve the JSON alias and both access-log directives in the dedicated virtual host. The server's Nginx clock is UTC+8; keep it aligned with the displayed timezone.

Source configs live under `scripts/daily-stats/` and are excluded from generated public files. Rollback configuration is under `/var/www/me.bflame.top/backups/20261012-daily/`; disable the scoped timer and restore the previous dedicated vhost if retiring this feature. Ordinary pre-existing server access logging remains unchanged.

## Acknowledgement

This project is based on [Academic Pages](https://academicpages.github.io/), with extensive customization for Yu Li's personal academic homepage.
