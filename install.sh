#!/data/data/com.termux/files/usr/bin/bash

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

GREEN="\033[1;32m"
CYAN="\033[1;36m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
RESET="\033[0m"

BANNER_SOURCE="$SCRIPT_DIR/banner.sh"
BANNER_TARGET="$HOME/.termux_banner.sh"
RUN_FILE="$SCRIPT_DIR/run.py"

BANNER_COMMAND='[ -f "$HOME/.termux_banner.sh" ] && bash "$HOME/.termux_banner.sh"'

show_logo() {
    if [ -f "$BANNER_SOURCE" ]; then
        bash "$BANNER_SOURCE"
    else
        clear
        echo -e "${YELLOW}"
        cat <<'LOGO'
 _      _____   ________  ___   __
| | /| / / _ | / __/  _/ / _ | / /
| |/ |/ / __ |_\ \_/ /  / __ |/ /__
|__/|__/_/ |_/___/___/ /_/ |_/____/
LOGO
        echo -e "${RESET}"
    fi
}

add_banner_to_shell() {
    local shell_file="$1"

    touch "$shell_file"

    if ! grep -Fqx "$BANNER_COMMAND" "$shell_file" 2>/dev/null; then
        printf '\n%s\n' "$BANNER_COMMAND" >> "$shell_file"
    fi
}

clear

echo -e "${GREEN}"
echo "============================================================"
echo "              WASI AL OS LINUX v1.7"
echo "                 FINAL INSTALLER"
echo "============================================================"
echo -e "${RESET}"

echo -e "${CYAN}[1/4] Checking required files...${RESET}"

if [ ! -f "$BANNER_SOURCE" ]; then
    echo -e "${RED}[ERROR] banner.sh not found.${RESET}"
    echo "Expected: $BANNER_SOURCE"
    exit 1
fi

if [ ! -f "$RUN_FILE" ]; then
    echo -e "${RED}[ERROR] run.py not found.${RESET}"
    echo "Expected: $RUN_FILE"
    exit 1
fi

echo -e "${GREEN}[OK] Project files found.${RESET}"

echo
echo -e "${CYAN}[2/4] Installing required packages...${RESET}"

if command -v pkg >/dev/null 2>&1; then
    pkg update -y
    pkg install python -y
else
    echo -e "${YELLOW}[NOTICE] Termux pkg command not found.${RESET}"
    echo "Continuing with the existing Python installation..."
fi

echo
echo -e "${CYAN}[3/4] Installing WASI AL startup banner...${RESET}"

cp -f "$BANNER_SOURCE" "$BANNER_TARGET"
chmod +x "$BANNER_TARGET"

add_banner_to_shell "$HOME/.bashrc"
add_banner_to_shell "$HOME/.zshrc"

echo -e "${GREEN}[OK] Startup banner installed.${RESET}"

echo
echo -e "${CYAN}[4/4] Finalizing WASI AL OS Linux v1.7...${RESET}"

chmod +x "$RUN_FILE"
chmod +x "$BANNER_SOURCE"

if [ -f "$SCRIPT_DIR/assets/angry-face.png" ]; then
    echo -e "${GREEN}[OK] Angry Bird image found.${RESET}"
else
    echo -e "${YELLOW}[NOTICE] Angry Bird image not found.${RESET}"
    echo "Expected:"
    echo "$SCRIPT_DIR/assets/angry-face.png"
fi

echo
echo -e "${GREEN}============================================================${RESET}"
echo -e "${GREEN}        WASI AL OS LINUX v1.7 READY${RESET}"
echo -e "${GREEN}============================================================${RESET}"
echo
echo -e "${CYAN}Launch command:${RESET}"
echo
echo "    python run.py"
echo

read -r -p "Press Enter to launch WASI AL OS v1.7..."

exec python "$RUN_FILE"
