

function test(){
    # python3 test.py
    # LBUFFER=$(</tmp/test)
    BUFFER=$(LINES=${LINES} COLUMNS=${COLUMNS} python3 main.py)
    zle -R -c
    # CURSOR=$#BUFFER
    # echo $CURSOR
    # LBUFFER="ls"
    # zle -R
    # RBUFFER="\\n123"
    # PREDISPLAY="kkk"
    # POSTDISPLAY="asd"
}

zle -N test

bindkey '^R' test