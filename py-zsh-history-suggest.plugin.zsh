pushd
cd $(dirname $0)
if [ ! -f /usr/bin/suggest ]; then
    sudo ln -s $(pwd)/suggest /usr/bin/suggest
fi
popd

function py_zsh_history_suggest(){
    BUFFER=$(LINES=${LINES} COLUMNS=${COLUMNS} /usr/bin/suggest)
    CURSOR=$#BUFFER
    zle -R -c
}

zle -N py_zsh_history_suggest

bindkey '^R' py_zsh_history_suggest