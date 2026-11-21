# pontos.org.au

Website of the Federation of Pontian Associations of Australia (Ομοσπονδία Ποντιακών Σωματείων Αυστραλίας).

Bilingual (English / Greek) static site. No dependencies: `python3 build.py` writes the site to `dist/`.

## Editing content
- **Volunteers:** sign in at <https://app.pagescms.org> with GitHub and open this repository. You can edit News, Events, Member associations and the Executive committee there. Each save rebuilds the site automatically within a minute or two.
- **Content files:** `content/news/*.json`, `content/events/*.json`, `content/associations.json`, `content/committee.json`.
- **Page layout and fixed text:** `build.py`. **Styles:** `src/assets/style.css`.

## Hosting (Cloudflare Pages)
- Build command: `python3 build.py`
- Build output directory: `dist`
- Production branch: `main`
- Custom domain: `pontos.org.au` (and `www.pontos.org.au`)
