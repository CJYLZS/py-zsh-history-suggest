import os
import tty


def get_terminal_size():
    try:
        tmp = os.get_terminal_size()
    except:
        return int(os.environ["LINES"]), int(os.environ["COLUMNS"])
    return tmp.lines, tmp.columns


def get_cursor_pos():
    # x: line_index
    # y: column_index
    x, y = shell()[2:].split(';')
    return int(x), int(y)


def shell():
    # shell = \
    # '''
    # echo -ne '\u001b[6n' > /dev/tty
    # read -t 1 -s -d 'R' pos < /dev/tty
    # pos="${pos##*\[}"
    # row="$(( ${pos%;*} -1 ))"
    # col="$(( ${pos#*;} -1 ))"
    # echo $row $col
    # '''
    with open('/dev/tty', 'w') as f:
        f.write('\u001b[6n')
    with open('/dev/tty', 'r') as f:
        tty.setcbreak(f)
        tmp = ''
        while True:
            x = f.read(1)
            if x == 'R':
                break
            tmp += x
    return tmp


if __name__ == '__main__':
    print(get_cursor_pos())
