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

__author__ = "Erivando Sena Ramos"
__copyright__ = "Erivando Sena (2016)"
__email__ = "erivandoramos@bol.com.br"
__status__ = "Prototype"

tag1 = "3541237681"
tag2 = "3541300382"

volume_min = 0.0
volume_max = 1.0


class LeitorCartao(threading.Thread):

    nfc = Nfc522()
    numero_cartao = None

    def __init__(self, intervalo=1):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self._sleepperiod = intervalo
        self.name = 'Thread LeitorCartao'

        self.music_player = Player()
        self.stream = self.music_player.get_stream()

    def run(self):
        # Set volumes to 0 and play music
        self.music_player.play()

        print "%s. Run... " % self.name
        while not self._stopevent.isSet():
            self.ler()
            self._stopevent.wait(self._sleepperiod)
        print "%s.Turning off..." % (self.getName(),)

    def obtem_numero_cartao_rfid(self):
        id = None
        try:
            while True:
                id = self.nfc.obtem_nfc_rfid()
                if id:
                    id = str(id).zfill(10)
                    if (len(id) >= 10):
                        self.numero_cartao = id
                        print "Read TAG Number: " + str(self.numero_cartao)
                        return self.numero_cartao
                    else:
                        print "Error TAG Number: " + str(self.numero_cartao)
                        id = None
                        return None
                else:
                    return id
        except Exception as e:
            print e

    def ler(self):
        try:
            if self.obtem_numero_cartao_rfid():
                self.update_volumes(self.numero_cartao, volume_max)
            else:
                self.update_volumes(self.numero_cartao, volume_min)
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

    def turnoff_volumes(self):
        self.music_player.set_volume1(volume_min)
        self.music_player.set_volume2(volume_max)
