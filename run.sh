# wget --no-cache -O run.sh https://raw.githubusercontent.com/qJake/NFCMusicBox/main/run.sh; sudo chmod +x run.sh; sudo ./run.sh

clear
echo =====================
echo === NFC Music Box ===
echo =====================
echo 
echo Preparing...

apt-get update -y
apt-get install git python3 wget python3-pip python3-dev python3-rpi.gpio libsdl-ttf2.0-0 python3-sdl2 -y
python3 -m pip install flask RPi Mock.GPIO pygame spidev

echo Pulling...
echo 

if [ -d '~/nfc-music-box' ]
then
    echo Cleaning...
    echo    
    ls ~/nfc-music-box -A1 | xargs rm -rf
    cd ..
    rmdir ~/nfc-music-box
fi

git clone https://github.com/qJake/NFCMusicBox.git ~/nfc-music-box

echo Running...
echo
python3 ~/nfc-music-box/main.py &
