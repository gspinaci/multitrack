#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class in Python 2.7 that executes a Thread for reading RFID tags.
Credits and License: Created by Erivando Sena

 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License.
"""

import threading
import time

from time import sleep
from module.nfc_522 import Nfc522
from module.player import Player

tag1 = "3541237681"
tag2 = "3541300382"

bottle1 = "2809470880"
bottle2 = "795038986"

readed_tags = list()

class LeitorCartao(threading.Thread):

    nfc = Nfc522()
    numero_cartao = None

    def __init__(self, intervalo=0.1):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self._sleepperiod = intervalo
        self.name = 'Thread LeitorCartao'

        self.music_player = Player()

    def run(self):
        # Set volumes to 0 and play music
        self.stream = self.music_player.stream_pizzica()
        self.music_player.play()

        print "%s. Run... " % self.name
        while not self._stopevent.isSet():
            self.ler()
            self._stopevent.wait(self._sleepperiod)
        print "%s.Turning off..." % (self.getName(),)

    def obtem_numero_cartao_rfid(self):
        id = None
        try:
            id = self.nfc.obtem_nfc_rfid()
            return id
        except Exception as e:
            print e

    def ler(self):
        try:
            read_values = self.obtem_numero_cartao_rfid()

            print read_values

            # Clear the list
            del readed_tags[:]

            if read_values[0] is not None:
                readed_tags.append(read_values[0])

            if read_values[1] is not None:
                readed_tags.append(read_values[1])

            print readed_tags

        except Exception as e:
            print e

    def valida_cartao(self, numero):
        try:
            print "I make interesting operations here with the tag:" + str(numero)
        except Exception as e:
            print e

    def update_volumes(self, numero, volume):
        if numero == tag1:
            self.music_player.set_volume1(volume)
        elif numero == tag2:
            self.music_player.set_volume2(volume)
