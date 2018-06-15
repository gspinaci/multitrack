#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyaudio
import wave
import numpy

p = pyaudio.PyAudio()

class Player():

  def __init__(self):
    self.sound1 = wave.open("pizzica/rithm.wav", 'rb')
    self.sound2 = wave.open("pizzica/lead.wav", 'rb')
    #self.sound3 = wave.open("pizzica/rithm.wav", 'rb')
    self.volume1 = 0.05
    self.volume2 = 0.05

    def callback(in_data, frame_count, time_info, status):
      data1 = self.sound1.readframes(frame_count)
      data2 = self.sound2.readframes(frame_count)
      #data3 = self.sound3.readframes(frame_count)

      decodeddata1 = numpy.fromstring(data1, numpy.int16)
      decodeddata2 = numpy.fromstring(data2, numpy.int16)
      #decodeddata3 = numpy.fromstring(data3, numpy.int16)

      newdata = (decodeddata1 * self.volume1 + decodeddata2 * self.volume2).astype(numpy.int16)

      return (newdata.tostring(), pyaudio.paContinue)

    # open stream using callback (3)
    self.stream = p.open(format=p.get_format_from_width(self.sound1.getsampwidth()),
      channels = self.sound1.getnchannels(),
      rate = self.sound1.getframerate(),
      output = True,
      stream_callback = callback)

  def get_stream(self):
    return self.stream

  def play(self):
    print "Music starts..."
    self.stream.start_stream()

  def set_volume1(self, volume1):
    print "Set AUDIO1 volume to " + str(volume1)
    self.volume1 = volume1

  def set_volume2(self, volume2):
    print "Set AUDIO2 volume to " + str(volume2)
    self.volume2 = volume2

  def stop(self):
    self.stream.stop_stream()
    self.stream.close()
    self.sound1.close()
    self.sound2.close()
