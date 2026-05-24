# Mawid marketing site

Static marketing site for [mawid.ai](https://mawid.ai). Bilingual (English at `/`, Arabic at `/ar/`).

## Structure

```
/                en homepage
/about/          about
/product/        product
/pricing/        pricing
/contact/        contact
/privacy/        privacy
/terms/          terms
/ar/             ar homepage (and mirror of all pages above under /ar/<page>/)
/assets/         shared CSS + JS
/404.html        404 page
/sitemap.xml
/robots.txt
```

## Tech

Plain HTML / CSS / JS. No build step. Hosted on Vercel — pushes to `main` auto-deploy.

The operator dashboard and customer booking flow live in a separate repo: [mawid](https://github.com/itsalizee/mawid).
