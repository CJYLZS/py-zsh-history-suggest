from multiprocessing import current_process
import os
import re
import sys
import tty

use_async = True

try:
    import asyncio
    import aiofiles
except ModuleNotFoundError:
    use_async = False

from terminal import get_cursor_pos, get_terminal_size
from history import History_Suggest

buffer = []
current_suggestion_list = []
current_suggestion_pos = 0
backspace = '\b \b'
cursor_pos = get_cursor_pos()
terminal_size = get_terminal_size()
left_lines = terminal_size[0] - cursor_pos[0]
hs = History_Suggest()


def handle_backspace():
    if len(buffer) > 0:
        buffer.pop()
    return backspace


def handle_enter():
    # Regex for ANSI colour codes
    ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
    if current_suggestion_pos == len(current_suggestion_list):
        sys.stdout.write(''.join(buffer))
    else:
        sys.stdout.write(
            re.sub(ANSI_RE, "", current_suggestion_list[current_suggestion_pos]))
    return "".join([backspace for _ in range(len(buffer))])


def indicate():
    _str = '\n ' * (len(current_suggestion_list))
    sys.stderr.write(f"\033[s{_str}\033[u")
    if current_suggestion_pos == len(current_suggestion_list):
        return
    _str = '\n' * (current_suggestion_pos + 1) + "\033[1;32m>\033[0m"
    sys.stderr.write(f"\033[s{_str}\033[u")


def handle_alt_j():
    global current_suggestion_pos
    current_suggestion_pos += 1
    current_suggestion_pos %= len(current_suggestion_list) + 1
    indicate()


def handle_alt_k():
    global current_suggestion_pos
    current_suggestion_pos -= 1
    if current_suggestion_pos < 0:
        current_suggestion_pos = len(current_suggestion_list)
    indicate()


_handle_dict = {
    127: handle_backspace,
    10: handle_enter,
    27: {
        106: handle_alt_j,
        107: handle_alt_k
    },
}
# callback = lambda:0


def clear_suggestions():
    _str = "\n".join(" " * terminal_size[1] for _ in range(left_lines))
    sys.stderr.write(f"\033[s\n{_str}\033[u")


def callback():
    global current_suggestion_pos, current_suggestion_list
    # sys.stderr.write(f'\033[s\n{"".join(buffer)}\033[u')
    clear_suggestions()
    if len(buffer) == 0:
        return
    res = hs.get_suggest(''.join(buffer), left_lines)
    current_suggestion_list = res
    current_suggestion_pos = len(current_suggestion_list)
    _str_res = '\n  '.join(res)
    sys.stderr.write(f"\033[s\n  {_str_res}\033[u")


async def async_main():
    async with aiofiles.open('/dev/tty', 'r') as fdr, aiofiles.open('/dev/tty', 'w') as fdw:
        tty.setcbreak(fdr)
        modify = False
        while True:
            x = await fdr.read(1)
            ordx = ord(x)
            if ordx == 27:
                modify = True
                continue
            if modify:
                modify = False
                if ordx in _handle_dict[27]:
                    _handle_dict[27][ordx]()
                continue

            if ordx in _handle_dict:
                x = _handle_dict[ordx]()
                if not x:
                    continue
            else:
                buffer.append(x)
            await fdw.write(x)
            await fdw.flush()
            if ordx == 10:
                break
            callback()
    clear_suggestions()
    return 0


def sync_main():
    with open('/dev/tty', 'r') as fdr, open('/dev/tty', 'w') as fdw:
        tty.setcbreak(fdr)
        while 1:
            x = fdr.read(1)
            ordx = ord(x)
            if ordx in _handle_dict:
                x = _handle_dict[ordx]()
            else:
                buffer.append(x)
            fdw.write(x)
            fdw.flush()
            if ordx == 10:
                break
            callback()
    clear_suggestions()
    return 0


def main():
    if use_async:
        ret = asyncio.run(async_main())
    else:
        ret = sync_main()
    return ret


if __name__ == '__main__':
    sys.exit(main())
