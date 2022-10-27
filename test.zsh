

function test(){
    BUFFER=$(LINES=${LINES} COLUMNS=${COLUMNS} `which python3` main.py)
    CURSOR=$#BUFFER
    zle -R -c
}

zle -N test

bindkey '^R' test