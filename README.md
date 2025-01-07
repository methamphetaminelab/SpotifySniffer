# SpotifySniffer
A bot for downloading tracks and albums from Spotify. Just send a link, and it will download the music and send the files back to the chat. Supports downloading both individual tracks and entire albums.

## Usage

1. Install [spotdl](https://github.com/spotDL/spotify-downloader?ysclid=m5mt3hgz2l868633386) `pip install spotdl`
2. Install ffmpeg `spotdl --download-ffmpeg` or `spotdl --ffmpeg /path/to/ffmpeg`

### telebot
1. Paste your bot token into `config.py`
2. `pip install -r requirements.txt`
3. `python main.py`

### aiogram
1. Paste your bot token into `config.py`
2. `pip install -r requirements.txt`
3. `python aio.py`