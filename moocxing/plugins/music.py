import requests
import os
import random
import ffmpeg

from moocxing.plugins.sdk import AbstractPlugin


class Plugin(AbstractPlugin):
    SLUG = "music"

    def _getMusicId(self, keyword):
        url = "http://music.sliot.top/search?keywords=" + str(keyword)
        res = requests.get(url)
        return res.json()["result"]["songs"][0]["id"]

    def getMusicRankings(self):
        url = "http://music.sliot.top/personalized/newsong"
        res = requests.get(url)
        return res.json()["result"][random.randint(0, 9)]["id"]

    def getMusicUrl(self, keyword):
        url = "http://music.sliot.top/song/url?id=" + str(self._getMusicId(keyword))
        res = requests.get(url)
        return res.json()["data"][0]["url"]

    def downMusic(self, keyword):
        try:
            if keyword == "":
                keyword = self.getMusicRankings()
            musicUrl = self.getMusicUrl(keyword)
        except:
            keyword = self.getMusicRankings()
            musicUrl = self.getMusicUrl(keyword)

        print(f"wget {musicUrl} -O music.mp3")

        os.system(f"wget {musicUrl} -O music.mp3")
        ffmpeg.run(ffmpeg.output(ffmpeg.input('music.mp3'), 'music.wav'), quiet=True, overwrite_output=True)

    def handle(self, query):
        musicName = self.nlp.getMusicName(query)
        self.say(f"正在为你准备{musicName}")
        self.downMusic(musicName)
        self.playThread("music.wav")

    def isValid(self, query):
        return any(word in query for word in ["听", "播放", "首", "歌"])
