# wget --no-cache -O run.sh https://raw.githubusercontent.com/qJake/NFCMusicBox/main/run.sh; sudo chmod +x run.sh; ./run.sh

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
    sudo apt-get install git python3 wget python3-pip python3-dev python3-rpi.gpio -y
    sudo python3 -m pip install flask RPi Mock.GPIO pygame spidev
else
    apt-get update -y
    apt-get install git python3 wget python3-pip python3-dev python3-rpi.gpio -y
    python3 -m pip install flask RPi Mock.GPIO pygame spidev
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