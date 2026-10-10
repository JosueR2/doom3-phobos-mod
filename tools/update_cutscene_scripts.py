# -*- coding: utf-8 -*-
import os

# --- 1. map_e1m1.script ---
p1 = "src/script/map_e1m1.script"
with open(p1, "r", encoding="latin-1") as f:
    c1 = f.read()

old_timer_1 = """\tvoid EnableSkipTimer()
\t{
\t\t// Wait 2 seconds for the scene to settle and ignore any clicks from the menu
\t\tsys.wait(2.0);

\t\tif (map_intro::introSkipped == 0 && map_intro::introActive == 1)
\t\t{
\t\t\tmap_intro::canSkipIntro = 1;
\t\t\tPhobosShowSubtitle_e1m1("", "[ Press SPACE or X to skip ]");
\t\t\tsys.wait(5.0);
\t\t\tif (map_intro::introSkipped == 0 && map_intro::introActive == 1)
\t\t\t{
\t\t\t\tsys.hideSubtitles();
\t\t\t}
\t\t}
\t}"""

new_timer_1 = """\tvoid EnableSkipTimer()
\t{
\t\t// Wait 2 seconds for the scene to settle and ignore any clicks from the menu
\t\tsys.wait(2.0);

\t\tif (map_intro::introSkipped == 0 && map_intro::introActive == 1)
\t\t{
\t\t\tmap_intro::canSkipIntro = 1;
\t\t\tPhobosSetCanSkip(1);
\t\t}
\t}"""

assert old_timer_1 in c1, "old_timer_1 not found in map_e1m1.script"
c1 = c1.replace(old_timer_1, new_timer_1, 1)

old_skip_seq_1 = """\t\tmap_intro::introSkipped = 1;
\t\tmap_intro::introActive = 0;
\t\tmap_intro::canSkipIntro = 0;"""

new_skip_seq_1 = """\t\tmap_intro::introSkipped = 1;
\t\tmap_intro::introActive = 0;
\t\tmap_intro::canSkipIntro = 0;
\t\tPhobosSetCanSkip(0);"""

assert old_skip_seq_1 in c1, "old_skip_seq_1 not found in map_e1m1.script"
c1 = c1.replace(old_skip_seq_1, new_skip_seq_1, 1)

old_endbox = """\t\tmap_intro::activeCam = 0;
\t\tmap_intro::introActive = 0;
\t}"""

new_endbox = """\t\tmap_intro::activeCam = 0;
\t\tmap_intro::introActive = 0;
\t\tmap_intro::canSkipIntro = 0;
\t\tPhobosSetCanSkip(0);
\t}"""

assert old_endbox in c1, "old_endbox not found in map_e1m1.script"
c1 = c1.replace(old_endbox, new_endbox, 1)

with open(p1, "w", encoding="latin-1") as f:
    f.write(c1)
print("Updated map_e1m1.script successfully!")


# --- 2. map_e1m1_scanner.script ---
p2 = "src/script/map_e1m1_scanner.script"
with open(p2, "r", encoding="latin-1") as f:
    c2 = f.read()

old_timer_2 = """\tvoid EnableScannerSkipTimer()
\t{
\t\tsys.wait(1.5);
\t\tif (scannerActive == 1 && scannerSkipped == 0)
\t\t{
\t\t\tcanSkipScanner = 1;
\t\t\tPhobosShowSubtitle_e1m1("", "[ Press SPACE or X to skip ]");
\t\t\tsys.wait(5.0);
\t\t\tif (scannerActive == 1 && scannerSkipped == 0)
\t\t\t{
\t\t\t\tsys.hideSubtitles();
\t\t\t}
\t\t}
\t}"""

new_timer_2 = """\tvoid EnableScannerSkipTimer()
\t{
\t\tsys.wait(1.5);
\t\tif (scannerActive == 1 && scannerSkipped == 0)
\t\t{
\t\t\tcanSkipScanner = 1;
\t\t\tPhobosSetCanSkip(1);
\t\t}
\t}"""

assert old_timer_2 in c2, "old_timer_2 not found in map_e1m1_scanner.script"
c2 = c2.replace(old_timer_2, new_timer_2, 1)

old_skip_seq_2 = """\t\tscannerSkipped = 1;
\t\tcanSkipScanner = 0;
\t\tscannerActive = 0;"""

new_skip_seq_2 = """\t\tscannerSkipped = 1;
\t\tcanSkipScanner = 0;
\t\tscannerActive = 0;
\t\tPhobosSetCanSkip(0);"""

assert old_skip_seq_2 in c2, "old_skip_seq_2 not found in map_e1m1_scanner.script"
c2 = c2.replace(old_skip_seq_2, new_skip_seq_2, 1)

old_scanner_end = """\t\tsys.trigger($target_endlevel_1);
\t}

\tfloat b = 0;"""

new_scanner_end = """\t\tPhobosSetCanSkip(0);
\t\tsys.trigger($target_endlevel_1);
\t}

\tfloat b = 0;"""

assert old_scanner_end in c2, "old_scanner_end not found in map_e1m1_scanner.script"
c2 = c2.replace(old_scanner_end, new_scanner_end, 1)

with open(p2, "w", encoding="latin-1") as f:
    f.write(c2)
print("Updated map_e1m1_scanner.script successfully!")


# --- 3. map_e1m1_1.script ---
p3 = "src/script/map_e1m1_1.script"
with open(p3, "r", encoding="latin-1") as f:
    c3 = f.read()

old_timer_3 = """\tvoid EnableHospitalSkipTimer()
\t{
\t\tsys.wait(1.5);
\t\tif (hospitalActive == 1 && hospitalSkipped == 0)
\t\t{
\t\t\tcanSkipHospital = 1;
\t\t\tPhobosShowSubtitle_e1m1_1("", "[ Press SPACE or X to skip ]");
\t\t\tsys.wait(5.0);
\t\t\tif (hospitalActive == 1 && hospitalSkipped == 0)
\t\t\t{
\t\t\t\tsys.hideSubtitles();
\t\t\t}
\t\t}
\t}"""

new_timer_3 = """\tvoid EnableHospitalSkipTimer()
\t{
\t\tsys.wait(1.5);
\t\tif (hospitalActive == 1 && hospitalSkipped == 0)
\t\t{
\t\t\tcanSkipHospital = 1;
\t\t\tPhobosSetCanSkip(1);
\t\t}
\t}"""

assert old_timer_3 in c3, "old_timer_3 not found in map_e1m1_1.script"
c3 = c3.replace(old_timer_3, new_timer_3, 1)

old_skip_seq_3 = """\t\thospitalSkipped = 1;
\t\tcanSkipHospital = 0;
\t\thospitalActive = 0;"""

new_skip_seq_3 = """\t\thospitalSkipped = 1;
\t\tcanSkipHospital = 0;
\t\thospitalActive = 0;
\t\tPhobosSetCanSkip(0);"""

assert old_skip_seq_3 in c3, "old_skip_seq_3 not found in map_e1m1_1.script"
c3 = c3.replace(old_skip_seq_3, new_skip_seq_3, 1)

old_hosp_end = """\t\tsys.trigger($relay_objective_doctor_complete);
\t\thospitalActive = 0;
\t}"""

new_hosp_end = """\t\tsys.trigger($relay_objective_doctor_complete);
\t\thospitalActive = 0;
\t\tcanSkipHospital = 0;
\t\tPhobosSetCanSkip(0);
\t}"""

assert old_hosp_end in c3, "old_hosp_end not found in map_e1m1_1.script"
c3 = c3.replace(old_hosp_end, new_hosp_end, 1)

with open(p3, "w", encoding="latin-1") as f:
    f.write(c3)
print("Updated map_e1m1_1.script successfully!")


# --- 4. map_e1m3.script ---
p4 = "src/script/map_e1m3.script"
with open(p4, "r", encoding="latin-1") as f:
    c4 = f.read()

old_timer_4 = """\tvoid EnableDepartureSkipTimer()
\t{
\t\tsys.wait(1.5);
\t\tif (departureActive == 1 && departureSkipped == 0)
\t\t{
\t\t\tcanSkipDeparture = 1;
\t\t\tPhobosShowSubtitle_e1m3("", "[ Press SPACE or X to skip ]");
\t\t\tsys.wait(5.0);
\t\t\tif (departureActive == 1 && departureSkipped == 0)
\t\t\t{
\t\t\t\tsys.hideSubtitles();
\t\t\t}
\t\t}
\t}"""

new_timer_4 = """\tvoid EnableDepartureSkipTimer()
\t{
\t\tsys.wait(1.5);
\t\tif (departureActive == 1 && departureSkipped == 0)
\t\t{
\t\t\tcanSkipDeparture = 1;
\t\t\tPhobosSetCanSkip(1);
\t\t}
\t}"""

assert old_timer_4 in c4, "old_timer_4 not found in map_e1m3.script"
c4 = c4.replace(old_timer_4, new_timer_4, 1)

old_skip_seq_4 = """\t\tdepartureSkipped = 1;
\t\tcanSkipDeparture = 0;
\t\tdepartureActive = 0;"""

new_skip_seq_4 = """\t\tdepartureSkipped = 1;
\t\tcanSkipDeparture = 0;
\t\tdepartureActive = 0;
\t\tPhobosSetCanSkip(0);"""

assert old_skip_seq_4 in c4, "old_skip_seq_4 not found in map_e1m3.script"
c4 = c4.replace(old_skip_seq_4, new_skip_seq_4, 1)

old_depart_end = """\t\tactiveDepartureCam = 0;
\t\tdepartureActive = 0;
\t\tsys.trigger($info_player_teleport_outro);"""

new_depart_end = """\t\tactiveDepartureCam = 0;
\t\tdepartureActive = 0;
\t\tcanSkipDeparture = 0;
\t\tPhobosSetCanSkip(0);
\t\tsys.trigger($info_player_teleport_outro);"""

assert old_depart_end in c4, "old_depart_end not found in map_e1m3.script"
c4 = c4.replace(old_depart_end, new_depart_end, 1)

with open(p4, "w", encoding="latin-1") as f:
    f.write(c4)
print("Updated map_e1m3.script successfully!")


# --- 5. map_e1m3_outro.script ---
p5 = "src/script/map_e1m3_outro.script"
with open(p5, "r", encoding="latin-1") as f:
    c5 = f.read()

old_timer_5 = """\tvoid EnableOutroSkipTimer()
\t{
\t\tsys.wait(1.5);
\t\tif (outroActive == 1 && outroSkipped == 0)
\t\t{
\t\t\tcanSkipOutro = 1;
\t\t\tPhobosShowSubtitle_e1m3_outro("", "[ Press SPACE or X to skip ]");
\t\t\tsys.wait(5.0);
\t\t\tif (outroActive == 1 && outroSkipped == 0)
\t\t\t{
\t\t\t\tsys.hideSubtitles();
\t\t\t}
\t\t}
\t}"""

new_timer_5 = """\tvoid EnableOutroSkipTimer()
\t{
\t\tsys.wait(1.5);
\t\tif (outroActive == 1 && outroSkipped == 0)
\t\t{
\t\t\tcanSkipOutro = 1;
\t\t\tPhobosSetCanSkip(1);
\t\t}
\t}"""

assert old_timer_5 in c5, "old_timer_5 not found in map_e1m3_outro.script"
c5 = c5.replace(old_timer_5, new_timer_5, 1)

old_skip_seq_5 = """\t\toutroSkipped = 1;
\t\tcanSkipOutro = 0;
\t\toutroActive = 0;"""

new_skip_seq_5 = """\t\toutroSkipped = 1;
\t\tcanSkipOutro = 0;
\t\toutroActive = 0;
\t\tPhobosSetCanSkip(0);"""

assert old_skip_seq_5 in c5, "old_skip_seq_5 not found in map_e1m3_outro.script"
c5 = c5.replace(old_skip_seq_5, new_skip_seq_5, 1)

old_outro_end = """\t\tsys.wait(12);
\t\tsys.trigger($EndEpisodeOne);
\t}"""

new_outro_end = """\t\tsys.wait(12);
\t\toutroActive = 0;
\t\tcanSkipOutro = 0;
\t\tPhobosSetCanSkip(0);
\t\tsys.trigger($EndEpisodeOne);
\t}"""

assert old_outro_end in c5, "old_outro_end not found in map_e1m3_outro.script"
c5 = c5.replace(old_outro_end, new_outro_end, 1)

with open(p5, "w", encoding="latin-1") as f:
    f.write(c5)
print("Updated map_e1m3_outro.script successfully!")

