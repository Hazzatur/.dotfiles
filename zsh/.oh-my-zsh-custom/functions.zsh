# copy text|file to clipboard
function clipcopy() {
  if [[ $# -lt 1 ]]; then
    echo "Usage: $funcstack[1] <text|file>"
    echo "text supports multiple entries separated by space"
    echo "Use -t to treat everything as text"
    return
  fi

  local allText="false"
  if [[ "$1" == "-t" ]]; then
    allText="true"
  fi

  local _clipboard=""
  echo "" | xclip -selection clipboard
  for arg in "$@"; do
    if [[ "$arg" == "-t" ]]; then
      continue
    fi
    if [[ -f "$arg" && $allText == "false" ]]; then
      _clipboard+="$(cat "$arg")"
      _clipboard+="\n"
    else
      _clipboard+="$arg\n"
    fi
  done
  clipboard=$(echo "$_clipboard" | sed '$d')
  echo -e "$clipboard" | xclip -selection clipboard
}

# cd to the directory of a symlink
function cdl() { 
  if [[ $# -lt 1 ]]; then
    echo "Usage: $funcstack[1] <symlink>"
    echo "if file, change to parent folder"
    return
  fi

  if [[ -L $1 ]]; then
    if [[ -d $1 ]]; then
      local dir=$(readlink -e $1); [[ -n "$dir" ]] && cd $dir; 
    else
      local dir=$(readlink -e $1); [[ -n "$dir" ]] && cd $(dirname $dir); 
    fi
  else
    echo "$1 is not a symlink"
  fi
}

# clear docker container logs
function clear_dc_logs() {
  if [[ $# -lt 1 ]]; then
    echo "Usage: $funcstack[1] <container>"
    return
  fi

  docker inspect --format='{{.LogPath}}' $1 | xargs -L 1 sudo truncate -s 0
}

# save output of a command to a log file
# alias -g LOG='| to_log'
function to_log() { tee -a /tmp/log_$(date +%F_%T).log; } 

function remove_empty_lines() {
  if [[ $# -lt 1 ]]; then
    echo "Usage: $funcstack[1] <file> -s[same file]"
    return
  fi

  if [[ "$2" == "-s" ]]; then
    sed '/^$/d' "$1" > "$1"_tmp
    mv "$1"_tmp "$1"
  else
    sed '/^$/d' "$1" > "$1"_no_empty_lines
  fi
}

function remove_duplicated_lines() {
  if [[ $# -lt 1 ]]; then
    echo "Usage: $funcstack[1] <file> -s[same file]"
    return
  fi

  if [[ "$2" == "-s" ]]; then
    awk '!a[$0]++' "$1" > "$1"_tmp
    mv "$1"_tmp "$1"
  else
    awk '!a[$0]++' "$1" > "$1"_no_duplicate_lines
  fi
}

function remove_lines_containing() {
  if [[ $# -lt 2 ]]; then
    echo "Usage: $funcstack[1] <file> <regex> -s[same file]"
    return
  fi

  if [[ "$3" == "-s" ]]; then
    < "$1" grep -v "$2" > "$1"_tmp
    mv "$1"_tmp "$1"
  else
    < "$1" grep -v "$2" > "$1"_remove_lines_containing
  fi
}
