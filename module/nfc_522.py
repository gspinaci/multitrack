#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class in Python 2.7 for simultaneous reading of RFID tags through two modules
RFID-RC522 using the SPI interface of Raspberry Pi through the MFRC522 driver.

Credits and License: Created by Mario Gómez, adapted by Erivando Sena(2016)

 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License.
"""

import signal
from module.MFRC522 import MFRC522
from module.pinos import PinoControle

__author__ = "Erivando Sena Ramos (Adaptations)"
__copyright__ = "Mario Gómez"
__email__ = "erivandoramos@bol.com.br"
__status__ = "Prototype"

class Nfc522(object):
    
    pc = PinoControle()
    MIFAREReader = None
    RST1 = 22 #GPIO
    RST2 = 27 #GPIO
    SPI_DEV0 = '/dev/spidev0.0'
    SPI_DEV1 = '/dev/spidev0.1'
    
    def obtem_nfc_rfid(self, autenticacao=False):
        try:
            result1 = None
            result2 = None
            
            self.MIFAREReader = MFRC522(self.RST1, self.SPI_DEV0)
            (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
            
            if status == self.MIFAREReader.MI_OK:
                result1 = self.obtem_tag(self.MIFAREReader, status, uid, autenticacao)
            # else:
            #     self.pc.atualiza(self.RST1, self.pc.baixo())

            self.MIFAREReader = MFRC522(self.RST2, self.SPI_DEV1)
            (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
            
            if status == self.MIFAREReader.MI_OK:
                result2 = self.obtem_tag(self.MIFAREReader, status, uid, autenticacao)
            # else:
            #     self.pc.atualiza(self.RST2, self.pc.baixo())

            return (result1, result2)

        except Exception as e:
            print e
        finally:
            self.MIFAREReader.fecha_spi()
			
    def obtem_tag(self, MIFAREReader, status, uid, autenticacao):
        try:
			if autenticacao:
				# Chave padrão para a autenticação
				key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
				MIFAREReader.MFRC522_SelectTag(uid)
				status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
				if status == MIFAREReader.MI_OK:
					MIFAREReader.MFRC522_Read(8)
					MIFAREReader.MFRC522_StopCrypto1()
				else:
					print "Erro na autenticação!"
					return None
			tag_hexa = ''.join([str(hex(x)[2:4]).zfill(2) for x in uid[:-1][::-1]]) #Returns in hexadecimal
			return int(tag_hexa.upper(), 16) #Returns in decimal
        except Exception as e:
            print e
			