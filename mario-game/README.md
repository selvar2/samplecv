# Super Jumper Bros 🍄

A classic Mario-style side-scrolling platformer that runs on **any smart
device** — old Android phones, iPhones, tablets, laptops, desktops — straight
from the browser. No installation, no app store, no dependencies.

## ▶ How to play

Just open `index.html` in any browser. That's it.

To serve it on your network (so phones can reach it):

```sh
# from the repo root, any of these works:
python -m http.server 8000          # Python 3
python -m SimpleHTTPServer 8000     # Python 2
npx http-server -p 8000             # Node
```

Then visit `http://<your-computer-ip>:8000/mario-game/` on the phone.

Or host the folder on any static host (GitHub Pages, Netlify, etc.).

## 🎮 Controls

| Action | Touch (phone/tablet) | Keyboard |
|--------|----------------------|----------|
| Move   | ◀ / ▶ buttons        | Arrow keys or A / D |
| Jump   | A button             | Space, ↑, W, Z or X |
| Start  | Tap anywhere         | Any key |

Hold jump longer to jump higher. Stomp enemies, grab coins, bump `?` blocks,
smash bricks, and reach the flag before the timer runs out. 3 lives.

## 📱 Backward compatibility (old Android phones)

The whole game is **one self-contained HTML file** built specifically so it
works on legacy devices:

- **Pure ES5 JavaScript** — no arrow functions, `let`/`const`, classes,
  template literals or promises, so the Android 2.3+ stock browser and old
  WebViews can parse it.
- **`requestAnimationFrame` polyfill** with `webkit`/`moz` prefixes and a
  `setTimeout` fallback for browsers that predate rAF.
- **Canvas 2D only** — supported since Android 2.x / iOS 3. No WebGL, no
  external images, no fonts, no CSS frameworks. All sprites are pixel art
  generated at runtime.
- **Fixed-timestep game loop** with frame-drop protection, so the game speed
  stays correct on slow single-core phones.
- **Capped devicePixelRatio (≤2)** to keep the canvas small enough for weak
  GPUs.
- **Touch controls** appear automatically on touch devices (multi-touch
  `touchstart`/`touchend`), with mouse and keyboard fallbacks for desktop.
- **Responsive letterboxed scaling** — fits any screen size and orientation,
  reacting to `resize`/`orientationchange`.
- **Sound is optional** — a tiny Web Audio synth wrapped in try/catch; on
  browsers without audio support the game simply plays silently instead of
  crashing.
- Works **fully offline** once the single file is on the device.

## 🏗 Tech notes

- Virtual resolution 256×224 (NES-like), scaled to the screen with image
  smoothing disabled for crisp pixels.
- Tile-based level (212×14) with axis-separated AABB collision.
- Original hand-made pixel art — inspired by the classics, not copied.
