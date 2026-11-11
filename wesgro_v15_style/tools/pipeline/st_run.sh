set -e
cd /tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/scripts && python3 st_build.py $1 2>&1 | tail -6
cd /tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/wst && (cd build && rm -f ../build.docx && zip -XrDq ../build.docx .)
python3 /mnt/skills/public/docx/scripts/office/validate.py build.docx --original /home/user/Letsema/wesgro_v15_style/input/Unlocking_Tourism_Growth_Final_Report_DRAFT_v15.1.docx --author "Claude (style edit)" 2>&1 | tail -4
python3 /tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/scripts/st_accept.py && (cd acc && rm -f ../accepted.docx && zip -XrDq ../accepted.docx .)
soffice --headless --convert-to pdf --outdir /tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/wst accepted.docx >/dev/null 2>&1
python3 /tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/scripts/st_pages.py accepted.pdf
