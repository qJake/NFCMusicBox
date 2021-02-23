# wget --no-cache -O run.sh https://raw.githubusercontent.com/qJake/NFCMusicBox/main/run.sh; sudo chmod +x run.sh; ./run.sh

clear
echo =====================
echo === NFC Music Box ===
echo =====================
echo 
read -p $'Does this system require sudo? [y/N] ' needsudo

echo Preparing...
cd /
if [ "$needsudo" = "y" ]
then
    sudo echo Sudo elevated.
    sudo apt-get update -y
    sudo apt-get install git python3 wget python3-pip python3-dev python3-rpi.gpio libsdl-ttf2.0-0 python3-sdl2 -y
    sudo python3 -m pip install flask RPi Mock.GPIO pygame spidev
else
    apt-get update -y
    apt-get install git python3 wget python3-pip python3-dev python3-rpi.gpio libsdl-ttf2.0-0 python3-sdl2 -y
    python3 -m pip install flask RPi Mock.GPIO pygame spidev
fi

echo
echo Pulling...
echo


cd ~

if [ -d '~/nfc-music-box' ]
then
    cd nfc-music-box
    ls -A1 | xargs rm -rf
    cd ..
    rmdir nfc-music-box
fi

git clone https://github.com/qJake/NFCMusicBox.git nfc-music-box
cd nfc-music-box

echo
echo Running...
echo

python3 main.py