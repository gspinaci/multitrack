#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyaudio
import wave
import numpy

p = pyaudio.PyAudio()

class Player():

  max_volume = 1.0
  min_volume = 0.0

  def __init__(self):
    self.volume1 = self.min_volume
    self.volume2 = self.min_volume

  def play(self):
    self.stream.start_stream()

  def set_volume1(self, volume1):
    self.volume1 = volume1

  def set_volume2(self, volume2):
    self.volume2 = volume2

  def init_stream(self):
    def callback(in_data, frame_count, time_info, status):
      data1 = self.sound1.readframes(frame_count)
      data2 = self.sound2.readframes(frame_count)

      decodeddata1 = numpy.fromstring(data1, numpy.int16)
      decodeddata2 = numpy.fromstring(data2, numpy.int16)

      newdata = (decodeddata1 * self.volume1 + decodeddata2 * self.volume2).astype(numpy.int16)

      return (newdata.tostring(), pyaudio.paContinue)

    self.stream = p.open(format=p.get_format_from_width(self.sound1.getsampwidth()),
      channels = self.sound1.getnchannels(),
      rate = self.sound1.getframerate(),
      output = True,
      stream_callback = callback)

  def stream_pizzica(self):
    self.stop()

    self.sound1 = wave.open("pizzica/rithm.wav", 'rb')
    self.sound2 = wave.open("pizzica/lead.wav", 'rb')

    self.init_stream()
    self.play()

  def stream_tarantella(self):
    self.stop()

    self.sound1 = wave.open("tarantella/mandolin.wav", 'rb')
    self.sound2 = wave.open("tarantella/piano.wav", 'rb')

    self.init_stream()
    self.play()

  def stop(self):
    if hasattr(self, 'stream'):
      self.stream.stop_stream()
      self.stream.close()
