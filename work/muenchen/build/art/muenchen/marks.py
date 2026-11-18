# -*- coding: utf-8 -*-
# כרטיסים קיימים בקובץ העיר שמסומנים גם כיצירות (שדה e -> aw). המזהים מ-OpenStreetMap.
MARK = {
 "Memorial for the Victims of National Socialism (Platz der Opfer des Nationalsozialismus)": {"k": "n441271086", "t": "אנדרטה", "p": ["jew", "h2"], "z": 1},
 "Ludwig Maximilian University and the White Rose memorial": {"k": "n5503441922", "t": "אנדרטה", "p": ["h2"], "z": 1},
 "Walking Man (Borofsky) and Münchner Freiheit": {"k": "w176590371", "t": "פסל", "p": ["h3", "abs"], "z": 0},
 "Angel of Peace (Friedensengel)": {"k": "w48441018", "t": "אנדרטה", "p": ["h1"], "z": 1},
 "Bavaria statue and Ruhmeshalle": {"k": "w96753009", "t": "פסל", "p": ["h1", "ppl"], "z": 1},
 "Oktoberfest bombing memorial (1980)": {"k": "n311974710", "t": "אנדרטה", "p": ["h3"], "z": 0},
 "Memorial to the 1972 Olympic attack (Erinnerungsort Olympia-Attentat)": {"k": "n4068438305", "t": "אנדרטה", "p": ["jew", "h3"], "z": 0},
 "Fish Fountain (Fischbrunnen)": {"k": "w117873670", "t": "מזרקה", "p": ["fnt", "h1"], "z": 1},
 "Hubertus Fountain": {"k": "n1337056612", "t": "מזרקה", "p": ["fnt", "ani"], "z": 0},
}
# יצירות שהוסרו אחרי הביקורת (סעיף 9.10), לפי הסיבה
SKIP = set()
SKIP |= set('n441271086 n5503441922 w176590371 w48441018 n311974710 w96753009 n1337056612 n4068438305'.split())  # אותה יצירה כבר מסומנת ככרטיס קיים בקובץ העיר (MARK)
SKIP |= set('w215291417 w851851301 n14289399780 n2515521124 n292910963 n2427886290 n8075117775 n11040119385 w1378770479'.split())  # כפילות (אותה יצירה או כרטיס קיים)
SKIP |= set('n9250152869 n9240705154 n9250151289 n9385447916 n9387754924 n9337750029 n9340994982 n9251380991 n9482908528 n9490079052 n9422551912 n9542973329 n9142685044 n14363566982 n14363417965 n8113016811 n8917523469 n9350544118'.split())  # בתוך מבנה סגור (כנסייה, קפלה, קומה פנימית, מתחם סגור)
SKIP |= set('n10676110247 n12898564358 n673851790 n9341587069 w110537428 n666304991'.split())  # אינה יצירה (מוצג טכני, שלט, תערוכה, ברז, מבנה)
SKIP |= set('n14174071507 n9422298866'.split())  # זמנית או הוסרה
SKIP |= set('n433909671 n2859401856 n8182265281 n9592006823 n670710436 n1784539254 r21117549'.split())  # אין עליה שום מידע
SRC = "הנתונים שנאספו (OpenStreetMap, ויקידאטה ומקורות כלליים)"
