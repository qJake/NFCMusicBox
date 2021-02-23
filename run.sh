# wget -O - https://raw.githubusercontent.com/qJake/NFCMusicBox/main/run.sh | bash

echo =====================
echo === NFC Music Box ===
echo =====================
echo 
read -p $'Does this system require sudo? [y/N] ' needsudo

echo Preparing...
echo
cd /
if [ "$needsudo" = "y" ]
then
    sudo echo Elevated
    sudo apt-get update -y
    sudo apt-get install git python3 wget python3-pip -y
    sudo python3 -m pip install flask RPi Mock.GPIO pygame
else
    apt-get update -y
    apt-get install git python3 wget python3-pip -y
    python3 -m pip install flask RPi Mock.GPIO pygame
fi

echo
echo Pulling...
echo

cd ~
git clone https://github.com/qJake/NFCMusicBox.git nfc-music-box
cd nfc-music-box

echo
echo Running...
echo

python3 main.py