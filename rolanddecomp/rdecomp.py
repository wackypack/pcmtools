import binascii
from os import getcwd
from os.path import join
from struct import pack
from sys import argv

if len(argv) != 5:
    print("Invalid arguments\n\nUsage:\npython rdecomp.py [soundbank] [comp table address] [comp table len] [sample address]\n\n")
    print("soundbank: Binfile containing waveforms\ncomp table address: Address of companding table for sample\ncomp table len: Length of companding table for sample\nsample address: Address of waveform")

if len(argv) == 5:
    sb = argv[1]
    tabaddr = int(argv[2])
    tablen = int(argv[3])
    sampaddr = int(argv[4])

binfile=open(join(getcwd(), sb),"rb")
decompfile=open(join(getcwd(),"rolandcompand.bin"),"rb")
decomptab=decompfile.read()

binfile.seek(tabaddr)
comptable=str(binascii.hexlify(binfile.read(tablen)))[2:-1]
binfile.seek(sampaddr)
waveform=binfile.read(tablen*32)
# print(binascii.hexlify(binfile.read(tablen)))

outbin=open(join(getcwd(), str(sampaddr)), "wb")
for x in range(tablen*2):
    fact=int(comptable[x])
    for y in range(16):
        sam=waveform[(x*16)+y]
        dcadd=sam*2+(fact*512)
        ws=decomptab[dcadd:dcadd+2]
        outbin.write(ws)
