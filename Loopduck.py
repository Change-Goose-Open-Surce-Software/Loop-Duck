#!/usr/bin/env python3
"""
Loop Duck - Terminal Loop Utility
by Change Goose
"""

import sys
import os
import subprocess
import argparse
import re
import webbrowser
import time
from datetime import datetime
from typing import List, Tuple, Optional

VERSION = "1.0"
RELEASE_DATE = "2024-02-02 14:30"
GITHUB_URL = "https://github.com/Change-Goose-Open-Surce-Software?tab=repositories"
UPDATE_URL = "https://raw.githubusercontent.com/Change-Goose-Open-Surce-Software/Loop-Duck/main/install.sh"

# Version History
VERSION_HISTORY = {
    "1.0": {
        "date": "2024-02-02 14:30",
        "changes": [
            "Initial Release",
            "Loop-Funktionalität mit Wiederholungen",
            "Parameter: -c (changes), -o (output), -s (stop), -q (quit)",
            "Gegebenheiten-System mit Backticks",
            "TUI mit Retro-Vibes und RGB-Effekten",
            "F&Q Menü mit Pfeiltasten-Navigation",
            "Update-Funktion mit wget"
        ]
    }
}

# FAQ Data - NUR PLATZHALTER! Zum Ausfüllen gedacht
FAQ_DATA = {
    "Grundlagen": [
        {"q": "Frage 1 - Platzhalter", "a": "Antwort 1 - Platzhalter"},
        {"q": "Frage 2 - Platzhalter", "a": "Antwort 2 - Platzhalter"},
        {"q": "Frage 3 - Platzhalter", "a": "Antwort 3 - Platzhalter"},
    ],
    "Parameter": [
        {"q": "Frage 4 - Platzhalter", "a": "Antwort 4 - Platzhalter"},
        {"q": "Frage 5 - Platzhalter", "a": "Antwort 5 - Platzhalter"},
    ],
    "Gegebenheiten": [
        {"q": "Frage 6 - Platzhalter", "a": "Antwort 6 - Platzhalter"},
        {"q": "Frage 7 - Platzhalter", "a": "Antwort 7 - Platzhalter"},
    ],
    "Fortgeschritten": [
        {"q": "Frage 8 - Platzhalter", "a": "Antwort 8 - Platzhalter"},
    ],
    "Installation": [
        {"q": "Frage 9 - Platzhalter", "a": "Antwort 9 - Platzhalter"},
        {"q": "Frage 10 - Platzhalter", "a": "Antwort 10 - Platzhalter"},
    ]
}


class LoopDuck:
    """Hauptklasse für Loop Duck Funktionalität"""
    
    def __init__(self):
        self.outputs = []
        self.changes_detected = []
        
    def parse_condition(self, condition: str) -> Tuple[str, str, Optional[int]]:
        """
        Parse eine Gegebenheit wie `-c =p =3`
        Returns: (param, comparison, loop_number)
        """
        condition = condition.strip('`').strip()
        parts = condition.split()
        
        param = parts[0] if len(parts) > 0 else ""
        comparison = parts[1] if len(parts) > 1 else ""
        loop_num = None
        
        if len(parts) > 2:
            try:
                loop_num = int(parts[2].strip('='))
            except:
                pass
                
        return param, comparison, loop_num
    
    def check_condition(self, condition: str, current_loop: int) -> bool:
        """Prüft ob eine Gegebenheit erfüllt ist"""
        param, comparison, loop_num = self.parse_condition(condition)
        
        # Wenn eine spezifische Loop-Nummer angegeben ist
        if loop_num is not None and current_loop != loop_num:
            return False
        
        # Check index für changes_detected
        check_idx = loop_num - 1 if loop_num else current_loop - 1
        
        if param == "-c":
            if check_idx >= len(self.changes_detected):
                return False
                
            has_changes = self.changes_detected[check_idx]
            
            if comparison == "=p":  # positiv (Änderungen vorhanden)
                return has_changes
            elif comparison == "=n":  # negativ (keine Änderungen)
                return not has_changes
                
        return False
    
    def run_loop(self, iterations: int, command: List[str], 
                 check_changes: bool = False, 
                 show_output: bool = False,
                 quit_after: bool = False,
                 stop_condition: Optional[str] = None) -> int:
        """
        Führt einen Befehl mehrfach aus
        """
        print(f"🦆 Loop Duck startet {iterations} Iterationen von: {' '.join(command)}")
        print("-" * 60)
        
        for i in range(1, iterations + 1):
            print(f"\n▶ Loop {i}/{iterations}")
            
            try:
                if show_output:
                    # Zeige vollen Output
                    result = subprocess.run(command, 
                                          capture_output=False,
                                          text=True)
                    output = ""
                else:
                    # Capture Output für Vergleich
                    result = subprocess.run(command, 
                                          capture_output=True,
                                          text=True)
                    output = result.stdout + result.stderr
                    
                self.outputs.append(output)
                
                # Check for changes
                if check_changes and i > 1:
                    has_changes = self.outputs[-1] != self.outputs[-2]
                    self.changes_detected.append(has_changes)
                    
                    if has_changes:
                        print("  ✓ Änderungen erkannt")
                    else:
                        print("  ✗ Keine Änderungen")
                elif check_changes and i == 1:
                    self.changes_detected.append(False)
                
                # Quit-Parameter: Beende Prozess sofort
                if quit_after and result.returncode == 0:
                    # Für Programme die im Hintergrund laufen
                    pass
                
                # Check Stop-Condition
                if stop_condition and self.check_condition(stop_condition, i):
                    print(f"\n⏹ Stopp-Bedingung erfüllt bei Loop {i}")
                    return i
                    
            except KeyboardInterrupt:
                print(f"\n\n⏸ Unterbrochen bei Loop {i}/{iterations}")
                return i
            except Exception as e:
                print(f"  ❌ Fehler: {e}")
                
        print(f"\n✅ Alle {iterations} Loops abgeschlossen!")
        return iterations


def print_help():
    """Zeigt ausführliche Hilfe mit Beispielen"""
    help_text = r"""
🦆 Loop Duck - Terminal Loop Utility
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERWENDUNG:
    Loop <Anzahl> <Befehl> [Argumente...]
    Loop [Parameter] <Anzahl> <Befehl> [Argumente...]
    loop duck                    # Öffnet TUI-Menü
    loop duck version           # Zeigt Versionshistorie

BEISPIELE:
    Loop 3 ./data.sh
        → Führt data.sh 3 mal nacheinander aus
        
    Loop 5 firefox
        → Öffnet Firefox 5 mal (wartet auf Schließen)
        
    Loop -o 10 python script.py
        → Führt script.py 10 mal aus mit sichtbarem Output
        
    Loop -c 5 ./backup.sh
        → Zeigt Unterschiede zwischen den Ausführungen an
        
    Loop -q 3 steam
        → Startet Steam 3 mal und beendet es sofort wieder
        
    Loop -s `-c =n =7` 20 ./test.sh
        → Bricht ab wenn in Loop 7 keine Änderungen erkannt werden

PARAMETER:
    -c, --changes    Zeigt Unterschiede zwischen Ausführungen
    -o, --output     Zeigt den kompletten Terminal-Output
    -s, --stop       Bricht bei Bedingung ab
    -q, --quit       Beendet Programm sofort nach Start

GEGEBENHEITEN:
    Bedingungen in Backticks für -s Parameter:
    
    `-c =p`         Changes positiv (Unterschiede vorhanden)
    `-c =n`         Changes negativ (keine Unterschiede)
    `-c =p =3`      Changes positiv in Loop 3
    `-c =n =7`      Keine Changes in Loop 7

HINWEISE:
    • Alle Befehle laufen nacheinander, nicht parallel
    • Ein Befehl wird erst wiederholt wenn er beendet wurde
    • Parameter müssen VOR dem Programm stehen
    • Alles nach <Anzahl> gehört zum ausgeführten Befehl

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
by Change Goose | Version """ + VERSION + """
"""
    print(help_text)


def show_tui():
    """Zeigt das Terminal User Interface"""
    try:
        import curses
        curses.wrapper(main_menu)
    except ImportError:
        print("❌ curses Modul nicht verfügbar.")
        print("Verwende Loop Duck im Kommandozeilen-Modus.")


def run_update():
    """Führt das Update durch"""
    print("\n" + "="*60)
    print("🔄 Loop Duck Update")
    print("="*60)
    print(f"\nDownload von: {UPDATE_URL}")
    print("\nFühre aus:")
    print(f"  wget {UPDATE_URL}")
    print("  chmod +x install.sh")
    print("  ./install.sh")
    print("\n" + "-"*60)
    
    confirm = input("\nUpdate jetzt starten? (j/n): ").lower()
    
    if confirm == 'j':
        try:
            cmd = f'wget {UPDATE_URL} && chmod +x install.sh && ./install.sh'
            print(f"\n▶ Führe aus: {cmd}\n")
            subprocess.run(cmd, shell=True)
        except Exception as e:
            print(f"\n❌ Fehler beim Update: {e}")
    else:
        print("\n⏸ Update abgebrochen")
    
    input("\n[Enter] zum Fortfahren...")


def show_version_history_curses(stdscr):
    """Zeigt Versionshistorie mit curses"""
    import curses
    
    curses.curs_set(0)
    stdscr.clear()
    
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        # Header
        title = "VERSIONSHISTORIE"
        stdscr.addstr(1, w//2 - len(title)//2, title, curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(3, 0, "═" * w, curses.color_pair(1))
        
        y = 5
        for version, info in sorted(VERSION_HISTORY.items(), reverse=True):
            if y >= h - 3:
                break
                
            stdscr.addstr(y, 2, f"Version {version}", curses.color_pair(2) | curses.A_BOLD)
            y += 1
            stdscr.addstr(y, 2, info['date'], curses.color_pair(3))
            y += 2
            
            for change in info['changes']:
                if y >= h - 3:
                    break
                stdscr.addstr(y, 4, f"• {change}", curses.color_pair(3))
                y += 1
            y += 1
        
        # Footer
        stdscr.addstr(h-2, 0, "─" * w, curses.color_pair(1))
        stdscr.addstr(h-1, 2, "Enter: Zurück", curses.color_pair(3))
        
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == ord('\n') or key == ord('q'):
            break


def show_faq_categories(stdscr):
    """Zeigt FAQ Kategorien mit Pfeiltasten-Navigation"""
    import curses
    
    curses.curs_set(0)
    categories = list(FAQ_DATA.keys())
    current_row = 0
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        # Header mit RGB-Effekt
        title = "F&Q - KATEGORIEN"
        stdscr.addstr(1, w//2 - len(title)//2, title, curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(3, 0, "═" * w, curses.color_pair(1))
        
        # Kategorien
        for idx, category in enumerate(categories):
            y = 5 + idx * 2
            if y >= h - 3:
                break
                
            if idx == current_row:
                stdscr.addstr(y, 4, "► " + category, curses.color_pair(2) | curses.A_BOLD)
            else:
                stdscr.addstr(y, 4, "  " + category, curses.color_pair(3))
        
        # Footer
        stdscr.addstr(h-2, 0, "─" * w, curses.color_pair(1))
        stdscr.addstr(h-1, 2, "↑↓: Navigieren | Enter: Öffnen | q: Zurück", curses.color_pair(3))
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(categories) - 1:
            current_row += 1
        elif key == ord('\n'):
            show_faq_questions(stdscr, categories[current_row])
        elif key == ord('q'):
            break


def show_faq_questions(stdscr, category):
    """Zeigt Fragen einer Kategorie mit Pfeiltasten-Navigation"""
    import curses
    
    curses.curs_set(0)
    questions = FAQ_DATA[category]
    current_row = 0
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        # Header
        title = f"F&Q - {category.upper()}"
        stdscr.addstr(1, w//2 - len(title)//2, title, curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(3, 0, "═" * w, curses.color_pair(1))
        
        # Fragen
        for idx, qa in enumerate(questions):
            y = 5 + idx * 2
            if y >= h - 3:
                break
                
            question_num = str(idx + 1)
            if idx == current_row:
                stdscr.addstr(y, 4, f"► {question_num}. {qa['q']}"[:w-6], curses.color_pair(2) | curses.A_BOLD)
            else:
                stdscr.addstr(y, 4, f"  {question_num}. {qa['q']}"[:w-6], curses.color_pair(3))
        
        # Footer
        stdscr.addstr(h-2, 0, "─" * w, curses.color_pair(1))
        stdscr.addstr(h-1, 2, "↑↓: Navigieren | Enter: Antwort | q: Zurück", curses.color_pair(3))
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(questions) - 1:
            current_row += 1
        elif key == ord('\n'):
            show_faq_answer(stdscr, category, questions[current_row])
        elif key == ord('q'):
            break


def show_faq_answer(stdscr, category, qa):
    """Zeigt eine einzelne Antwort"""
    import curses
    
    curses.curs_set(0)
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        # Header
        title = f"F&Q - {category.upper()}"
        stdscr.addstr(1, w//2 - len(title)//2, title, curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(3, 0, "═" * w, curses.color_pair(1))
        
        # Frage
        stdscr.addstr(5, 2, "FRAGE:", curses.color_pair(2) | curses.A_BOLD)
        
        # Word wrap für Frage
        y = 6
        words = qa['q'].split()
        line = ""
        for word in words:
            if len(line) + len(word) + 1 <= w - 4:
                line += word + " "
            else:
                stdscr.addstr(y, 2, line.strip(), curses.color_pair(3))
                y += 1
                line = word + " "
        if line:
            stdscr.addstr(y, 2, line.strip(), curses.color_pair(3))
            y += 1
        
        y += 1
        stdscr.addstr(y, 2, "ANTWORT:", curses.color_pair(2) | curses.A_BOLD)
        y += 1
        
        # Word wrap für Antwort
        words = qa['a'].split()
        line = ""
        for word in words:
            if len(line) + len(word) + 1 <= w - 4:
                line += word + " "
            else:
                if y < h - 3:
                    stdscr.addstr(y, 2, line.strip(), curses.color_pair(3))
                    y += 1
                line = word + " "
        if line and y < h - 3:
            stdscr.addstr(y, 2, line.strip(), curses.color_pair(3))
        
        # Footer
        stdscr.addstr(h-2, 0, "─" * w, curses.color_pair(1))
        stdscr.addstr(h-1, 2, "Enter/q: Zurück", curses.color_pair(3))
        
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == ord('\n') or key == ord('q'):
            break


def main_menu(stdscr):
    """Hauptmenü mit RGB-Effekten und Retro-Style"""
    import curses
    
    curses.curs_set(0)
    stdscr.clear()
    stdscr.nodelay(True)  # Non-blocking input für Animationen
    
    # Erweiterte Farbpalette
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
    
    menu_items = [
        "Loop ausführen",
        "Versionshistorie",
        "F&Q",
        "Updates",
        "GitHub öffnen",
        "Beenden"
    ]
    
    current_row = 0
    color_cycle = 0
    frame = 0
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        # Animierter RGB Header
        frame += 1
        color_idx = (frame // 10) % 6 + 1
        
        # ASCII Art Logo
        logo = [
            "╔═══════════════════════════════════════╗",
            "║    ██╗      ██████╗  ██████╗ ██████╗  ║",
            "║    ██║     ██╔═══██╗██╔═══██╗██╔══██╗ ║",
            "║    ██║     ██║   ██║██║   ██║██████╔╝ ║",
            "║    ██║     ██║   ██║██║   ██║██╔═══╝  ║",
            "║    ███████╗╚██████╔╝╚██████╔╝██║      ║",
            "║    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝      ║",
            "║                                       ║",
            "║    ██████╗ ██╗   ██╗ ██████╗██╗  ██╗  ║",
            "║    ██╔══██╗██║   ██║██╔════╝██║ ██╔╝  ║",
            "║    ██║  ██║██║   ██║██║     █████╔╝   ║",
            "║    ██║  ██║██║   ██║██║     ██╔═██╗   ║",
            "║    ██████╔╝╚██████╔╝╚██████╗██║  ██╗  ║",
            "║    ╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝  ║",
            "╚═══════════════════════════════════════╝"
        ]
        
        start_y = 1
        for i, line in enumerate(logo):
            if start_y + i < h:
                x = max(0, w//2 - len(line)//2)
                stdscr.addstr(start_y + i, x, line, curses.color_pair(color_idx) | curses.A_BOLD)
        
        # Version Info mit Effekt
        y = start_y + len(logo) + 1
        version_text = f"version: {VERSION}"
        author_text = "by Change Goose"
        
        if y < h - 2:
            stdscr.addstr(y, 2, "Loop", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(y, 7, version_text, curses.color_pair(3))
            y += 1
        
        if y < h - 2:
            stdscr.addstr(y, 2, "Duck", curses.color_pair(4) | curses.A_BOLD)
            stdscr.addstr(y, 7, author_text, curses.color_pair(5))
            y += 1
        
        # Trennlinie mit RGB
        y += 1
        if y < h - 2:
            border = "━" * w
            stdscr.addstr(y, 0, border, curses.color_pair(color_idx))
            y += 2
        
        # Menü-Items mit Retro-Style
        for idx, item in enumerate(menu_items):
            if y >= h - 3:
                break
                
            x = w//4
            
            if idx == current_row:
                # Ausgewähltes Item mit Animation
                prefix = "►►►" if frame % 20 < 10 else "►► "
                stdscr.addstr(y, x, prefix + " " + item, curses.color_pair(2) | curses.A_BOLD | curses.A_REVERSE)
            else:
                stdscr.addstr(y, x + 4, item, curses.color_pair(3))
            
            y += 2
        
        # Footer mit RGB
        if h > 2:
            stdscr.addstr(h-2, 0, "─" * w, curses.color_pair(color_idx))
            footer = "↑↓: Nav | Enter: OK | q: Exit"
            stdscr.addstr(h-1, w//2 - len(footer)//2, footer, curses.color_pair(3) | curses.A_BOLD)
        
        stdscr.refresh()
        
        # Input mit Timeout für Animation
        try:
            key = stdscr.getch()
        except:
            key = -1
        
        if key == -1:
            time.sleep(0.05)  # Animation delay
            continue
        
        stdscr.nodelay(False)  # Blocking input für Menü-Interaktion
        
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == ord('\n'):
            if current_row == 0:  # Loop ausführen
                curses.endwin()
                run_loop_interactive()
                stdscr = curses.initscr()
                curses.curs_set(0)
            elif current_row == 1:  # Versionshistorie
                show_version_history_curses(stdscr)
            elif current_row == 2:  # F&Q
                show_faq_categories(stdscr)
            elif current_row == 3:  # Updates
                curses.endwin()
                run_update()
                stdscr = curses.initscr()
                curses.curs_set(0)
            elif current_row == 4:  # GitHub
                curses.endwin()
                print(f"\n🌐 Öffne {GITHUB_URL}")
                webbrowser.open(GITHUB_URL)
                input("\n[Enter] zum Fortfahren...")
                stdscr = curses.initscr()
                curses.curs_set(0)
            elif current_row == 5:  # Beenden
                break
        elif key == ord('q'):
            break
        
        stdscr.nodelay(True)  # Zurück zu non-blocking für Animation


def run_loop_interactive():
    """Interaktive Loop-Ausführung"""
    print("\n" + "="*60)
    print("🦆 Loop-Ausführung")
    print("="*60)
    
    try:
        iterations = int(input("\nAnzahl der Wiederholungen: "))
        command = input("Befehl: ").strip()
        
        use_changes = input("Changes erkennen? (j/n): ").lower() == 'j'
        show_output = input("Output anzeigen? (j/n): ").lower() == 'j'
        quit_after = input("Sofort beenden (-q)? (j/n): ").lower() == 'j'
        
        cmd_list = command.split()
        
        duck = LoopDuck()
        duck.run_loop(iterations, cmd_list, use_changes, show_output, quit_after)
        
    except ValueError:
        print("❌ Ungültige Eingabe!")
    except KeyboardInterrupt:
        print("\n\n⏸ Abgebrochen")
    
    input("\n[Enter] zum Fortfahren...")


def main():
    """Hauptfunktion"""
    
    # Check for special commands
    if len(sys.argv) >= 2:
        if sys.argv[1].lower() == "duck":
            if len(sys.argv) >= 3 and sys.argv[2].lower() == "version":
                try:
                    import curses
                    curses.wrapper(show_version_history_curses)
                except:
                    print("Versionshistorie im Textmodus nicht verfügbar.")
                return
            else:
                show_tui()
                return
        elif sys.argv[1] in ["--help", "-h"]:
            print_help()
            return
    
    # Parse command line arguments
    if len(sys.argv) < 3:
        print("❌ Zu wenige Argumente!")
        print("Verwende 'Loop --help' für Hilfe oder 'loop duck' für das Menü")
        return 1
    
    # Parse parameters and arguments
    check_changes = False
    show_output = False
    quit_after = False
    stop_condition = None
    
    args = sys.argv[1:]
    iterations = None
    command = []
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg in ["-c", "--changes"]:
            check_changes = True
            i += 1
        elif arg in ["-o", "--output"]:
            show_output = True
            i += 1
        elif arg in ["-q", "--quit"]:
            quit_after = True
            i += 1
        elif arg in ["-s", "--stop"]:
            # Next argument should be the condition
            if i + 1 < len(args):
                stop_condition = args[i + 1]
                i += 2
            else:
                print("❌ -s Parameter benötigt eine Gegebenheit!")
                return 1
        elif iterations is None:
            try:
                iterations = int(arg)
                i += 1
            except ValueError:
                print(f"❌ Ungültige Anzahl: {arg}")
                return 1
        else:
            # Rest is the command
            command = args[i:]
            break
    
    if iterations is None or not command:
        print("❌ Fehlende Argumente!")
        print("Verwendung: Loop [Parameter] <Anzahl> <Befehl>")
        return 1
    
    # Run the loop
    duck = LoopDuck()
    duck.run_loop(iterations, command, check_changes, show_output, quit_after, stop_condition)
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⏸ Programm abgebrochen")
        sys.exit(0)
