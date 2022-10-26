import tty

with open('/dev/tty', 'r') as fdr, open('/dev/tty', 'w') as fdw:
    tty.setcbreak(fdr)
    while 1:
        x = fdr.read(1)
        print(ord(x))
