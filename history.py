


class History_Suggest:

    def __parse_history_file(self):
        self.history_list = []
        with open(self.__history_file, 'r', errors='ignore') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith(':'):
                    time_str, *command_str = line.split(';')
                    command_str = ''.join(command_str).strip('\n')
                    time_str = int(time_str.split(':')[1].strip())
                    self.history_list.append(
                        [time_str, command_str]
                    )
                else:
                    self.history_list[-1][1] += '\n' + line

    def __init__(self):
        self.__history_file = '/root/.zsh_history'
        self.__parse_history_file()

    def get_suggest(self, _str, count=10):
        res = set()
        for history in reversed(self.history_list):
            if _str[0] == history[1][0] and _str in history[1]:
                res.add(history[1].replace(_str, f'\033[1;32m{_str}\033[0m'))
            if len(res) >= count:
                return list(res)
        return list(res)



if __name__ == '__main__':
    print(History_Suggest().get_suggest('systemctl'))