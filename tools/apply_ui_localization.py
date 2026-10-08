import os

gui_root = r"E:\MisApps\Reverse\doom3phobos\src\guis"

def update_file(rel_path, replacements):
    full_path = os.path.join(gui_root, rel_path)
    with open(full_path, "r", encoding="latin-1") as f:
        content = f.read()
    for target, replacement in replacements:
        if target not in content:
            print(f"Warning: target '{target}' not found in {rel_path}")
        content = content.replace(target, replacement)
    with open(full_path, "w", encoding="latin-1") as f:
        f.write(content)
    print(f"Updated {rel_path}")

def run():
    # 1. MainButtons.pd
    update_file("mainmenu/MainButtons.pd", [
        ('text "NEW GAME"', 'text "gui::txt_newgame"'),
        ('text "LOAD GAME"', 'text "gui::txt_loadgame"'),
        ('text "SAVE GAME"', 'text "gui::txt_savegame"'),
        ('text "OPTIONS"', 'text "gui::txt_options"'),
        ('text "END GAME"', 'text "gui::txt_endgame"'),
        ('text "BACK TO GAME"', 'text "gui::txt_returngame"'),
        ('text "EXIT GAME"', 'text "gui::txt_exitgame"')
    ])

    # 2. OptionsMenu tabs
    update_file("mainmenu/Options/ControlsButton.pd", [
        ('text "Controls"', 'text "gui::txt_tab_controls"')
    ])
    
    # DefaultsButton.pd
    update_file("mainmenu/Options/DefaultsButton.pd", [
        ('text "Defaults"', 'text "gui::txt_tab_defaults"')
    ])

    # GameButton.pd
    # We also inject the Language and Size controls
    game_path = os.path.join(gui_root, "mainmenu/Options/GameButton.pd")
    with open(game_path, "r", encoding="latin-1") as f:
        game_content = f.read()

    game_content = game_content.replace('text "Game"', 'text "gui::txt_tab_game"')
    game_content = game_content.replace('text\t\t"Game Settings"', 'text\t\t"gui::txt_gamesettings"')
    game_content = game_content.replace('text\t\t"Show Subtitles"', 'text\t\t"gui::txt_subtitles"')

    # Inject SubtitlesLangSetup & SubtitlesSizeSetup at the end before closing bracket of GamePanel
    lang_size_block = """\t\twindowDef Divider10
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
\t\t\t\ttext\t\t"gui::txt_lang_label"
\t\t\t\tfont\t\t"fonts/bank"
\t\t\t\ttextscale\t0.15
\t\t\t\tforecolor 0.15,0.42,0.66,.8
\t\t\t}

\t\t\tchoiceDef SubtitlesLangSelector
\t\t\t{
\t\t\t\trect\t\t129, 0, 90, 14
\t\t\t\tchoices\t\t"ENGLISH;ESPA\xd1OL"
\t\t\t\tvalues\t\t"english;spanish"
\t\t\t\tcvar\t\t"g_subLang"
\t\t\t\tchoiceType\t1
\t\t\t\tfont\t\t"fonts/bank"
\t\t\t\ttextscale\t0.15
\t\t\t\tforecolor 0.2,0.56,0.88,.8

\t\t\t\tonAction {
\t\t\t\t\tset "cmd" "play guisounds_clicksonar2";
\t\t\t\t\tnamedEvent "Desktop" "UpdateLanguage";
\t\t\t\t}
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
\t\t\t\ttext\t\t"gui::txt_size_label"
\t\t\t\tfont\t\t"fonts/bank"
\t\t\t\ttextscale\t0.15
\t\t\t\tforecolor 0.15,0.42,0.66,.8
\t\t\t}

\t\t\tchoiceDef SubtitlesSizeSelector
\t\t\t{
\t\t\t\trect\t\t129, 0, 90, 14
\t\t\t\tchoices\t\t"Normal;Grande;Muy Grande"
\t\t\t\tvalues\t\t"0.275;0.35;0.43"
\t\t\t\tcvar\t\t"g_subSize"
\t\t\t\tchoiceType\t1
\t\t\t\tfont\t\t"fonts/bank"
\t\t\t\ttextscale\t0.15
\t\t\t\tforecolor 0.2,0.56,0.88,.8
\t\t\t}
\t\t}
"""
    # Replace closing brace of GamePanel
    # The last brace of GameButton.pd closes GamePanel
    idx = game_content.rfind("}")
    game_content = game_content[:idx] + lang_size_block + "}\n"
    with open(game_path, "w", encoding="latin-1") as f:
        f.write(game_content)
    print("Updated mainmenu/Options/GameButton.pd")

    # VideoButton.pd
    update_file("mainmenu/Options/VideoButton.pd", [
        ('text "Video"', 'text "gui::txt_tab_video"'),
        ('text\t\t"Video Settings"', 'text\t\t"gui::txt_videosettings"'),
        ('text\t\t"Screen Width"', 'text\t\t"gui::txt_screenwidth"'),
        ('text\t\t"Screen Height"', 'text\t\t"gui::txt_screenheight"'),
        ('text\t\t"Aspect Ratio"', 'text\t\t"gui::txt_aspectratio"'),
        ('text "Restart Video"', 'text "gui::txt_restartvideo"'),
        ('text\t\t"Advanced"', 'text\t\t"gui::txt_advanced"')
    ])

    # AudioButton.pd
    update_file("mainmenu/Options/AudioButton.pd", [
        ('text "Audio"', 'text "gui::txt_tab_audio"'),
        ('text\t\t"Audio Settings"', 'text\t\t"gui::txt_audiosettings"')
    ])

    # 3. Controls sub-tabs
    update_file("mainmenu/Options/ControlsMovement.pd", [
        ('text\t\t"Movement"', 'text\t\t"gui::txt_movement"')
    ])
    update_file("mainmenu/Options/ControlsWeapons.pd", [
        ('text\t\t"Weapons"', 'text\t\t"gui::txt_weapons"')
    ])
    update_file("mainmenu/Options/ControlsAttack.pd", [
        ('text\t\t"Miscellaneous"', 'text\t\t"gui::txt_misc"'),
        ('text\t\t"Use Button"', 'text\t\t"gui::txt_use_btn"'),
        ('text\t\t"Show Objectives"', 'text\t\t"gui::txt_objectives"')
    ])

    # 4. LoadGameMenu.pd
    update_file("mainmenu/LoadGameMenu.pd", [
        ('text\t\t"LOAD GAME"', 'text\t\t"gui::txt_loadgame_title"'),
        ('text\t\t"NAME"', 'text\t\t"gui::txt_col_name"'),
        ('text\t\t"DATE"', 'text\t\t"gui::txt_col_date"'),
        ('text\t\t"TIME"', 'text\t\t"gui::txt_col_time"'),
        ('text "LOAD SAVEGAME"', 'text "gui::txt_btn_load"'),
        ('text "DELETE SAVEGAME"', 'text "gui::txt_btn_delete"')
    ])

    # 5. SaveGameMenu.pd
    update_file("mainmenu/SaveGameMenu.pd", [
        ('text\t\t"SAVE GAME"', 'text\t\t"gui::txt_savegame_title"'),
        ('text\t\t"NAME"', 'text\t\t"gui::txt_col_name"'),
        ('text\t\t"DATE"', 'text\t\t"gui::txt_col_date"'),
        ('text\t\t"TIME"', 'text\t\t"gui::txt_col_time"'),
        ('text "SAVE GAME"', 'text "gui::txt_btn_save"')
    ])

    # 6. SelectSkillLevel.pd
    update_file("mainmenu/SelectSkillLevel.pd", [
        ('text "Choose a skill level"', 'text "gui::txt_skill_title"'),
        ('text "I\'m too young to die!"', 'text "gui::txt_skill_1"'),
        ('text "Hurt me plenty"', 'text "gui::txt_skill_2"'),
        ('text "Ultra-violence"', 'text "gui::txt_skill_3"'),
        ('text "NIGHTMARE"', 'text "gui::txt_skill_4"'),
        ('text "CANCEL"', 'text "gui::txt_skill_cancel"')
    ])

    # 7. ExitGame.pd
    update_file("mainmenu/ExitGame.pd", [
        ('text "EXIT GAME?"', 'text "gui::txt_exit_title"'),
        ('text "Are you sure you want to quit?"', 'text "gui::txt_exit_msg"'),
        ('text "YES"', 'text "gui::txt_yes"'),
        ('text "NO"', 'text "gui::txt_no"')
    ])

    # 8. DeleteGame.pd
    update_file("mainmenu/DeleteGame.pd", [
        ('text "DELETE SAVEGAME?"', 'text "gui::txt_del_title"'),
        ('text "DELETE"', 'text "gui::txt_delete"'),
        ('text "CANCEL"', 'text "gui::txt_btn_cancel"')
    ])

    # 9. EndGame.pd
    update_file("mainmenu/EndGame.pd", [
        ('text "END GAME"', 'text "gui::txt_end_title"'),
        ('text "Are you sure you want to end the game?"', 'text "gui::txt_end_msg"'),
        ('text "YES"', 'text "gui::txt_yes"'),
        ('text "Cancel"', 'text "gui::txt_btn_cancel"')
    ])

    # 10. OverwriteSaveGame.pd
    update_file("mainmenu/OverwriteSaveGame.pd", [
        ('text "Overwrite SAVEGAME?"', 'text "gui::txt_ovr_title"'),
        ('text "Overwrite"', 'text "gui::txt_overwrite"'),
        ('text "CANCEL"', 'text "gui::txt_btn_cancel"')
    ])

    # 11. ApplyChanges.pd
    update_file("mainmenu/ApplyChanges.pd", [
        ('text "RESTART VIDEO"', 'text "gui::txt_apply_title"'),
        ('text "Do you wish to restart video?"', 'text "gui::txt_apply_msg"'),
        ('text "OK"', 'text "gui::txt_ok"'),
        ('text "Cancel"', 'text "gui::txt_btn_cancel"')
    ])

    # 12. Episodes
    for ep in ['Ep1Button.pd', 'Ep2Button.pd', 'Ep3Button.pd', 'Ep4Button.pd', 'Ep5Button.pd', 'PrologueButton.pd']:
        update_file(f"mainmenu/Episodes/{ep}", [
            ('text "EPISODE UNAVAILABLE"', 'text "gui::txt_ep_unavail"')
        ])

    print("All .pd files updated successfully!")

if __name__ == "__main__":
    run()
