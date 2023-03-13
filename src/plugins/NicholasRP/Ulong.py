from __future__ import annotations
class Ulong(object):
    def __init__(self, integer:int):
        self.byte64 = ["0" for i in range(64)]
        binary_string = str(bin(integer))[2:]
        for i in range(64):
            if len(binary_string) - 64 + i >= 0:
                self.byte64[i] = binary_string[len(binary_string) - 64 + i]

    def __lshift__(self, shift: int) -> Ulong:
        output = Ulong(int(self))
        i = 0
        while i < 64:
            if i + shift < 64:
                output.byte64[i] = output.byte64[i + shift]
            else:
                output.byte64[i] = "0"
            i += 1
        return output

    def __int__(self):
        return int("".join(self.byte64), 2)
    
    def __float__(self):
        return float(int(self))

    def __str__(self):
        return "".join(self.byte64)

    def __xor__(self, other: Ulong):
        output = Ulong(0)
        for i in range(64):
            output.byte64[i] = str(int(self.byte64[i]) ^ int(other.byte64[i]))
        return output

    def __eq__(self, other: Ulong):
        self.byte64 = other.byte64

    def __call__(self, integer:int):
        self.__init__(integer)
        return self