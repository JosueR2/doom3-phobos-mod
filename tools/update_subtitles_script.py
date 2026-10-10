# -*- coding: utf-8 -*-
path = "src/script/phobos_subtitles_es.script"
with open(path, "r", encoding="latin-1") as f:
    content = f.read()

old_func = """void PhobosSetCanSkip(float enable) {
\tif (enable == 1) {
\t\tsys.setcvar("g_canSkip", "1");
\t\tif (sys.getcvar("g_subLang") == "spanish") {
\t\tsys.setcvar("g_subLangIsES", "1");
\t\t} else {
\t\tsys.setcvar("g_subLangIsES", "0");
\t\t}
\t} else {
\t\tsys.setcvar("g_canSkip", "0");
\t}
}"""

new_func = """void PhobosSetCanSkip(float canSkipState) {
\tif (canSkipState == 1) {
\t\tsys.setcvar("g_canSkip", "1");
\t\tif (sys.getcvar("g_subLang") == "spanish") {
\t\tsys.setcvar("g_subLangIsES", "1");
\t\t} else {
\t\tsys.setcvar("g_subLangIsES", "0");
\t\t}
\t} else {
\t\tsys.setcvar("g_canSkip", "0");
\t}
}"""

assert old_func in content, "old_func not found!"
content = content.replace(old_func, new_func, 1)

with open(path, "w", encoding="latin-1") as f:
    f.write(content)

print("Successfully replaced float enable with float canSkipState in phobos_subtitles_es.script!")
