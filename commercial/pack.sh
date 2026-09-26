#!/usr/bin/env bash
# Build midnight-geo-pro-v1.0.0.zip from this checkout + bundled citation research.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VER="${GEO_PRO_VERSION:-1.0.0}"
NAME="midnight-geo-pro-v${VER}"
DIST="${ROOT}/commercial/dist"
STAGE="$(mktemp -d)"
trap 'rm -rf "${STAGE}"' EXIT

mkdir -p "${STAGE}/${NAME}/commercial" "${STAGE}/${NAME}/skills" \
  "${STAGE}/${NAME}/research/ai-citation-patterns" "${DIST}"

cp "${ROOT}/LICENSE" "${ROOT}/LICENSE-COMMERCIAL.md" "${ROOT}/README.md" "${STAGE}/${NAME}/"
cp "${ROOT}/commercial/INSTALL.md" "${ROOT}/commercial/THANKS.md" \
  "${ROOT}/commercial/BUYER-JOURNEY.md" "${STAGE}/${NAME}/commercial/"
cp -R "${ROOT}/skills/." "${STAGE}/${NAME}/skills/"

CITE_SRC="${AI_CITATION_PATTERNS_ROOT:-${HOME}/projects/ai-citation-patterns}"
if [[ ! -f "${CITE_SRC}/README.md" ]]; then
  echo "missing ai-citation-patterns README at ${CITE_SRC}" >&2
  exit 1
fi
cp "${CITE_SRC}/README.md" "${CITE_SRC}/LICENSE" "${CITE_SRC}/CITATION.cff" \
  "${STAGE}/${NAME}/research/ai-citation-patterns/"

# Drop junk that should never ship
find "${STAGE}/${NAME}" -name '.DS_Store' -delete
find "${STAGE}/${NAME}" -name '.git' -prune -o -name '.git' -print

ZIP="${DIST}/${NAME}.zip"
rm -f "${ZIP}"
(cd "${STAGE}" && zip -qry "${ZIP}" "${NAME}")

echo "wrote ${ZIP}"
echo "--- counts ---"
skill_md=$(unzip -Z1 "${ZIP}" | grep -c '/skills/.*/SKILL.md$' || true)
cite=$(unzip -Z1 "${ZIP}" | grep -c 'ai-citation-patterns/README.md$' || true)
lic=$(unzip -Z1 "${ZIP}" | grep -c 'LICENSE-COMMERCIAL.md$' || true)
total=$(unzip -Z1 "${ZIP}" | wc -l | tr -d ' ')
echo "skill_md=${skill_md} cite_readme=${cite} commercial_license=${lic} total_files=${total}"
test "${skill_md}" -ge 15
test "${cite}" -ge 1
test "${lic}" -ge 1
