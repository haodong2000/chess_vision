# -*- coding: utf-8 -*-

import Global_Params


class PlayChess(object):
    def _init_(self):
        self.Name = "LHD"
        self.Age = "20"
        self.Sex = "male"

    class Step(object):
        def _init_(self, chessNum, chessNumber, camp, PosX, PosY,
                     isKill, killNum, killNumber):
            self._chessNum = chessNum
            self._chessNumber = chessNumber
            self._camp = camp
            self._PosX = PosX
            self._PosY = PosY
            self._isKill = isKill
            self._killNum = killNum
            self._killNumber = killNumber

        def display(self):
            print("Num      = ", self._chessNum)
            print("Number   = ", self._chessNumber)
            Camp = ""
            if self._camp:
                Camp = "Red"
            else:
                Camp = "Black"
            print("Camp     = ", Camp)
            print("PosX     = ", self._PosX)
            print("PosY     = ", self._PosY)
            Kill = ""
            if self._isKill:
                Kill = "True"
            else:
                Kill = "False"
            print("Kill   = ", Kill)
            if self._isKill:
                print("K_Num    = ", self._killNum)
                print("K_Number = ", self._killNumber)


