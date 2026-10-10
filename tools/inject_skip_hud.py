# -*- coding: utf-8 -*-
import os

gui_path = r"src/guis/textmessagesystem.gui"
with open(gui_path, "r", encoding="latin-1") as f:
    content = f.read()

vars_chunk = """\tfloat "skip_visible" 0
\tfloat "is_spanish" 1

\teditDef SkipSync
\t{
\t\trect 0, 0, 0, 0
\t\tvisible 1
\t\tnoevents 1
\t\tcvar "g_canSkip"
\t\tliveUpdate 1
\t\ttext "gui::skip_visible"
\t}

\teditDef LangSync
\t{
\t\trect 0, 0, 0, 0
\t\tvisible 1
\t\tnoevents 1
\t\tcvar "g_subLangIsES"
\t\tliveUpdate 1
\t\ttext "gui::is_spanish"
\t}
"""

prompt_4_3 = """\t\twindowDef SkipPrompt_4_3
\t\t{
\t\t\trect 468, 12, 160, 24
\t\t\tvisible "gui::skip_visible"
\t\t\tbackcolor 0, 0, 0, 0.6
\t\t\tbordercolor 0.4, 0.4, 0.4, 0.8
\t\t\tbordersize 1
\t\t\tforceaspectwidth 640

\t\t\twindowDef SkipText_4_3_ES
\t\t\t{
\t\t\t\trect 0, 3, 160, 18
\t\t\t\tvisible "gui::is_spanish"
\t\t\t\ttext "[ X ] Saltar escena"
\t\t\t\tforecolor 0.9, 0.9, 0.9, 0.95
\t\t\t\ttextscale 0.22
\t\t\t\ttextalign 1
\t\t\t\tshadow 1
\t\t\t\tfont "fonts/an"
\t\t\t\tforceaspectwidth 640
\t\t\t}

\t\t\twindowDef SkipText_4_3_EN
\t\t\t{
\t\t\t\trect 0, 3, 160, 18
\t\t\t\tvisible 1 - "gui::is_spanish"
\t\t\t\ttext "[ X ] Skip scene"
\t\t\t\tforecolor 0.9, 0.9, 0.9, 0.95
\t\t\t\ttextscale 0.22
\t\t\t\ttextalign 1
\t\t\t\tshadow 1
\t\t\t\tfont "fonts/an"
\t\t\t\tforceaspectwidth 640
\t\t\t}
\t\t}
"""

prompt_16_9 = """\t\twindowDef SkipPrompt_16_9
\t\t{
\t\t\trect 677, 12, 160, 24
\t\t\tvisible "gui::skip_visible"
\t\t\tbackcolor 0, 0, 0, 0.6
\t\t\tbordercolor 0.4, 0.4, 0.4, 0.8
\t\t\tbordersize 1
\t\t\tforceaspectwidth 853

\t\t\twindowDef SkipText_16_9_ES
\t\t\t{
\t\t\t\trect 0, 3, 160, 18
\t\t\t\tvisible "gui::is_spanish"
\t\t\t\ttext "[ X ] Saltar escena"
\t\t\t\tforecolor 0.9, 0.9, 0.9, 0.95
\t\t\t\ttextscale 0.22
\t\t\t\ttextalign 1
\t\t\t\tshadow 1
\t\t\t\tfont "fonts/an"
\t\t\t\tforceaspectwidth 853
\t\t\t}

\t\t\twindowDef SkipText_16_9_EN
\t\t\t{
\t\t\t\trect 0, 3, 160, 18
\t\t\t\tvisible 1 - "gui::is_spanish"
\t\t\t\ttext "[ X ] Skip scene"
\t\t\t\tforecolor 0.9, 0.9, 0.9, 0.95
\t\t\t\ttextscale 0.22
\t\t\t\ttextalign 1
\t\t\t\tshadow 1
\t\t\t\tfont "fonts/an"
\t\t\t\tforceaspectwidth 853
\t\t\t}
\t\t}
"""

prompt_16_10 = """\t\twindowDef SkipPrompt_16_10
\t\t{
\t\t\trect 592, 12, 160, 24
\t\t\tvisible "gui::skip_visible"
\t\t\tbackcolor 0, 0, 0, 0.6
\t\t\tbordercolor 0.4, 0.4, 0.4, 0.8
\t\t\tbordersize 1
\t\t\tforceaspectwidth 768

\t\t\twindowDef SkipText_16_10_ES
\t\t\t{
\t\t\t\trect 0, 3, 160, 18
\t\t\t\tvisible "gui::is_spanish"
\t\t\t\ttext "[ X ] Saltar escena"
\t\t\t\tforecolor 0.9, 0.9, 0.9, 0.95
\t\t\t\ttextscale 0.22
\t\t\t\ttextalign 1
\t\t\t\tshadow 1
\t\t\t\tfont "fonts/an"
\t\t\t\tforceaspectwidth 768
\t\t\t}

\t\t\twindowDef SkipText_16_10_EN
\t\t\t{
\t\t\t\trect 0, 3, 160, 18
\t\t\t\tvisible 1 - "gui::is_spanish"
\t\t\t\ttext "[ X ] Skip scene"
\t\t\t\tforecolor 0.9, 0.9, 0.9, 0.95
\t\t\t\ttextscale 0.22
\t\t\t\ttextalign 1
\t\t\t\tshadow 1
\t\t\t\tfont "fonts/an"
\t\t\t\tforceaspectwidth 768
\t\t\t}
\t\t}
"""

prompt_21_9 = """\t\twindowDef SkipPrompt_21_9
\t\t{
\t\t\trect 940, 12, 160, 24
\t\t\tvisible "gui::skip_visible"
\t\t\tbackcolor 0, 0, 0, 0.6
\t\t\tbordercolor 0.4, 0.4, 0.4, 0.8
\t\t\tbordersize 1
\t\t\tforceaspectwidth 1120

\t\t\twindowDef SkipText_21_9_ES
\t\t\t{
\t\t\t\trect 0, 3, 160, 18
\t\t\t\tvisible "gui::is_spanish"
\t\t\t\ttext "[ X ] Saltar escena"
\t\t\t\tforecolor 0.9, 0.9, 0.9, 0.95
\t\t\t\ttextscale 0.22
\t\t\t\ttextalign 1
\t\t\t\tshadow 1
\t\t\t\tfont "fonts/an"
\t\t\t\tforceaspectwidth 1120
\t\t\t}

\t\t\twindowDef SkipText_21_9_EN
\t\t\t{
\t\t\t\trect 0, 3, 160, 18
\t\t\t\tvisible 1 - "gui::is_spanish"
\t\t\t\ttext "[ X ] Skip scene"
\t\t\t\tforecolor 0.9, 0.9, 0.9, 0.95
\t\t\t\ttextscale 0.22
\t\t\t\ttextalign 1
\t\t\t\tshadow 1
\t\t\t\tfont "fonts/an"
\t\t\t\tforceaspectwidth 1120
\t\t\t}
\t\t}
"""

assert 'rect\t0,0,1120,480\t\t\n' in content, "Root rect not found"
assert 'forceaspectwidth\t640\n\n\t\twindowDef TextMessages2' in content, "Desktop_4_3 hook not found"
assert 'forceaspectwidth\t853\n\n\t\twindowDef TextMessages2' in content, "Desktop_16_9 hook not found"
assert 'forceaspectwidth\t768\n\n\t\twindowDef TextMessages2' in content, "Desktop_16_10 hook not found"
assert 'forceaspectwidth\t1120\n\n\t\twindowDef TextMessages\n' in content, "Desktop_21_9 hook not found"

content = content.replace('rect\t0,0,1120,480\t\t\n', 'rect\t0,0,1120,480\t\t\n\n' + vars_chunk, 1)
content = content.replace('forceaspectwidth\t640\n\n\t\twindowDef TextMessages2', 'forceaspectwidth\t640\n\n' + prompt_4_3 + '\n\t\twindowDef TextMessages2', 1)
content = content.replace('forceaspectwidth\t853\n\n\t\twindowDef TextMessages2', 'forceaspectwidth\t853\n\n' + prompt_16_9 + '\n\t\twindowDef TextMessages2', 1)
content = content.replace('forceaspectwidth\t768\n\n\t\twindowDef TextMessages2', 'forceaspectwidth\t768\n\n' + prompt_16_10 + '\n\t\twindowDef TextMessages2', 1)
content = content.replace('forceaspectwidth\t1120\n\n\t\twindowDef TextMessages\n', 'forceaspectwidth\t1120\n\n' + prompt_21_9 + '\n\t\twindowDef TextMessages\n', 1)

with open(gui_path, "w", encoding="latin-1") as f:
    f.write(content)

print("Successfully injected Skip HUD elements into textmessagesystem.gui!")

