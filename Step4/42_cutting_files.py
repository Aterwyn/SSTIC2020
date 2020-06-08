
import struct
import binascii

f = open("output_00.raw","rb")
raw = f.read()
f.close()


f1 = open("extracted/desktop.ini","wb")
f1.write(raw[0x140:0x140+0x7D])
f1.close()

f2 = open("extracted/screensaver.iso","wb")
f2.write(raw[0x300:0x300+0x25F860])
f2.close()

f3 = open("extracted/KeyProvider.dll","wb")
f3.write(raw[0x25FCA0:0x25FCA0 + 0x2391])
f3.close()

f4 = open("extracted/wallpaper.jpg","wb")
f4.write(raw[0x262178:0x262178+0x10E1D])
f4.close()

f5 = open("extracted/KeePass.exe","wb")
f5.write(raw[0x2730D8:0x2730D8+0xAFC00])
f5.close()

f6 = open("extracted/KeePass.ini","wb")
f6.write(raw[0x322E18:0x322E18 + 0x5C])
f6.close()

f7 = open("extracted/Database.kdb","wb")
f7.write(raw[0x322FB8:0x322FB8+0x5AC])
f7.close()

f8 = open("extracted/flag.txt","wb")
f8.write(raw[0x3236A8:])
f8.close()