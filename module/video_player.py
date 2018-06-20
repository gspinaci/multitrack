#!/usr/bin/env python
# -*- coding: utf-8 -*-

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
from threading import Thread

class VideoPlayerWrapper():

  def play(self):
      print('Playing...')
      self.play_thread = VideoPlayer()
      self.play_thread_start_join = Thread(target=self.play_thread.run,)
      self.play_thread_start_join.start()

  def stop(self):
      print('Play Stopped...')
      self.play_thread.terminate()
      # wait for actual termination to close up recording screen 
      self.play_thread_start_join.join()


class VideoPlayer():

  def __init__(self):
    self.running = True  # activated by Start button

  def terminate(self):  # activated by Stop button
    self.running = False
    print('Terminating thread...')

  def run(self):
    omxplayer = OMXPlayer(Path("./video/Slàinte.mp4"))
    time_remaining = omxplayer.duration()
    omxplayer_sleep = 1 # one second sleep sessions below for video to run in loop
    omxplayer.play()
    while self.running:
        time_remaining = time_remaining - omxplayer_sleep
        if time_remaining > 0:
            sleep(omxplayer_sleep)
        print('Can Control = '+str(omxplayer.can_control())) 
        # If can_control() = True, pressing Kivy Stop button will make self.running = False and allow
        # me to take control of this loop and terminate the thread.

    omxplayer.quit()