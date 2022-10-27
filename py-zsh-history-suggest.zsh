

function test(){
    BUFFER=$(LINES=${LINES} COLUMNS=${COLUMNS} /usr/bin/suggest)
    CURSOR=$#BUFFER
    zle -R -c
}

zle -N test

bindkey '^R' test