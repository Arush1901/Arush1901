# ARUSH / SYSTEMS OBSERVATORY
## Design blueprint · v1.0

### Concept
A digital observatory where software projects are presented as objects in orbit, and engineering skills as scientific instrumentation. The identity mixes restrained editorial astronomy with the clarity of a systems dashboard. This is **not** a real uptime monitor or live map of deployments; the graphics are a visual metaphor.

### Visual system

| Role | Hex | Purpose |
|---|---|---|
| Deep void | `#080D16` | Main canvas, rich near-black |
| Instrument navy | `#0C1420` | Secondary surfaces |
| Starlight ivory | `#EDE5D1` | Primary text |
| Observatory brass | `#C9B47C` | Identity, orbit markers, featured project |
| Atmospheric blue | `#80A7BF` | Secondary orbit/project accent |
| Slate | `#9FAEC0` | Supporting typography |
| Technical line | `#293848` | Thin strokes and borders |

**Typography:** System-native sans serif in the custom SVGs; large tightly tracked display name contrasted with small uppercase technical annotations. README body uses GitHub's native typography to retain accessibility and reliability. No downloaded font dependencies.

**Graphic rules:** Thin ellipses and instrument ticks; softened halos; sparse stars; no saturated neon, glossy 3D planets, or excessive animation. Prefer dark, spacious, composed layouts.

### Architecture of the page

1. **Hero** — 1200 × 500 SVG. Name on the left, technical orbit diagram on the right. Large enough to remain recognizable at typical GitHub profile widths.
2. **Introduction** — Native HTML/Markdown subtitle and quick links to real properties.
3. **Observer profile** — Short, human-first introduction with a readable YAML identity card.
4. **Objects in orbit** — Two custom SVG project cards linked to the existing site and the public repository. Real text below each graphic is accessible and searchable.
5. **Instrumentation** — 1200 × 252 SVG stack index with four equal tool groups.
6. **Mission notes** — Three concise points, not a fabricated timeline.
7. **Signal routing** — Verified GitHub profile and website only. Additional contact placeholders are hidden as comments until supplied.

### Art direction / micro-interactions

**Current release: static by design.** The chart suggests motion using diagonally rotated elliptical paths; it renders consistently on GitHub without scripts or third-party image generators. Future optional orbit motion could use CSS/SVG animation, but must degrade gracefully and respect reduced-motion preferences. GitHub's rendering and sanitization mean animation behavior should be tested on the live page; it is not relied upon here.

### Important engineering decisions

- No JS, custom README-level CSS, dynamic embeds, API keys, build jobs, or external image hosts.
- All art is local relative-path SVG (`assets/`), so cloning/pushing the repository deploys the complete theme.
- SVGs have `viewBox` and explicit accessible labels, and the README includes descriptive text.
- Image cards are wrapped in working links; project claims avoid invented live metrics.
- The two-card table is designed for desktop GitHub. On narrow screens, GitHub may horizontally scroll the table; the rest remains responsive.
- No badge asserting employment availability, which can be added after confirmation.

### Editable identity/content

- User / profile: `Arush1901` (confirmed via public GitHub profile).
- Display name: `Arush Maurya` (confirmed via public GitHub profile).
- Project 1: https://eclipsefantasy.art (user-provided project context).
- Project 2: https://github.com/Arush1901/AI-Commerce-Gateway (public repository).
- LinkedIn and email are **not filled in** because their exact URLs have not been provided.
- Confirm that all visible skill claims and project summaries match how you want to present yourself publicly.

### Files

```text
Arush1901/                 ← must match your username
├── README.md               ← automatically displayed on your GitHub profile
├── assets/
│   ├── observatory-hero.svg
│   ├── object-01-eclipse.svg
│   ├── object-02-commerce.svg
│   └── instrumentation.svg
└── DESIGN_BLUEPRINT.md     ← design notes; optional in the live repository
```

### Publishing

1. Create public repository named `Arush1901` on GitHub, or open the existing one.
2. Upload `README.md` and the whole `assets/` directory, preserving paths.
3. Commit to the repository default branch.
4. Visit https://github.com/Arush1901 and check desktop and phone widths. GitHub profile READMEs load automatically from a public same-name repository.

### Future upgrades (optional)

- Third object/card for an additional flagship project after its public details are confirmed.
- A separate light-mode asset variant using `<picture>` and `prefers-color-scheme`.
- Very slow SVG orbit motion if live GitHub tests confirm acceptable rendering.
- A tiny GitHub Action that updates genuine data in a separate summary — no fake counters.
