#!/usr/bin/env bash
# =====================================================================
# Claude Website-Rebuild Kit - One-Click-Installation
# DER KI BERATER - der-ki-berater.at
#
# Usage (one command, run from anywhere):
#   curl -fsSL https://raw.githubusercontent.com/celikakan/claude-website-rebuild-kit/main/install.sh | bash
#
# Safe to re-run: existing skills are updated, nothing else is touched.
# All skills are read from skills-manifest.txt - to add a skill, add a
# line there and re-run this script.
# =====================================================================
set -u

REPO_URL="https://github.com/celikakan/claude-website-rebuild-kit.git"
SKILLS_DIR="$HOME/.claude/skills"
MANIFEST="skills-manifest.txt"

ok()   { printf '  \033[32m[OK]\033[0m %s\n' "$1"; }
warn() { printf '  \033[33m[!]\033[0m %s\n' "$1"; }
fail() { printf '  \033[31m[X]\033[0m %s\n' "$1"; }

INSTALLED=0; UPDATED=0; FAILED=0
SUMMARY=""

note() { SUMMARY="${SUMMARY}$1\n"; }

echo ""
echo "=============================================="
echo "  Claude Website-Rebuild Kit - Installation"
echo "  DER KI BERATER"
echo "=============================================="
echo ""

# --- Preconditions ----------------------------------------------------
command -v git >/dev/null 2>&1 || { fail "git fehlt. Bitte zuerst installieren: https://git-scm.com"; exit 1; }
mkdir -p "$SKILLS_DIR"

# --- Locate the kit (clone when run via curl | bash) ------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"
if [ -f "$SCRIPT_DIR/$MANIFEST" ]; then
  KIT_DIR="$SCRIPT_DIR"
else
  KIT_DIR="$(mktemp -d)/kit"
  echo "Lade das Kit von GitHub ..."
  git clone --quiet --depth 1 "$REPO_URL" "$KIT_DIR" || { fail "Kit-Download fehlgeschlagen."; exit 1; }
fi
[ -f "$KIT_DIR/$MANIFEST" ] || { fail "Manifest nicht gefunden."; exit 1; }

CLONE_CACHE="$(mktemp -d)"
trap 'rm -rf "$CLONE_CACHE"' EXIT

# Copy one skill directory into ~/.claude/skills (install or update).
install_skill_dir() {
  local src="$1" name="$2" desc="$3"
  local dst="$SKILLS_DIR/$name"
  local verb="installiert"
  [ -d "$dst" ] && verb="aktualisiert"
  rm -rf "$dst"
  cp -R "$src" "$dst"
  find "$dst" -name '.DS_Store' -delete 2>/dev/null
  if [ "$verb" = "installiert" ]; then INSTALLED=$((INSTALLED+1)); else UPDATED=$((UPDATED+1)); fi
  ok "$name $verb"
  note "  $name - $desc"
}

# Shallow-clone a repo once per run, reuse for multiple skills.
clone_repo() {
  local url="$1"
  local key
  key="$(printf '%s' "$url" | shasum | cut -c1-12)"
  local dir="$CLONE_CACHE/$key"
  if [ ! -d "$dir" ]; then
    git clone --quiet --depth 1 "$url" "$dir" || return 1
  fi
  printf '%s' "$dir"
}

# Find the directory inside a repo that contains the skill.
find_skill_in_repo() {
  local repo="$1" name="$2"
  # 1) directory named exactly like the skill, containing SKILL.md
  local hit
  hit="$(find "$repo" -type d -name "$name" -not -path '*/node_modules/*' 2>/dev/null | while read -r d; do
    [ -f "$d/SKILL.md" ] && { printf '%s' "$d"; break; }
  done)"
  if [ -n "$hit" ]; then printf '%s' "$hit"; return 0; fi
  # 2) repo root itself is the skill
  if [ -f "$repo/SKILL.md" ]; then printf '%s' "$repo"; return 0; fi
  # 3) any SKILL.md whose frontmatter name matches
  find "$repo" -name SKILL.md -not -path '*/node_modules/*' 2>/dev/null | while read -r f; do
    if grep -qE "^name: *$name *$" "$f"; then printf '%s' "$(dirname "$f")"; break; fi
  done
}

echo ""
echo "Installiere Skills nach $SKILLS_DIR ..."
echo ""

# --- Process the manifest --------------------------------------------
while IFS='|' read -r typ quelle name desc; do
  case "$typ" in
    ''|\#*) continue ;;
  esac
  case "$typ" in
    custom)
      if [ -d "$KIT_DIR/$quelle" ]; then
        install_skill_dir "$KIT_DIR/$quelle" "$name" "$desc"
      else
        fail "$name: $quelle fehlt im Kit"; FAILED=$((FAILED+1))
      fi
      ;;
    github)
      repo="$(clone_repo "$quelle")" || { fail "$name: Repo nicht erreichbar ($quelle)"; FAILED=$((FAILED+1)); continue; }
      src="$(find_skill_in_repo "$repo" "$name")"
      if [ -n "$src" ]; then
        install_skill_dir "$src" "$name" "$desc"
      else
        fail "$name: im Repo nicht gefunden ($quelle)"; FAILED=$((FAILED+1))
      fi
      ;;
    plugin)
      if command -v claude >/dev/null 2>&1; then
        claude plugin marketplace add "$quelle" >/dev/null 2>&1
        if claude plugin install "$name" >/dev/null 2>&1; then
          ok "Plugin $name installiert"
          note "  $name (Plugin) - $desc"
        else
          warn "Plugin $name: bitte einmalig in Claude Code ausfuehren: /plugin install $name"
        fi
      else
        warn "claude-Befehl nicht gefunden. Plugin $name spaeter in Claude Code installieren: /plugin marketplace add $quelle && /plugin install $name"
      fi
      ;;
    npm)
      if command -v npm >/dev/null 2>&1; then
        if command -v "$name" >/dev/null 2>&1; then
          ok "CLI $name bereits vorhanden"
        elif npm install -g "$quelle" >/dev/null 2>&1; then
          ok "CLI $name installiert ($quelle)"
        else
          warn "CLI $quelle konnte nicht installiert werden. Manuell: npm install -g $quelle"
        fi
      else
        warn "npm fehlt (Node.js installieren: https://nodejs.org). Danach: npm install -g $quelle"
      fi
      ;;
    brew)
      # macOS/Linux: Homebrew. Windows (Git Bash): winget with mapped IDs.
      case "$quelle" in
        gh)     winget_id="GitHub.cli" ;;
        ffmpeg) winget_id="Gyan.FFmpeg" ;;
        yt-dlp) winget_id="yt-dlp.yt-dlp" ;;
        *)      winget_id="" ;;
      esac
      if command -v "$name" >/dev/null 2>&1; then
        ok "Werkzeug $name bereits vorhanden"
      elif command -v brew >/dev/null 2>&1; then
        if brew install "$quelle" >/dev/null 2>&1; then
          ok "Werkzeug $name installiert (brew)"
        else
          warn "Werkzeug $quelle konnte nicht installiert werden. Manuell: brew install $quelle"
        fi
      elif command -v winget >/dev/null 2>&1 && [ -n "$winget_id" ]; then
        if winget install --id "$winget_id" -e --silent --accept-package-agreements --accept-source-agreements >/dev/null 2>&1; then
          ok "Werkzeug $name installiert (winget). Hinweis: neues Terminal oeffnen, damit es gefunden wird."
        else
          warn "Werkzeug $name konnte nicht installiert werden. Manuell: winget install --id $winget_id"
        fi
      else
        warn "Mac/Linux: Homebrew installieren (https://brew.sh), dann: brew install $quelle. Windows: winget install --id ${winget_id:-$quelle}"
      fi
      ;;
    *)
      warn "Unbekannter Typ '$typ' im Manifest, Zeile uebersprungen"
      ;;
  esac
done < "$KIT_DIR/$MANIFEST"

# --- Summary ----------------------------------------------------------
echo ""
echo "=============================================="
echo "  Ergebnis: $INSTALLED neu installiert, $UPDATED aktualisiert, $FAILED Fehler"
echo "=============================================="
printf "$SUMMARY"
echo ""
if [ "$FAILED" -gt 0 ]; then
  echo "Es gab Fehler. Script einfach nochmal ausfuehren oder DER KI BERATER kontaktieren."
  exit 1
fi
echo "Fertig. Claude Code neu starten, dann stehen alle Skills bereit."
echo "Start des Rebuilds in Claude Code mit:  /website-rebuild"
