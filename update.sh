# TODO: This is pretty aggressive, find a better way to identify just our process.
cd ~

sudo pkill -f python3

sudo rm -f ./run.sh
wget --no-cache -O run.sh https://raw.githubusercontent.com/qJake/NFCMusicBox/main/run.sh
sudo chmod +x run.sh
sudo ./run.sh