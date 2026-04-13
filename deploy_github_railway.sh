#!/usr/bin/env bash
# =============================================================================
# deploy_github_railway.sh
# Deployment helper: push ke GitHub dan/atau trigger deploy ke Railway
# tanpa perlu install Railway CLI secara global.
#
# Usage:
#   ./deploy_github_railway.sh [OPTIONS]
#
# Options:
#   --remote-url <url>   Set/update GitHub remote origin (git URL)
#   --push               Push branch saat ini ke GitHub (origin)
#   --deploy             Trigger deployment ke Railway via API
#   -h, --help           Tampilkan pesan bantuan ini
#
# Environment variables (alternatif dari flag):
#   GITHUB_REMOTE_URL    Sama dengan --remote-url
#   RAILWAY_TOKEN        Token API Railway (wajib untuk --deploy)
#   RAILWAY_SERVICE_ID   (Opsional) ID service Railway yang spesifik
#
# Contoh:
#   # Setup remote + push
#   ./deploy_github_railway.sh --remote-url git@github.com:USERNAME/REPO.git --push
#
#   # Deploy ke Railway (tanpa CLI global)
#   export RAILWAY_TOKEN="token_kamu"
#   ./deploy_github_railway.sh --deploy
#
#   # Push + deploy sekaligus via env vars
#   export GITHUB_REMOTE_URL="git@github.com:USERNAME/REPO.git"
#   export RAILWAY_TOKEN="token_kamu"
#   ./deploy_github_railway.sh --push --deploy
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Warna output
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
info()    { echo -e "${BLUE}[INFO]${RESET}  $*"; }
success() { echo -e "${GREEN}[OK]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
error()   { echo -e "${RED}[ERROR]${RESET} $*" >&2; }
die()     { error "$*"; exit 1; }

print_banner() {
  echo -e "${CYAN}${BOLD}"
  echo "╔══════════════════════════════════════════════════╗"
  echo "║        🚂  GitHub → Railway Deployer             ║"
  echo "║        Bot Sinau Inggris — deploy helper         ║"
  echo "╚══════════════════════════════════════════════════╝"
  echo -e "${RESET}"
}

usage() {
  sed -n '/^# Usage:/,/^# =====/p' "$0" | sed 's/^# \{0,3\}//' | head -n -1
  exit 0
}

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------
require_cmd() {
  command -v "$1" &>/dev/null || die "Command '$1' tidak ditemukan. Pastikan sudah terinstall."
}

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
OPT_REMOTE_URL="${GITHUB_REMOTE_URL:-}"
OPT_PUSH=false
OPT_DEPLOY=false

if [[ $# -eq 0 ]]; then
  print_banner
  warn "Tidak ada opsi yang diberikan. Gunakan --help untuk melihat cara pakai."
  echo ""
  usage
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --remote-url)
      [[ -n "${2:-}" ]] || die "--remote-url membutuhkan nilai URL."
      OPT_REMOTE_URL="$2"
      shift 2
      ;;
    --push)
      OPT_PUSH=true
      shift
      ;;
    --deploy)
      OPT_DEPLOY=true
      shift
      ;;
    -h|--help)
      print_banner
      usage
      ;;
    *)
      die "Opsi tidak dikenal: '$1'. Gunakan --help untuk melihat cara pakai."
      ;;
  esac
done

# ---------------------------------------------------------------------------
# Validasi: minimal satu aksi harus dipilih
# ---------------------------------------------------------------------------
if [[ "$OPT_PUSH" == false && "$OPT_DEPLOY" == false && -z "$OPT_REMOTE_URL" ]]; then
  die "Tidak ada aksi yang dipilih. Gunakan --push, --deploy, atau --remote-url."
fi

print_banner

# ---------------------------------------------------------------------------
# STEP 1 — Setup GitHub remote
# ---------------------------------------------------------------------------
setup_remote() {
  require_cmd git

  info "Mengatur GitHub remote origin → ${OPT_REMOTE_URL}"

  if git remote get-url origin &>/dev/null; then
    local current
    current=$(git remote get-url origin)
    if [[ "$current" == "$OPT_REMOTE_URL" ]]; then
      success "Remote origin sudah sesuai: ${OPT_REMOTE_URL}"
    else
      warn "Remote origin saat ini: ${current}"
      info "Mengubah remote origin ke: ${OPT_REMOTE_URL}"
      git remote set-url origin "$OPT_REMOTE_URL"
      success "Remote origin berhasil diperbarui."
    fi
  else
    git remote add origin "$OPT_REMOTE_URL"
    success "Remote origin berhasil ditambahkan: ${OPT_REMOTE_URL}"
  fi
}

# ---------------------------------------------------------------------------
# STEP 2 — Push ke GitHub
# ---------------------------------------------------------------------------
push_to_github() {
  require_cmd git

  # Pastikan ini adalah git repo
  git rev-parse --is-inside-work-tree &>/dev/null \
    || die "Direktori ini bukan git repository. Jalankan 'git init' terlebih dahulu."

  # Pastikan ada commit
  git rev-parse HEAD &>/dev/null \
    || die "Belum ada commit. Buat commit terlebih dahulu sebelum push."

  local branch
  branch=$(git rev-parse --abbrev-ref HEAD)
  info "Branch aktif: ${BOLD}${branch}${RESET}"

  # Pastikan remote origin tersedia
  git remote get-url origin &>/dev/null \
    || die "Remote 'origin' belum diset. Gunakan --remote-url untuk menambahkannya."

  local remote_url
  remote_url=$(git remote get-url origin)
  info "Push ke remote: ${remote_url}"

  # Cek apakah ada perubahan yang belum di-commit
  if ! git diff --quiet || ! git diff --cached --quiet; then
    warn "Ada perubahan yang belum di-commit:"
    git status --short
    echo ""
    warn "Lanjutkan push dengan kondisi working tree saat ini? (hanya committed changes yang akan di-push)"
  fi

  info "Menjalankan: git push origin ${branch} ..."
  if git push origin "$branch"; then
    success "Push ke GitHub berhasil! Branch '${branch}' sudah terupdate."
  else
    echo ""
    error "Push gagal. Kemungkinan penyebab:"
    echo "  • Belum ada akses ke repository (cek SSH key atau token)"
    echo "  • Branch remote sudah lebih maju (coba 'git pull --rebase' dulu)"
    echo "  • Repository belum dibuat di GitHub"
    die "Push ke GitHub gagal."
  fi
}

# ---------------------------------------------------------------------------
# STEP 3 — Deploy ke Railway via API (tanpa CLI global)
# ---------------------------------------------------------------------------
deploy_to_railway() {
  require_cmd curl

  local token="${RAILWAY_TOKEN:-}"
  [[ -n "$token" ]] || die "RAILWAY_TOKEN belum diset. Export dulu: export RAILWAY_TOKEN='token_kamu'"

  info "Menghubungi Railway API untuk trigger deployment..."

  # Ambil daftar project yang dimiliki token ini
  local projects_response
  projects_response=$(curl -sf \
    -X POST "https://backboard.railway.app/graphql/v2" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json" \
    -d '{"query":"{ me { projects { edges { node { id name } } } } }"}' \
    2>&1) || {
      echo ""
      error "Gagal menghubungi Railway API. Kemungkinan penyebab:"
      echo "  • RAILWAY_TOKEN tidak valid atau sudah expired"
      echo "  • Tidak ada koneksi internet"
      echo "  • Railway API sedang down"
      die "Koneksi ke Railway API gagal."
    }

  # Cek apakah response mengandung error autentikasi
  if echo "$projects_response" | grep -qi '"errors"'; then
    echo ""
    error "Railway API mengembalikan error:"
    echo "$projects_response" | grep -o '"message":"[^"]*"' | head -5
    die "Autentikasi Railway gagal. Pastikan RAILWAY_TOKEN valid."
  fi

  # Ekstrak project IDs dan names
  local project_ids project_names
  project_ids=$(echo "$projects_response" \
    | grep -o '"id":"[^"]*"' | sed 's/"id":"//;s/"//' | head -20 || true)
  project_names=$(echo "$projects_response" \
    | grep -o '"name":"[^"]*"' | sed 's/"name":"//;s/"//' | head -20 || true)

  if [[ -z "$project_ids" ]]; then
    warn "Tidak ada project Railway yang ditemukan untuk token ini."
    warn "Pastikan token memiliki akses ke project yang ingin di-deploy."
    die "Tidak ada project yang bisa di-deploy."
  fi

  # Jika RAILWAY_SERVICE_ID sudah diset, langsung deploy service tersebut
  local service_id="${RAILWAY_SERVICE_ID:-}"

  if [[ -n "$service_id" ]]; then
    info "Menggunakan RAILWAY_SERVICE_ID: ${service_id}"
    trigger_redeploy "$token" "$service_id"
    return
  fi

  # Ambil semua service dari semua project
  info "Mengambil daftar service dari Railway..."

  local all_services=""
  while IFS= read -r pid; do
    local svc_response
    svc_response=$(curl -sf \
      -X POST "https://backboard.railway.app/graphql/v2" \
      -H "Authorization: Bearer ${token}" \
      -H "Content-Type: application/json" \
      -d "{\"query\":\"{ project(id: \\\"${pid}\\\") { services { edges { node { id name } } } } }\"}" \
      2>/dev/null || echo "")
    if [[ -n "$svc_response" ]] && ! echo "$svc_response" | grep -qi '"errors"'; then
      all_services="${all_services}${svc_response}"$'\n'
    fi
  done <<< "$project_ids"

  local svc_ids
  svc_ids=$(echo "$all_services" \
    | grep -o '"id":"[^"]*"' | sed 's/"id":"//;s/"//' | grep -v '^$' || true)

  local svc_count
  svc_count=$(echo "$svc_ids" | grep -c '[a-z0-9]' || echo "0")

  if [[ "$svc_count" -eq 0 ]]; then
    warn "Tidak ada service yang ditemukan di project Railway kamu."
    die "Tidak ada service yang bisa di-deploy."
  fi

  if [[ "$svc_count" -eq 1 ]]; then
    service_id=$(echo "$svc_ids" | tr -d '[:space:]')
    info "Ditemukan 1 service, langsung deploy: ${service_id}"
    trigger_redeploy "$token" "$service_id"
  else
    # Lebih dari 1 service — tampilkan daftar dan minta pilihan
    echo ""
    warn "Ditemukan ${svc_count} service. Set RAILWAY_SERVICE_ID untuk memilih service spesifik."
    echo ""
    echo -e "${BOLD}Daftar service yang tersedia:${RESET}"
    local i=1
    while IFS= read -r sid; do
      [[ -z "$sid" ]] && continue
      echo "  ${i}. ${sid}"
      ((i++))
    done <<< "$svc_ids"
    echo ""
    echo -e "Contoh: ${CYAN}export RAILWAY_SERVICE_ID=\"<id-service>\"${RESET}"
    die "Pilih service dengan RAILWAY_SERVICE_ID lalu jalankan ulang."
  fi
}

trigger_redeploy() {
  local token="$1"
  local svc_id="$2"

  info "Trigger redeploy untuk service: ${svc_id}"

  local deploy_response
  deploy_response=$(curl -sf \
    -X POST "https://backboard.railway.app/graphql/v2" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"mutation { serviceInstanceRedeploy(serviceId: \\\"${svc_id}\\\") }\"}" \
    2>&1) || {
      error "Gagal mengirim request redeploy ke Railway."
      die "Redeploy gagal."
    }

  if echo "$deploy_response" | grep -qi '"errors"'; then
    echo ""
    error "Railway API mengembalikan error saat redeploy:"
    echo "$deploy_response" | grep -o '"message":"[^"]*"' | head -5
    echo ""
    echo -e "${YELLOW}Tips:${RESET}"
    echo "  • Pastikan service sudah pernah di-deploy sebelumnya"
    echo "  • Cek apakah token memiliki permission 'Deploy' di project"
    die "Redeploy Railway gagal."
  fi

  success "Deployment berhasil di-trigger di Railway! 🚀"
  echo ""
  info "Pantau progress deploy di: ${CYAN}https://railway.app/dashboard${RESET}"
}

# ---------------------------------------------------------------------------
# Eksekusi berdasarkan flag
# ---------------------------------------------------------------------------

# Setup remote jika --remote-url diberikan
if [[ -n "$OPT_REMOTE_URL" ]]; then
  echo ""
  echo -e "${BOLD}── STEP: Setup GitHub Remote ──────────────────────${RESET}"
  setup_remote
fi

# Push ke GitHub
if [[ "$OPT_PUSH" == true ]]; then
  echo ""
  echo -e "${BOLD}── STEP: Push ke GitHub ───────────────────────────${RESET}"
  push_to_github
fi

# Deploy ke Railway
if [[ "$OPT_DEPLOY" == true ]]; then
  echo ""
  echo -e "${BOLD}── STEP: Deploy ke Railway ────────────────────────${RESET}"
  deploy_to_railway
fi

echo ""
success "Semua langkah selesai. ✅"
