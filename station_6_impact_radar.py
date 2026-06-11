#!/usr/bin/env python3
"""
================================================================================
  MOON BASE ALPHA  --  ESCAPE GAME CONSOLE
  STATION 6 of 6 : IMPACT RADAR  (the "master clock" station)
================================================================================

WHAT THIS IS
  A single-file, no-install Python console puzzle. Runs on any laptop with
  Python 3 (Windows / Mac / Linux). Pure standard library -- nothing to pip.

HOW TO RUN
  Double-click won't show the window cleanly on every OS, so the reliable way:
      Windows : open a terminal, type  py station_6_impact_radar.py
      Mac     : open Terminal, type    python3 station_6_impact_radar.py

HOW TO CLONE THIS INTO STATIONS 1-5
  Everything above the line  "### === EDIT BELOW FOR EACH STATION === ###"
  is the reusable FRAMEWORK. Copy this file, keep the framework, and rewrite
  only the puzzle content below that line. Each station should end by handing
  the team ONE shield-code digit for the finale.

TEACHES (without ever saying "today we will learn...")
  * A meteor shower has a RADIANT -- one point the meteors stream away from.
  * A shower PEAKS when you pass through the densest part of the comet's
    debris stream, and that peak time is predictable.
  * Why this matters on the airless Moon: no sky streaks, just impacts.
================================================================================
"""

import os
import re
import sys
import time

# ---------------------------------------------------------------------------
#  FRAMEWORK  (shared by all six stations -- copy this whole block unchanged)
# ---------------------------------------------------------------------------

SLOW = True          # set False to disable the typewriter effect (faster testing)
CHAR_DELAY = 0.012   # seconds per character when SLOW is True

# Try to turn on colored text in Windows terminals. Degrades silently if it
# doesn't work -- the game is fully readable without color.
if os.name == "nt":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleMode(
            ctypes.windll.kernel32.GetStdHandle(-11), 7
        )
    except Exception:
        pass

C = {
    "reset": "\033[0m",
    "dim":   "\033[2m",
    "amber": "\033[38;5;214m",
    "cyan":  "\033[38;5;51m",
    "green": "\033[38;5;46m",
    "red":   "\033[38;5;203m",
    "white": "\033[97m",
}


def color(text, key):
    return f"{C.get(key, '')}{text}{C['reset']}"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def tw(text="", delay=CHAR_DELAY, end="\n"):
    """Typewriter print. Press nothing -- it just streams a little for mood."""
    if not SLOW:
        print(text, end=end)
        return
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()


def banner(title, subtitle=""):
    width = 70
    bar = "=" * width
    print(color(bar, "amber"))
    print(color(title.center(width), "amber"))
    if subtitle:
        print(color(subtitle.center(width), "dim"))
    print(color(bar, "amber"))
    print()


def pause(msg="   [ press ENTER to continue ]"):
    try:
        input(color(msg, "dim"))
    except (EOFError, KeyboardInterrupt):
        pass


def solve(question, check, hints, success, intro_lines=None):
    """
    The core puzzle loop. It is FORGIVING and has NO DEAD ENDS:
      * Players can type 'hint' (or 'h' or '?') any time for the next hint.
      * After 3 wrong tries it offers a hint automatically.
      * The final hint in the list always reveals enough to get unstuck.

    question : the prompt string shown at the input line
    check    : function(player_text) -> True if correct
    hints    : list of progressively bigger hints (last one nearly gives it)
    success  : message printed on a correct answer
    """
    if intro_lines:
        for line in intro_lines:
            tw(line)
        print()

    hint_index = 0
    wrong = 0
    while True:
        try:
            ans = input(color(f"  {question} > ", "cyan")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            continue

        if ans.lower() in ("hint", "h", "?"):
            tip = hints[min(hint_index, len(hints) - 1)]
            tw(color(f"  HINT: {tip}", "dim"))
            hint_index += 1
            continue

        if not ans:
            continue

        if check(ans):
            print()
            tw(color(success, "green"))
            print()
            return ans

        wrong += 1
        tw(color("  >> Reading doesn't match. Re-check and try again.", "red"))
        if wrong % 3 == 0 and hint_index < len(hints):
            tip = hints[hint_index]
            tw(color(f"  HINT: {tip}", "dim"))
            hint_index += 1


# --- small normalizers so we accept messy kid-typed answers ------------------

def cell_norm(text):
    """'f7', 'F-7', 'F 7', '7f'  ->  'F7' """
    s = re.sub(r"[^A-Za-z0-9]", "", text).upper()
    letters = "".join(c for c in s if c.isalpha())
    digits = "".join(c for c in s if c.isdigit())
    return f"{letters}{digits}"


def first_int(text):
    """Pull the first whole number out of any answer. Returns None if none."""
    m = re.search(r"\d+", text)
    return int(m.group()) if m else None


### ========================================================================
### === EDIT BELOW FOR EACH STATION ===  (everything above is reusable)  ===
### ========================================================================

STATION_NAME = "IMPACT RADAR"
STATION_NUMBER = 6                 # which of the six shield digits this gives
RADIANT_CELL = "F7"                # where the meteor tracks converge

# The radar picture. '*' = a meteoroid track blip. Notice the blips stream
# OUTWARD from one empty cell (F7) -- that empty eye is the radiant, exactly
# how a real meteor shower looks. Players trace the tails back to find it.
RADAR_BLIPS = {
    "B3", "C4", "D5", "E6",       # ray pointing up-left
    "C10", "D9", "E8",            # ray pointing up-right
    "F1", "F3", "F5",            # ray pointing left
    "F9",                         # ray pointing right
    "G6", "H5",                   # ray pointing down-left
    "G8", "H9",                   # ray pointing down-right
}


def draw_radar():
    rows = "ABCDEFGH"
    header = "      " + "".join(f"{c:>3}" for c in range(1, 11))
    print(color(header, "dim"))
    for r in rows:
        line = f"   {r}  "
        for c in range(1, 11):
            cell = f"{r}{c}"
            line += f"  {'*' if cell in RADAR_BLIPS else '.'}"
        print(color(line, "cyan"))
    print()


def intro():
    clear()
    banner("M O O N   B A S E   A L P H A", "Shackleton Ridge  -  Lunar South Pole")
    tw(color("  >> NIGHT SHIFT LOG -- automated alert -------------------", "amber"))
    tw("  Impact rate on the outer hull is climbing. Fast.")
    tw("  Senior crew is out on the traverse and out of contact.")
    tw("  You are the only ones who can read the radar tonight.")
    print()
    tw(color("  A message is pinned to this console. Old. Handwritten.", "dim"))
    tw(color('   "If the rate is rising, do NOT panic. Confirm what it is,', "white"))
    tw(color('    find when it peaks, raise the shield. You can do this.', "white"))
    tw(color('                                          - V. L."', "white"))
    print()
    pause()


def puzzle_1_radiant():
    clear()
    banner("IMPACT RADAR  -  STEP 1 of 3", "What is hitting us?")
    tw("  The radar is plotting incoming tracks. Each * is a strike heading.")
    tw("  Real space junk comes from everywhere. A meteor SHOWER does not --")
    tw("  every track streams away from a single point in the sky.")
    print()
    tw(color("  ...scanning...", "dim")); time.sleep(0.6 if SLOW else 0)
    print()
    draw_radar()
    tw("  Trace the tails back. They all point away from ONE empty cell.")
    tw("  That cell is the RADIANT. Report its grid reference (letter+number).")
    print()

    solve(
        question="RADIANT CELL",
        check=lambda a: cell_norm(a) == RADIANT_CELL,
        hints=[
            "Pick any * and follow the line of *'s back toward the middle.",
            "All the rays meet near the lower-middle of the grid.",
            "It is in row F. Now count the columns to the center: F7.",
        ],
        success="  >> RADIANT LOCKED. Cross-referencing star chart...\n"
                "  >> Origin matches the constellation PERSEUS.\n"
                "  >> CONFIRMED: this is the PERSEID meteor shower. Not junk.",
        intro_lines=None,
    )
    tw(color("  Good. Knowing WHAT it is means we can predict what it does next.", "white"))
    print()
    pause()


def puzzle_2_peak():
    clear()
    banner("IMPACT RADAR  -  STEP 2 of 3", "When does it peak?")
    tw("  A shower gets worse as we plow into the THICKEST part of the comet's")
    tw("  dust stream, then eases off. Dr. Leavitt's stream model is loaded:")
    print()
    tw(color("     We ENTERED the dense stream at .......... 02:00", "cyan"))
    tw(color("     We will EXIT the dense stream at ......... 04:00", "cyan"))
    tw(color("     The stream is symmetric -- thickest dead center.", "dim"))
    print()
    tw("  Live impact rate, climbing on schedule:")
    tw(color("     02:00  ..  10 / min", "dim"))
    tw(color("     02:15  ..  18 / min", "dim"))
    tw(color("     02:30  ..  31 / min", "dim"))
    tw(color("     02:45  ..  52 / min   <-- it is now 02:45", "amber"))
    print()
    tw("  The model is right. So: what TIME is the peak (the exact center")
    tw("  between entering and exiting)?")
    print()

    solve(
        question="PEAK TIME (hh:mm)",
        check=lambda a: first_int(a) == 3,
        hints=[
            "The center is halfway between 02:00 and 04:00.",
            "Add the two hours and split the difference: 2 and 4 ...",
            "Halfway between 2 o'clock and 4 o'clock is 03:00.",
        ],
        success="  >> PEAK CONFIRMED: 03:00. That is our deadline.",
    )

    tw("  One more: it is 02:45 right now. How many MINUTES until 03:00?")
    print()
    solve(
        question="MINUTES TO PEAK",
        check=lambda a: first_int(a) == 15,
        hints=[
            "Count from :45 up to the next :00.",
            "From 02:45 to 03:00 is a quarter of an hour.",
            "It is 15 minutes.",
        ],
        success="  >> COUNTDOWN ARMED: 15:00 to peak. Shield must be up before then.",
    )
    tw(color("  >> RELAY: peak time + countdown sent to COMMAND console.", "amber"))
    print()
    pause()


def puzzle_3_shield_digit():
    clear()
    banner("IMPACT RADAR  -  STEP 3 of 3", "Your piece of the shield code")
    tw("  The hull shield won't raise without a 6-digit code -- one digit")
    tw("  from each station. Dr. Leavitt's protocol sets THIS station's digit:")
    print()
    tw(color('     "Station 6 digit = the PEAK HOUR you just found."', "white"))
    print()
    tw("  You found the peak at 03:00. Enter the peak HOUR to lock your digit.")
    print()

    solve(
        question="STATION 6 DIGIT",
        check=lambda a: first_int(a) == 3,
        hints=[
            "The peak was at 03:00. The hour is the first number.",
            "03:00 -- the hour is 3.",
            "Enter 3.",
        ],
        success="  >> DIGIT LOCKED.",
    )

    clear()
    banner("SHIELD CODE FRAGMENT  -  6 of 6")
    print()
    tw(color("        +-----------------------------+", "green"))
    tw(color("        |   STATION 6  (IMPACT RADAR) |", "green"))
    tw(color("        |                             |", "green"))
    tw(color("        |        DIGIT  =   3         |", "green"))
    tw(color("        |                             |", "green"))
    tw(color("        +-----------------------------+", "green"))
    print()
    tw("  Write this digit on your team card and carry it to COMMAND.")
    print()
    tw(color("  Final note, in the same old handwriting:", "dim"))
    tw(color('   "Six locks, six keys. No one believed the rate would spike", "white'))
    tw(color('    this high -- but the data did. Trust the data. Bring all', "white"))
    tw(color('    six digits together and raise the shield. - V. L."', "white"))
    print()
    pause("   [ press ENTER to power down this console ]")


def main():
    try:
        intro()
        puzzle_1_radiant()
        puzzle_2_peak()
        puzzle_3_shield_digit()
        clear()
        banner("STATION 6 COMPLETE", "Impact Radar -- digit secured: 3")
        tw(color("  Nicely flown. Now help the others. The peak won't wait.", "white"))
        print()
    except KeyboardInterrupt:
        print(color("\n  [console interrupted -- restart with the run command above]", "dim"))


if __name__ == "__main__":
    main()
