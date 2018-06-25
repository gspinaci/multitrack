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
    self.volume1 = self.max_volume
    self.volume2 = self.max_volume

  def play(self):
    print "Music starts..."
    self.stream.start_stream()

  def set_volume1(self, volume1):
    self.volume1 = volume1

  def set_volume2(self, volume2):
    self.volume2 = volume2

  def stream_pizzica(self):
    self.pizzica1 = wave.open("pizzica/rithm.wav", 'rb')
    self.pizzica2 = wave.open("pizzica/lead.wav", 'rb')

    def callback(in_data, frame_count, time_info, status):
      data1 = self.pizzica1.readframes(frame_count)
      data2 = self.pizzica2.readframes(frame_count)

      decodeddata1 = numpy.fromstring(data1, numpy.int16)
      decodeddata2 = numpy.fromstring(data2, numpy.int16)

      newdata = (decodeddata1 * self.volume1 + decodeddata2 * self.volume2).astype(numpy.int16)

      return (newdata.tostring(), pyaudio.paContinue)

    self.stream = p.open(format=p.get_format_from_width(self.pizzica1.getsampwidth()),
      channels = self.pizzica1.getnchannels(),
      rate = self.pizzica1.getframerate(),
      output = True,
      stream_callback = callback)

  def stream_tarantella(self):

    def callback(in_data, frame_count, time_info, status):
      data1 = self.tarantella1.readframes(frame_count)
      data2 = self.tarantella2.readframes(frame_count)

      decodeddata1 = numpy.fromstring(data1, numpy.int16)
      decodeddata2 = numpy.fromstring(data2, numpy.int16)

      newdata = (decodeddata1 * self.volume1 + decodeddata2 * self.volume2).astype(numpy.int16)

      return (newdata.tostring(), pyaudio.paContinue)

    self.tarantella1 = wave.open("tarantella/mandolin.wav", 'rb')
    self.tarantella2 = wave.open("tarantella/piano.wav", 'rb')

    self.stream = p.open(format=p.get_format_from_width(self.tarantella1.getsampwidth()),
      channels = self.tarantella1.getnchannels(),
      rate = self.tarantella1.getframerate(),
      output = True,
      stream_callback = callback)

    return self.stream

  def stop(self):
    self.stream.stop_stream()
    self.stream.close()
    p.terminate()
