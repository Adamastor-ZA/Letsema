set -e
cd /tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/s16 && python3 u_build.py $1 2>&1 | tail -8
cd /tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/w16 && (cd build && rm -f ../build.docx && zip -XrDq ../build.docx .)
python3 /mnt/skills/public/docx/scripts/office/validate.py build.docx --original /home/user/Letsema/wesgro_v15_2/input/Unlocking_Tourism_Growth_Final_Report_DRAFT_v15.1_edited_1.docx --author "Claude (update pass)" 2>&1 | tail -4
python3 /tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/s16/st_accept.py && (cd acc && rm -f ../accepted.docx && zip -XrDq ../accepted.docx .)
soffice --headless --convert-to pdf --outdir /tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/w16 accepted.docx >/dev/null 2>&1
python3 /tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/s16/st_pages.py accepted.pdf
