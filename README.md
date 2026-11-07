# Ethiopia Economic Atlas — Free News Monitor

A complete **standalone, embeddable** news module. It is NOT an ongoing Hostinger Horizons task. The visitor-facing page, its data file, and the RSS collector all live on GitHub Pages / GitHub Actions. **No paid news API, no API token, and no Horizons credits for routine news collection.**

## What you get

- Premium dark news site with searchable headlines, publisher/industry filters, dates and source links.
- Scheduled Python standard-library RSS/Atom collector (four runs per day, ~every six hours).
- Lightweight JSON output, no paid service or database.
- Compatible with a standalone tab or an iframe inside your existing Hostinger Horizons site.
- Does NOT republish full articles or images; headlines link readers to publishers.
- Source definitions in `feeds.json` so you can enable/disable publishers.

## Set up for $0 additional service charges

1. Create a **public** repository on [GitHub](https://github.com/new), e.g., `ethiopia-atlas-news`. Make it public if you wish to use GitHub Pages on GitHub Free.
2. Upload the **contents** of this folder to the repository, preserving the `.github/workflows/publish-news.yml` directory structure. GitHub's browser uploader accepts the individual files; uploading a ZIP file alone will not run it.
3. In repository **Settings → Pages → Build and deployment**, select **GitHub Actions** as the source.
4. In **Actions**, run **Refresh Ethiopia economic headlines and publish** using **Run workflow**. Confirm the workflow succeeds. A newly published repository may need Actions enabled first.
5. Open `https://YOUR-GITHUB-USERNAME.github.io/ethiopia-atlas-news/` (GitHub Pages URLs depend on repository name). The page should show articles after a successful permitted-feed collection.
6. Link the news page from Hostinger using a standard navigation link, or embed via iframe (code below). The one-time Horizons change may use build credits, but **scheduled collection does not use any Horizons credits**.

### Embed in the existing website

In a Horizons custom code/embed block **if supported**:

```html
<iframe
  src="https://YOUR-GITHUB-USERNAME.github.io/ethiopia-atlas-news/"
  title="Ethiopia Economic Atlas — Economic News"
  loading="lazy" referrerpolicy="strict-origin-when-cross-origin"
  style="width:100%;height:900px;border:0;border-radius:16px;background:#080f1b"
></iframe>
```

Or simply add a site navigation link titled "Economic News" opening the GitHub Pages address. Linking is more reliable if iframe blocks are not supported by your Horizons template. A standalone custom domain can be configured through GitHub Pages if desired.

## Essential editorial and legal checks

The sample feed list contains three **technically discoverable RSS endpoints**:

- `https://capitalethiopia.com/feed/`
- `https://newbusinessethiopia.com/feed/`
- `https://www.thereporterethiopia.com/feed/`

**RSS availability does not establish permission to use feed data in a public/commercial aggregation.** Verify each source's feed redistribution/usage terms and, if necessary, ask the publisher for permission to display linked headlines before public launch. Disable any source in `feeds.json` when use is not authorized. The collector uses only headline text, URL, publication date and publisher; it does not pull full articles or photographs.

The keyword filtering is deterministic, imperfect, and sometimes misses relevant stories; this is a news *monitor*, not an editorially curated wire.

## Cost and availability cautions

- GitHub Actions standard hosted runners in a **public** repository are currently free, but GitHub platform usage limits, anti-abuse policies and the free service terms still apply.
- GitHub Pages bandwidth/hosting policies apply. This is not literally unlimited hosting or uptime.
- Scheduled workflows are best effort, may be delayed and, on public repositories with 60 days of no activity, may be automatically disabled. Check occasionally and re-enable them if necessary.
- A blank news section until the first successful workflow run is intentional. **No fabricated stories are bundled.**
- Feed publishers may block automated requests, change feed URLs, or withdraw permissions.
- The source links direct visitors away from your site. This is by design for copyright safety.

## Files

- `site/index.html` — finished standalone interface, no build tool required.
- `site/news.json` — current data (empty until collector succeeds).
- `scripts/collect.py` — Python RSS collector (stdlib-only).
- `.github/workflows/publish-news.yml` — schedule + deployment.
- `feeds.json` — RSS sources and terms-review reminders.
- `tests/test_collector.py` — offline regression tests.

### Test locally

```bash
python -m unittest discover -s tests -v
python scripts/collect.py  # requires public network access; gracefully retains old data if feeds fail
cd site && python -m http.server 8000
```

Then open `http://localhost:8000` in a browser. Do not expect the sample JSON to contain actual news before a successful feed collection.
