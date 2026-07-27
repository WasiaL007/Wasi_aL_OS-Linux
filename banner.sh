#!/data/data/com.termux/files/usr/bin/bash

RED='\033[1;31m'
GREEN='\033[1;32m'
MAGENTA='\033[1;35m'
BLUE='\033[1;34m'
YELLOW='\033[1;33m'
WHITE='\033[1;37m'
RESET='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FACE_IMAGE="$SCRIPT_DIR/assets/angry-face.png"

COLS="$(stty size 2>/dev/null | awk '{print $2}')"
[[ "$COLS" =~ ^[0-9]+$ ]] || COLS=100
(( COLS < 80 )) && COLS=80

repeat_char() {
    local ch="$1" n="$2" i
    for ((i=0; i<n; i++)); do printf '%s' "$ch"; done
}

center_text() {
    local text="$1"
    local pad=$(( (COLS - ${#text}) / 2 ))
    (( pad < 0 )) && pad=0
    printf '%*s%s\n' "$pad" '' "$text"
}

red_line() {
    printf '%b' "$RED"
    repeat_char '─' "$COLS"
    printf '%b\n' "$RESET"
}

show_face() {
    if command -v chafa >/dev/null 2>&1 && [[ -f "$FACE_IMAGE" ]]; then
        chafa --format=symbols --colors=full --symbols=block \
              --size="${COLS}x20" "$FACE_IMAGE"
        printf '%b' "$RESET"
    else
        center_text "Angry Bird image not found: $FACE_IMAGE"
    fi
}


show_title() {
    printf '%b' "$RED"

    if (( WIDTH >= 92 )); then
        local lines=(
' __        __    _    ____  ___      _    _       __  __ _____ _   _ _____ ____  ___'
' \ \      / /   / \  / ___||_ _|    / \  | |     |  \/  | ____| | | | ____|  _ \|_ _|'
'  \ \ /\ / /   / _ \ \___ \ | |    / _ \ | |     | |\/| |  _| | |_| |  _| | | | | |'
'   \ V  V /   / ___ \ ___) || |   / ___ \| |___  | |  | | |___|  _  | |___| |_| || |'
'    \_/\_/   /_/   \_\____/|___| /_/   \_\_____| |_|  |_|_____|_| |_|_____|____/|___|'
        )
        local row
        for row in "${lines[@]}"; do
            center_text "$row"
        done
    else
        # Mobile-safe fallback keeps the title clear and centred.
        if command -v figlet >/dev/null 2>&1; then
            figlet -f small "WASI AL MEHEDI" 2>/dev/null |
            while IFS= read -r row; do
                center_text "$row"
            done
        else
            center_text "WASI AL MEHEDI"
        fi
    fi

    printf '%b\n' "$RESET"
}

box_row() {
    local color="$1" text="$2"
    local inner=$((COLS - 2))
    local pad=$((inner - ${#text}))
    (( pad < 0 )) && pad=0
    printf '%b│%b%s%*s%b│%b\n' \
        "$RED" "$color" "$text" "$pad" '' "$RED" "$RESET"
}

show_info() {
    local now
    now="$(date '+%a %d %b %Y %H:%M')"

    printf '%b┌' "$RED"
    repeat_char '─' $((COLS - 2))
    printf '┐%b\n' "$RESET"

    box_row "$GREEN"   '  SYSTEM      : ONLINE        | USER : WASI'
    box_row "$MAGENTA" '  OS          : WASI AL OS LINUX v1.7-dev'
    box_row "$GREEN"   '  DEVELOPER   : Wasi aL Mehedi'
    box_row "$YELLOW"  "  DATE        : $now"

    printf '%b└' "$RED"
    repeat_char '─' $((COLS - 2))
    printf '┘%b\n' "$RESET"
}

menu_width() {
    local width
    width="$(stty size 2>/dev/null | awk '{print $2}')"
    [[ "$width" =~ ^[0-9]+$ ]] || width=80
    (( width > 100 )) && width=100
    printf '%s' "$width"
}

menu_border() {
    local width
    width="$(menu_width)"

    printf '%b' "$RED"
    printf '%*s' "$width" '' | tr ' ' '*'
    printf '%b\n' "$RESET"
}

menu_title() {
    local width title left
    width="$(menu_width)"
    title='MAIN MENU - SELECT MODULE'
    left=$(( (width - ${#title}) / 2 ))

    printf '%b%*s%s%b\n' \
        "$YELLOW" "$left" '' "$title" "$RESET"
}

menu_line() {
    local icon="$1"
    local number="$2"
    local label="$3"
    local width

    width="$(menu_width)"

    printf '%b●%b' "$RED" "$RESET"

    printf '\033[4G%s' "$icon"
    printf '\033[9G%b[%02d]%b' "$RED" "$number" "$RESET"
    printf '\033[15G%b%s%b' "$WHITE" "$label" "$RESET"

    printf '\033[%dG%b●%b\n' "$width" "$RED" "$RESET"
}

show_menu() {
    menu_border
    menu_title
    menu_border

    menu_line '🌐' 1  'Network Scan'
    menu_line '🌍' 2  'Web Scanner'
    menu_line '🛡️' 3  'Vulnerability Scanner'
    menu_line '👤' 4  'User Finder (OSINT)'
    menu_line '📁' 5  'Directory Bruteforcer'
    menu_line '🔌' 6  'Port Scanner'
    menu_line '🌐' 7  'DNS Scanner'
    menu_line '🔗' 8  'Subdomain Scanner'
    menu_line '🛠️' 9  'Hash Tools'
    menu_line '🚀' 10 'Payload Generator'
    menu_line '💾' 11 'Save Report'
    menu_line '✏️' 12 'Change Banner'
    menu_line '🚪' 13 'Exit'

    menu_border
}



module_message() {
    printf '\n%b%s module is under development.%b\n' "$YELLOW" "$1" "$RESET"
    read -r -p 'Press Enter to return...'
}

while true; do
    clear
    show_face
    show_title
    show_info
    show_menu

    printf '%bEnter option: %b' "$GREEN" "$RESET"
    read -r option

    case "$option" in
        1|01) module_message 'Network Scan' ;;
        2|02) module_message 'Web Scanner' ;;
        3|03) module_message 'Vulnerability Scanner' ;;
        4|04) module_message 'User Finder (OSINT)' ;;
        5|05) module_message 'Directory Bruteforcer' ;;
        6|06) module_message 'Port Scanner' ;;
        7|07) module_message 'DNS Scanner' ;;
        8|08) module_message 'Subdomain Scanner' ;;
        9|09) module_message 'Hash Tools' ;;
        10) module_message 'Payload Generator' ;;
        11) module_message 'Save Report' ;;
        12) module_message 'Change Banner' ;;
        13) clear; exit 0 ;;
        *) printf '%bInvalid option.%b\n' "$RED" "$RESET"; sleep 1 ;;
    esac
done
