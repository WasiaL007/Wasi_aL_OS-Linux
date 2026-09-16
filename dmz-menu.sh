#!/bin/bash

COLS=$(stty size 2>/dev/null | awk '{print $2}')
[[ "$COLS" =~ ^[0-9]+$ ]] || COLS=60
(( COLS > 60 )) && COLS=60
(( COLS < 40 )) && COLS=40

ITEM_WIDTH=26

print_item() {
    local num="$1"
    local label="$2"
    local text="$num) $label"
    local pad_left=$(( (COLS - ITEM_WIDTH) / 2 ))
    (( pad_left < 0 )) && pad_left=0
    printf '%*s%-*s\n' "$pad_left" '' "$ITEM_WIDTH" "$text"
}

center() {
    local text="$1"
    local pad=$(( (COLS - ${#text}) / 2 ))
    (( pad < 0 )) && pad=0
    printf '%*s%s\n' "$pad" '' "$text"
}

border() {
    local i
    for ((i=0; i<COLS; i++)); do printf '═'; done
    echo ""
}

show_menu() {
    clear
    echo ""
    echo -e "\e[1;36m"
    border
    center "⚡ DmZcoder Sub-Menu ⚡"
    border
    echo -e "\e[0m"
    echo ""
    echo -e "\e[1;33m"
    print_item "1" "Website Crack"
    print_item "2" "DMZ BOMBER"
    print_item "3" "DMZ CAM"
    print_item "4" "Cyber Player"
    print_item "5" "DmZcoder ZIP CRACK"
    print_item "6" "DmZ-Phis-Tool"
    print_item "7" "Account Recovery"
    echo -e "\e[0m"
    echo ""
    echo -e "\e[1;36m"
    border
    echo -e "\e[0m"
    echo ""
    echo -e "\e[1;31m"
    print_item "8" "Back to Main Window"
    print_item "0" "Exit"
    echo -e "\e[0m"
    echo ""
    echo -e "\e[1;36m"
    border
    echo -e "\e[0m"
    echo ""
    local prompt="👉 Enter option: "
    local pad=$(( (COLS - ${#prompt}) / 2 ))
    (( pad < 0 )) && pad=0
    printf '\e[1;92m%*s\e[0m' "$pad" ''
    read -p "$prompt" opt
}

run_option() {
    case $opt in
        1)
            echo "⏳ Starting Website Crack..."
            sleep 1
            cd ~/DmZcoder-WEB-CRACK && python dmz_web_crack.py
            ;;
        2)
            echo "⏳ Starting DMZ BOMBER..."
            sleep 1
            cd ~/DMZ-BOMBER && python DMZ-BOMBER.py
            ;;
        3)
            echo "⏳ Starting DMZ CAM..."
            sleep 1
            cd ~/DMZ-CAM-Tool && bash dmzcam.sh
            ;;
        4)
            echo "⏳ Starting Cyber Player..."
            sleep 1
            cd ~/Animation-Studio-Player && python3 -m http.server 8004
            ;;
        5)
            echo "⏳ Starting DmZcoder ZIP CRACK..."
            sleep 1
            cd ~/DmZcoder-ZIP-CRACK && python dmz_zip.py
            ;;
        6)
            echo "⏳ Starting DmZ-Phis-Tool..."
            sleep 1
            cd ~/DmZ-Phis-Tool-clean && python dmzcoder.py
            ;;
        7)
            echo "⏳ Starting Account Recovery..."
            sleep 1
            if [ -d ~/Google-Account-Recovery ]; then
                cd ~/Google-Account-Recovery && python main.py
            elif [ -d ~/DmZcoder-Account-Recovery ]; then
                cd ~/DmZcoder-Account-Recovery && python main.py
            elif [ -d ~/DmZcoder-WEB-CRACK ]; then
                cd ~/DmZcoder-WEB-CRACK && python dmz_web_crack.py
            else
                echo "❌ Account Recovery folder not found"
                sleep 2
            fi
            ;;
        8)
            echo "🔙 Returning to Main Window..."
            sleep 1
            exec bash ~/Wasi_aL_OS-Linux/banner.sh
            ;;
        0)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid option! Try again."
            sleep 1
            ;;
    esac
}

while true; do
    show_menu
    run_option
    echo ""
    read -p "🔙 Press Enter to return..." dummy
done
