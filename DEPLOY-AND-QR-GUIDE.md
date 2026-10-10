# Deploy + QR / AR / VR guide

AR, VR and the phone camera only work on a real **https** website (not inside a
chat preview). This takes ~3 minutes:

## 1. Put the site online (pick one)
**Netlify (easiest):** go to app.netlify.com/drop → drag the `frontend` folder onto the page.
You get `https://something.netlify.app`. (Or drag this whole folder: `netlify.toml` points at `frontend`.)

**GitHub Pages:** new repo → upload the contents of `frontend/` (use `standalone-single-file.html` renamed
to `index.html`, or `index.html` + `styles.css` + `app.js`) → Settings → Pages → Deploy from branch.

## 2. Tell the app your address (once)
Open your live site → click **📲 QR** → paste the address in "Your hosted website address".
(It is remembered in the browser. You can also hard-code it in `app.js` / the HTML: search `PUBLIC_SITE_URL`.)
If you open the *live* site itself, the address is filled in automatically.

## 3. Scan
Design your building → **📲 QR** → choose Outside / Inside / Walk / AR / VR → scan with the phone camera.
The phone opens a full-screen viewer showing exactly your design:
| Mode | What happens |
|---|---|
| Outside / Inside | drag to rotate, pinch to zoom |
| Walk | left joystick to walk, drag to look; walls & furniture block you |
| AR | Android Chrome: tap the detected floor to place it (real WebXR). iPhone/others: live camera + gyroscope, model floats in front of you |
| VR | Phone in a Cardboard headset (tap = walk), or Meta Quest browser (thumbstick to walk) |

## Good to know / limits
- The QR holds the design itself (no database). Very large designs (~60+ items) may not fit one QR — use the copy-link button.
- If you later change the catalog order in the code, QR codes printed earlier won't match.
- iPhone Safari has no WebXR AR; it uses the camera+gyro mode.
- Models are procedurally built (no photoreal scans).
