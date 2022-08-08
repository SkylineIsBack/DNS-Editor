#!/bin/bash

echo "Checking python version"
pythoninstalled="$(python3 -V | cut -d"." -f1)"
if [[ "$pythoninstalled" == "Python 3" ]];
then
    echo "Correct python version is installed."
else
    echo "Correct python version is not installed."
    exit 1
fi
echo "Starting installation"
sudo mkdir /usr/share/DNSEditor && sudo mv DNSEditor.py /usr/share/DNSEditor/ && sudo mv DNSEditor.ui /usr/share/DNSEditor/ && sudo mv DNSEditor.png /usr/share/icons/ && sudo echo -e "[Desktop Entry]\\n\\nType=Application\\nVersion=1.0\\nName=DNS Editor\\nComment=Edit DNS at ease.\\nExec=python3 /usr/share/DNSEditor/DNSEditor.py\\nIcon=/usr/share/icons/DNSEditor.png\\nTerminal=false\\nCategories=Utility" >> DNSEditor.desktop && sudo mv DNSEditor.desktop /usr/share/applications/ && sudo chmod +x /usr/share/applications/DNSEditor.desktop && echo "Completed half of the installation"
mkdir /home/$USER/.config/DNSEditor && cd /home/$USER/.config/DNSEditor/ && touch currentDNS.txt && touch DNSList.txt && echo "disabled" >> state.txt && echo "$(nmcli dev show | grep DNS | cut -d":" -f2 | sed 's/^ *//g')" >> defaultDNS.txt && echo "Completed installation"