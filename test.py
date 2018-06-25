from module.player import Player
import time

music_player = Player()
stream = music_player.stream_tarantella()

music_player.play()

while stream.is_active():
  time.sleep(0.1)

music_player.stop()
