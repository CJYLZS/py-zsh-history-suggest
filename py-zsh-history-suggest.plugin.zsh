

function py_zsh_history_suggest(){
    BUFFER=$(LINES=${LINES} COLUMNS=${COLUMNS} /usr/bin/suggest)
    CURSOR=$#BUFFER
    zle -R -c
}

zle -N py_zsh_history_suggest

bindkey '^R' py_zsh_history_suggest