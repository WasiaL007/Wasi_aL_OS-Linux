#!/data/data/com.termux/files/usr/bin/bash

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

GREEN="\033[1;32m"
CYAN="\033[1;36m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
RESET="\033[0m"

APK_NAME="WASI_AL_OS_Termux_v1.5.apk"
APK_PATH="$SCRIPT_DIR/$APK_NAME"
APK_URL="https://github.com/WasiaL007/Wasi_aL_OS-Termux/releases/download/v1.6/WASI_AL_OS_Termux_v1.5.apk"
BANNER_SOURCE="$SCRIPT_DIR/banner.sh"
BANNER_TARGET="$HOME/.termux_banner.sh"
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

    if ! grep -Fqx "$BANNER_COMMAND" "$shell_file"; then
        printf '\n%s\n' "$BANNER_COMMAND" >> "$shell_file"
    fi
}

show_logo

echo -e "${GREEN}=================================================${RESET}"
echo -e "${YELLOW}          WASI AL OS v1.6 FINAL INSTALLER${RESET}"
echo -e "${CYAN}               Developed by Wasi aL${RESET}"
echo -e "${GREEN}=================================================${RESET}"
echo

echo -e "${CYAN}[1/4] Updating package lists...${RESET}"
pkg update -y

echo
echo -e "${CYAN}[2/4] Installing required packages...${RESET}"
pkg install wget python -y

echo
echo -e "${CYAN}[3/4] Installing the WASI AL startup banner...${RESET}"

if [ ! -f "$BANNER_SOURCE" ]; then
    echo -e "${RED}[ERROR] banner.sh was not found in:${RESET}"
    echo "$SCRIPT_DIR"
    exit 1
fi

cp -f "$BANNER_SOURCE" "$BANNER_TARGET"
chmod +x "$BANNER_TARGET"

add_banner_to_shell "$HOME/.bashrc"
add_banner_to_shell "$HOME/.zshrc"

echo -e "${GREEN}[OK] Startup banner installed.${RESET}"

echo
echo -e "${CYAN}[4/4] Preparing the Android APK...${RESET}"

if [ -s "$APK_PATH" ]; then
    echo -e "${GREEN}[OK] APK already exists and is not empty.${RESET}"
else
    rm -f "$APK_PATH"
    echo -e "${YELLOW}Downloading $APK_NAME...${RESET}"

    if ! wget --show-progress -O "$APK_PATH" "$APK_URL"; then
        echo -e "${RED}[ERROR] APK download failed.${RESET}"
        rm -f "$APK_PATH"
        exit 1
    fi

    if [ ! -s "$APK_PATH" ]; then
        echo -e "${RED}[ERROR] Downloaded APK is empty.${RESET}"
        rm -f "$APK_PATH"
        exit 1
    fi

    echo -e "${GREEN}[OK] APK downloaded successfully.${RESET}"
fi

echo
echo -e "${CYAN}Opening Android Package Installer...${RESET}"

INSTALLER_OPENED=0

if command -v termux-open >/dev/null 2>&1; then
    if termux-open --view "$APK_PATH" >/dev/null 2>&1; then
        INSTALLER_OPENED=1
    fi
fi

if [ "$INSTALLER_OPENED" -eq 0 ]; then
    if am start \
        -a android.intent.action.VIEW \
        -d "file://$APK_PATH" \
        -t "application/vnd.android.package-archive" \
        >/dev/null 2>&1; then
        INSTALLER_OPENED=1
    fi
fi

if [ "$INSTALLER_OPENED" -eq 1 ]; then
    echo -e "${GREEN}[OK] Android Package Installer opened.${RESET}"
else
    echo -e "${YELLOW}[NOTICE] The installer could not open automatically.${RESET}"
    echo "Open your file manager and install:"
    echo "$APK_PATH"
fi

echo
echo -e "${YELLOW}Complete the Android installation, then return to Termux.${RESET}"
read -r -p "Press Enter to launch WASI AL OS..."

show_logo

if [ -f "$SCRIPT_DIR/run.py" ]; then
    python "$SCRIPT_DIR/run.py"
else
    echo -e "${RED}[ERROR] run.py was not found in:${RESET}"
    echo "$SCRIPT_DIR"
    exit 1
fi
