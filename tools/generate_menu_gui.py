import os

def create_game_button():
    os.makedirs(r"src/guis/mainmenu/Options", exist_ok=True)
    
    with open("GameButton_pak002.pd", "r", encoding="utf-8") as f:
        content = f.read()
        
    last_brace = content.rfind("}")
    if last_brace == -1:
        raise ValueError("Could not find closing brace in GameButton_pak002.pd")
        
    prefix = content[:last_brace].rstrip()
    
    extra = """

\t\twindowDef Divider10
\t\t{
\t\t\trect\t\t5, 186, 180, 1
\t\t\tbackground "guis/assets/border_hori"
\t\t\tmatcolor 0.1,0.28,0.44,.5
\t\t\tnoevents\t1
\t\t}

\t\twindowDef SubtitlesLangSetup
\t\t{
\t\t\trect\t\t3, 184, 380, 14

\t\t\twindowDef SubtitlesLangTitle
\t\t\t{
\t\t\t\trect\t\t0, 0, 100, 14
\t\t\t\ttext\t\t"Subtitle Language"
\t\t\t\tfont\t\t"fonts/bank"
\t\t\t\ttextscale\t0.15
\t\t\t\tforecolor 0.15,0.42,0.66,.8
\t\t\t}

\t\t\tchoiceDef SubtitlesLangSelector
\t\t\t{
\t\t\t\trect\t\t129, 0, 90, 14
\t\t\t\tchoices\t\t"English;Español"
\t\t\t\tvalues\t\t"english;spanish"
\t\t\t\tcvar\t\t"g_subLang"
\t\t\t\tchoiceType\t1
\t\t\t\tfont\t\t"fonts/bank"
\t\t\t\ttextscale\t0.15
\t\t\t\tforecolor 0.2,0.56,0.88,.8
\t\t\t}
\t\t}

\t\twindowDef Divider11
\t\t{
\t\t\trect\t\t5, 201, 180, 1
\t\t\tbackground "guis/assets/border_hori"
\t\t\tmatcolor 0.1,0.28,0.44,.5
\t\t\tnoevents\t1
\t\t}

\t\twindowDef SubtitlesSizeSetup
\t\t{
\t\t\trect\t\t3, 199, 380, 14

\t\t\twindowDef SubtitlesSizeTitle
\t\t\t{
\t\t\t\trect\t\t0, 0, 100, 14
\t\t\t\ttext\t\t"Subtitle Size"
\t\t\t\tfont\t\t"fonts/bank"
\t\t\t\ttextscale\t0.15
\t\t\t\tforecolor 0.15,0.42,0.66,.8
\t\t\t}

\t\t\tchoiceDef SubtitlesSizeSelector
\t\t\t{
\t\t\t\trect\t\t129, 0, 90, 14
\t\t\t\tchoices\t\t"Normal;Grande;Muy Grande"
\t\t\t\tvalues\t\t"0;1;2"
\t\t\t\tcvar\t\t"g_subSize"
\t\t\t\tchoiceType\t1
\t\t\t\tfont\t\t"fonts/bank"
\t\t\t\ttextscale\t0.15
\t\t\t\tforecolor 0.2,0.56,0.88,.8
\t\t\t}
\t\t}
}
"""
    new_pd = prefix + extra
    target_path = r"src/guis/mainmenu/Options/GameButton.pd"
    with open(target_path, "w", encoding="latin-1") as f:
        f.write(new_pd)
        
    with open(target_path, "r", encoding="latin-1") as f:
        txt = f.read()
    opens = txt.count('{')
    closes = txt.count('}')
    print(f"Created {target_path} successfully! Open: {opens}, Close: {closes}, Balanced: {opens == closes}")

if __name__ == "__main__":
    create_game_button()

