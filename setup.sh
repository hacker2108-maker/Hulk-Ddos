#!/bin/bash

# HULK Multi-Tool Launcher
# Author: YourName
# Features:
# - Menu selection (GUI or CLI version)
# - Target input collection
# - Auto-venv setup

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if HULK exists
check_hulk() {
    if [ ! -f "hulk/hulk.py" ] && [ ! -f "hulk_pro_gui.py" ]; then
        echo -e "${RED}[!] Error: No HULK versions found${NC}"
        echo -e "${YELLOW}Please clone the repository first:${NC}"
        echo "git clone https://github.com/grafov/hulk.git"
        exit 1
    fi
}

# Menu function
show_menu() {
    clear
    echo -e "${BLUE}"
    echo " ██░ ██  █    ██  ███▄ ▄███▓"
    echo "▓██░ ██▒ ██  ▓██▒▓██▒▀█▀ ██▒"
    echo "▒██▀▀██░▓██  ▒██░▓██    ▓██░"
    echo "░▓█ ░██ ▓▓█  ░██░▒██    ▒██ "
    echo "░▓█▒░██▓▒▒█████▓ ▒██▒   ░██▒"
    echo " ▒ ░░▒░▒░▒▓▒ ▒ ▒ ░ ▒░   ░  ░"
    echo " ▒ ░▒░ ░░░▒░ ░ ░ ░  ░      ░"
    echo " ░  ░░ ░ ░░░ ░ ░ ░      ░   "
    echo " ░  ░  ░   ░            ░   "
    echo -e "${NC}"
    echo -e "${GREEN}HULK Attack Menu${NC}"
    echo -e "1. Launch GUI Version (Recommended)"
    echo -e "2. Launch Original hulk.py"
    echo -e "3. Exit"
    echo -n -e "${YELLOW}Select an option [1-3]: ${NC}"
}

# Target input function
get_target() {
    echo -n -e "${YELLOW}Enter target URL (e.g., http://example.com): ${NC}"
    read target
    echo -n -e "${YELLOW}Enter port (leave blank for default 80/443): ${NC}"
    read port
    
    if [ -z "$port" ]; then
        if [[ "$target" == https://* ]]; then
            port=443
        else
            port=80
        fi
    fi
}

# Main function
main() {
    check_hulk
    
    while true; do
        show_menu
        read choice
        
        case $choice in
            1)
                if [ -f "hulk_pro_gui.py" ]; then
                    echo -e "${GREEN}[+] Launching GUI version...${NC}"
                    python3 hulk_pro_gui.py
                    break
                else
                    echo -e "${RED}[!] GUI version not found${NC}"
                    sleep 2
                fi
                ;;
            2)
                get_target
                echo -e "${GREEN}[+] Launching hulk.py against $target:$port${NC}"
                
                # Activate venv if exists
                if [ -d "hulk/venv" ]; then
                    source hulk/venv/bin/activate
                fi
                
                # Run with parameters
                cd hulk
                python3 hulk.py "$target" "$port"
                cd ..
                break
                ;;
            3)
                echo -e "${RED}[+] Exiting...${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}[!] Invalid option${NC}"
                sleep 1
                ;;
        esac
    done
}

# Start
main