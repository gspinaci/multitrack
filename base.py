import sys
import time

from module.leitor_cartao import LeitorCartao
from module.video_player import VideoPlayerWrapper

reader_card = LeitorCartao()
video_player_wrapper = VideoPlayerWrapper()

try:
    while True:
        if not reader_card.isAlive():
            video_player_wrapper.play()
            reader_card.start()
except KeyboardInterrupt:
    print "trl+C received! Sending kill to " + reader_card.getName()
    video_player_wrapper.stop()
    if reader_card.isAlive():
        reader_card._stopevent.set()

"""

music_player = Player()
stream = music_player.get_stream()

while stream.is_active():
    music_player.play()

    time.sleep(5)
    print "DRUM only"
    music_player.update_volumes(1,0.2)

    time.sleep(5)
    print "GUITAR only"
    music_player.update_volumes(0.2,1)
"""
