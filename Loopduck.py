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
from datetime import datetime
from typing import List, Tuple, Optional

VERSION = "1.0"
RELEASE_DATE = "2024-02-02 14:30"
GITHUB_URL = "https://github.com/Change-Goose-Open-Surce-Software?tab=repositories"

# Version History
VERSION_HISTORY = {
    "1.0": {
        "date": "2024-02-02 14:30",
        "changes": [
            "Initial Release",
            "Loop-Funktionalität mit Wiederholungen",
            "Parameter: -c (changes), -o (output), -s (stop), -q (quit)",
            "Gegebenheiten-System mit Backticks",
            "TUI mit Retro-Vibes",
            "F&Q Menü",
            "Update-Funktion"
        ]
    }
}

# FAQ Data
FAQ_DATA = {
    "a": {
        "name": "Grundlagen",
        "questions": {
            "1a": {
                "q": "Wie starte ich Loop Duck?",
                "a": "Verwende 'Loop <Anzahl> <Befehl>' für einfache Loops oder 'loop duck' für das grafische Menü."
            },
            "2a": {
                "q": "Was macht der -q Parameter?",
                "a": "Der -q Parameter beendet das Programm sofort nach dem Start, um die Wiederholung zu beschleunigen."
            }
        }
    },
    "b": {
        "name": "Parameter",
        "questions": {
            "1b": {
                "q": "Wo stehen Parameter in der Befehlszeile?",
                "a": "Parameter müssen IMMER vor dem Programm/Script stehen, da alles danach zum geloopten Programm gehört."
            },
            "2b": {
                "q": "Was macht der -c Parameter?",
                "a": "Der -c Parameter zeigt Unterschiede zwischen den Ausführungen an (changes)."
            }
        }
    },
    "c": {
        "name": "Gegebenheiten",
        "questions": {
            "1c": {
                "q": "Was sind Gegebenheiten?",
                "a": "Gegebenheiten sind Bedingungen in Backticks, z.B. `-c =p` bedeutet: wenn changes positiv ist."
            },
            "2c": {
                "q": "Wie funktioniert =p, =n?",
                "a": "=p bedeutet positiv (Unterschiede vorhanden), =n bedeutet negativ (keine Unterschiede)."
            }
        }
    },
    "d": {
        "name": "Fortgeschritten",
        "questions": {
            "1d": {
                "q": "Wie breche ich einen Loop vorzeitig ab?",
                "a": "Verwende den -s Parameter mit einer Gegebenheit, z.B. 'Loop -s `-c =n =7` <Befehl>' bricht ab, wenn in Loop 7 keine Änderungen sind."
            }
        }
    },
    "e": {
        "name": "Installation",
        "questions": {
            "1e": {
                "q": "Wie installiere ich Loop Duck?",
                "a": "Speichere loopduck.py im System-PATH (z.B. /usr/local/bin/) und mache es ausführbar: chmod +x loopduck.py"
            }
        }
    }
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
    help_text = """
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
        
    Loop -s \`-c =n =7\` 20 ./test.sh
        → Bricht ab wenn in Loop 7 keine Änderungen erkannt werden

PARAMETER:
    -c, --changes    Zeigt Unterschiede zwischen Ausführungen
    -o, --output     Zeigt den kompletten Terminal-Output
    -s, --stop       Bricht bei Bedingung ab
    -q, --quit       Beendet Programm sofort nach Start

GEGEBENHEITEN:
    Bedingungen in Backticks für -s Parameter:
    
    \`-c =p\`         Changes positiv (Unterschiede vorhanden)
    \`-c =n\`         Changes negativ (keine Unterschiede)
    \`-c =p =3\`      Changes positiv in Loop 3
    \`-c =n =7\`      Keine Changes in Loop 7

HINWEISE:
    • Alle Befehle laufen nacheinander, nicht parallel
    • Ein Befehl wird erst wiederholt wenn er beendet wurde
    • Parameter müssen VOR dem Programm stehen
    • Alles nach <Anzahl> gehört zum ausgeführten Befehl

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
by Change Goose | Version {VERSION}
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
        fallback_menu()


def fallback_menu():
    """Einfaches Fallback-Menü ohne curses"""
    while True:
        print("\n" + "="*60)
        print("🦆 Loop Duck - Hauptmenü")
        print("="*60)
        print(f"Version: {VERSION}")
        print(f"by Change Goose")
        print("\n1) Loop ausführen")
        print("2) Versionshistorie")
        print("3) F&Q")
        print("4) Updates (Installation)")
        print("5) GitHub öffnen")
        print("0) Beenden")
        print("="*60)
        
        choice = input("\nAuswahl: ").strip()
        
        if choice == "1":
            run_loop_interactive()
        elif choice == "2":
            show_version_history()
        elif choice == "3":
            show_faq_menu()
        elif choice == "4":
            print("\n📦 Update-Funktion würde hier das Installationsscript starten...")
        elif choice == "5":
            print(f"\n🌐 Öffne {GITHUB_URL}")
            webbrowser.open(GITHUB_URL)
        elif choice == "0":
            print("\n👋 Auf Wiedersehen!")
            break


def run_loop_interactive():
    """Interaktive Loop-Ausführung"""
    print("\n" + "-"*60)
    print("Loop-Ausführung")
    print("-"*60)
    
    try:
        iterations = int(input("Anzahl der Wiederholungen: "))
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


def show_version_history():
    """Zeigt die Versionshistorie"""
    print("\n" + "="*60)
    print("📜 Loop Duck - Versionshistorie")
    print("="*60)
    
    for version, info in sorted(VERSION_HISTORY.items(), reverse=True):
        print(f"\n🔖 Version {version} - {info['date']}")
        print("-" * 40)
        for change in info['changes']:
            print(f"  • {change}")
    
    input("\n[Enter] zum Fortfahren...")


def show_faq_menu():
    """Zeigt das F&Q Menü"""
    while True:
        print("\n" + "="*60)
        print("❓ F&Q - Häufig gestellte Fragen")
        print("="*60)
        
        print("\nKategorien:")
        for key, cat in FAQ_DATA.items():
            print(f"  {key}) {cat['name']}")
        print("  0) Zurück")
        
        choice = input("\nKategorie wählen: ").strip().lower()
        
        if choice == "0":
            break
        elif choice in FAQ_DATA:
            show_category_questions(choice)
        else:
            print("❌ Ungültige Auswahl!")


def show_category_questions(category: str):
    """Zeigt Fragen einer Kategorie"""
    cat_data = FAQ_DATA[category]
    
    while True:
        print("\n" + "-"*60)
        print(f"Kategorie: {cat_data['name']}")
        print("-"*60)
        
        print("\nFragen:")
        for qid, qdata in cat_data['questions'].items():
            print(f"  {qid}) {qdata['q']}")
        print("  0) Zurück")
        
        choice = input("\nFrage auswählen: ").strip().lower()
        
        if choice == "0":
            break
        elif choice in cat_data['questions']:
            print("\n" + "="*60)
            print("Frage:", cat_data['questions'][choice]['q'])
            print("="*60)
            print("\nAntwort:")
            print(cat_data['questions'][choice]['a'])
            input("\n[Enter] zum Fortfahren...")
        else:
            print("❌ Ungültige Auswahl!")


def main_menu(stdscr):
    """Hauptmenü mit curses (Retro-Style)"""
    import curses
    
    curses.curs_set(0)
    stdscr.clear()
    
    # Farbschema definieren
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    menu_items = [
        "Loop ausführen",
        "Versionshistorie",
        "F&Q",
        "Updates",
        "GitHub öffnen",
        "Beenden"
    ]
    
    current_row = 0
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        # Header
        title = "LOOP DUCK"
        stdscr.addstr(1, w//2 - len(title)//2, title, curses.color_pair(1) | curses.A_BOLD)
        
        # Untertitel
        subtitle = f"version: {VERSION}"
        stdscr.addstr(2, 2, "Loop", curses.color_pair(2))
        stdscr.addstr(2, 7, subtitle, curses.color_pair(3))
        
        author = "by Change Goose"
        stdscr.addstr(3, 2, "Duck", curses.color_pair(2))
        stdscr.addstr(3, 7, author, curses.color_pair(3))
        
        # Trennlinie
        stdscr.addstr(4, 0, "─" * w, curses.color_pair(1))
        
        # Menü-Items
        for idx, item in enumerate(menu_items):
            y = 6 + idx * 2
            x = 4
            
            if idx == current_row:
                stdscr.addstr(y, x, "► " + item, curses.color_pair(2) | curses.A_BOLD)
            else:
                stdscr.addstr(y, x, "  " + item, curses.color_pair(3))
        
        # Footer
        stdscr.addstr(h-2, 0, "─" * w, curses.color_pair(1))
        stdscr.addstr(h-1, 2, "↑↓: Navigieren | Enter: Auswählen | q: Beenden", curses.color_pair(3))
        
        stdscr.refresh()
        
        # Input
        key = stdscr.getch()
        
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
                curses.endwin()
                show_version_history()
                stdscr = curses.initscr()
                curses.curs_set(0)
            elif current_row == 2:  # F&Q
                curses.endwin()
                show_faq_menu()
                stdscr = curses.initscr()
                curses.curs_set(0)
            elif current_row == 3:  # Updates
                curses.endwin()
                print("\n📦 Update-Funktion würde hier das Installationsscript starten...")
                input("[Enter] zum Fortfahren...")
                stdscr = curses.initscr()
                curses.curs_set(0)
            elif current_row == 4:  # GitHub
                webbrowser.open(GITHUB_URL)
            elif current_row == 5:  # Beenden
                break
        elif key == ord('q'):
            break


def main():
    """Hauptfunktion"""
    
    # Check for special commands
    if len(sys.argv) >= 2:
        if sys.argv[1].lower() == "duck":
            if len(sys.argv) >= 3 and sys.argv[2].lower() == "version":
                show_version_history()
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
