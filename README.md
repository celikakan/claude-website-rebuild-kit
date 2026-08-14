# Claude Website-Rebuild Kit

Skill-Paket fuer den kompletten Website-Rebuild mit Claude Code.
Bereitgestellt von [DER KI BERATER](https://der-ki-berater.at).

## Installation (ein Befehl)

```bash
curl -fsSL https://raw.githubusercontent.com/celikakan/claude-website-rebuild-kit/main/install.sh | bash
```

Danach Claude Code neu starten. Start: `/website-rebuild`

Die vollstaendige Anleitung mit allen Phasen erhalten Sie als separates
Dokument von DER KI BERATER.

## Skills erweitern

Neue Zeile in `skills-manifest.txt` anhaengen, Install-Befehl erneut
ausfuehren. Das Script ist idempotent: Vorhandenes wird aktualisiert.

## Lizenz

Eigene Skills (`skills/`): MIT. Fremd-Skills werden bei der Installation
aus ihren Original-Repos geladen und behalten deren Lizenzen.
