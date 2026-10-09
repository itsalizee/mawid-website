Social preview images (`/og-image.png`, `/og-image-ar.png`, 1200×630).

Regenerate after editing `og.html`:

```bash
for L in en ar; do "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --window-size=1200,630 --virtual-time-budget=8000 --screenshot="og-$L.png" "file://$PWD/og.html#$L"; done
mv og-en.png ../../og-image.png && mv og-ar.png ../../og-image-ar.png
```
