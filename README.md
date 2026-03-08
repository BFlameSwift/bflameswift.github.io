# Yu Li's Academic Homepage

This repository contains the source code for [https://bflameswift.github.io/](https://bflameswift.github.io/), a Jekyll-based academic homepage for Yu Li.

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
bundle exec jekyll serve -l -H localhost
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

## Acknowledgement

This project is based on [Academic Pages](https://academicpages.github.io/), with extensive customization for Yu Li's personal academic homepage.
