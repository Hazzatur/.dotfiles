for directory in */ ; do
    stow --target=$HOME $directory --restow
done
