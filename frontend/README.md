MOON AI Frontend (Phase 1)

This frontend is a Vite + React + TypeScript project scaffolded to integrate with the MOON AI backend. It includes Tailwind CSS and an Electron integration scaffold.

Getting started (after installing dependencies):

1. Install dependencies:
   npm install

2. Run dev mode (web):
   npm run dev

3. Run Electron dev (requires electron and concurrently):
   npm run electron:dev

Project structure (initial):

src/
  components/
    ui/
      Button.tsx
  layouts/
    MainLayout.tsx
  main.tsx
  App.tsx

electron/
  main.ts
  preload.ts

Configuration files:
  vite.config.ts, tsconfig.json, tailwind.config.cjs, postcss.config.cjs

Next steps:
- Run `npm install` to install declared deps
- Add app icons and electron build scripts
- Wire auth and API clients in src/services
