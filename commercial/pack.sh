#!/usr/bin/env bash
# Build midnight-geo-pro-v1.2.0.zip from this checkout + bundled citation research.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VER="${GEO_PRO_VERSION:-1.2.0}"
NAME="midnight-geo-pro-v${VER}"
DIST="${ROOT}/commercial/dist"
STAGE="$(mktemp -d)"
trap 'rm -rf "${STAGE}"' EXIT

node "${ROOT}/scripts/generate-staff.mjs"

mkdir -p "${STAGE}/${NAME}/commercial" "${STAGE}/${NAME}/skills" \
  "${STAGE}/${NAME}/research/ai-citation-patterns" \
  "${STAGE}/${NAME}/operator-evidence" \
  "${STAGE}/${NAME}/chatgpt-probe-harness" \
  "${STAGE}/${NAME}/staff-bundles" "${DIST}"

cp "${ROOT}/LICENSE" "${ROOT}/LICENSE-COMMERCIAL.md" "${ROOT}/README.md" \
  "${ROOT}/SUPPORT.md" "${ROOT}/MANIFEST.md" "${STAGE}/${NAME}/"
cp "${ROOT}/commercial/INSTALL.md" "${ROOT}/commercial/THANKS.md" \
  "${ROOT}/commercial/BUYER-JOURNEY.md" "${STAGE}/${NAME}/commercial/"
cp -R "${ROOT}/skills/." "${STAGE}/${NAME}/skills/"
cp -R "${ROOT}/operator-evidence/." "${STAGE}/${NAME}/operator-evidence/"
cp -R "${ROOT}/chatgpt-probe-harness/." "${STAGE}/${NAME}/chatgpt-probe-harness/"
cp -R "${ROOT}/staff-bundles/." "${STAGE}/${NAME}/staff-bundles/"

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
support=$(unzip -Z1 "${ZIP}" | grep -c '/SUPPORT.md$' || true)
evidence=$(unzip -Z1 "${ZIP}" | grep -c 'operator-evidence/README.md$' || true)
harness=$(unzip -Z1 "${ZIP}" | grep -c 'chatgpt-probe-harness/PROTOCOL.md$' || true)
staff=$(unzip -Z1 "${ZIP}" | grep -c 'staff-bundles/roster.json$' || true)
hermes_dist=$(unzip -Z1 "${ZIP}" | grep -c 'staff-bundles/hermes/.*/distribution.yaml$' || true)
grok=$(unzip -Z1 "${ZIP}" | grep -c 'staff-bundles/grok/bot-cards.md$' || true)
echo "skill_md=${skill_md} cite_readme=${cite} commercial_license=${lic} support=${support} evidence=${evidence} harness=${harness} staff_roster=${staff} hermes_dist=${hermes_dist} grok_cards=${grok} total_files=${total}"
test "${skill_md}" -ge 15
test "${cite}" -ge 1
test "${lic}" -ge 1
test "${support}" -ge 1
test "${evidence}" -ge 1
test "${harness}" -ge 1
test "${staff}" -ge 1
test "${hermes_dist}" -eq 9
test "${grok}" -ge 1
