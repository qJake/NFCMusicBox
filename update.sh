sudo systemctl stop nfcmb.service

cd ~
sudo rm -f ./run.sh
wget --no-cache -O run.sh https://raw.githubusercontent.com/qJake/NFCMusicBox/main/run.sh
sudo chmod +x run.sh
sudo ./run.sh