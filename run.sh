echo Preparing...
echo

cd /
apt-get update -y
apt-get install git python3 wget python3-pip -y
python3 -m pip install flask GPIO Mock.GPIO

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