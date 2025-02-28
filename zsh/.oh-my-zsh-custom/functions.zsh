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

function br {
    local cmd cmd_file code
    cmd_file=$(mktemp)
    if broot --outcmd "$cmd_file" "$@"; then
        cmd=$(<"$cmd_file")
        command rm -f "$cmd_file"
        eval "$cmd"
    else
        code=$?
        command rm -f "$cmd_file"
        return "$code"
    fi
}

function git_search_commit() {
  if [[ $# -lt 2 ]]; then
    echo "Usage: git_search_commit <commit-hash> <text-to-search> [--case-sensitive]"
    return 1
  fi

  local commit="$1"
  local search_text="$2"
  local case_sensitive=false

  # Check if optional case-sensitive flag is provided
  if [[ "$3" == "--case-sensitive" ]]; then
    case_sensitive=true
  fi

  # Retrieve the files changed in the commit and containing the search text
  local files
  if $case_sensitive; then
    files=$(git grep "$search_text" -- $(git show --pretty=format: --name-only "$commit"))
  else
    files=$(git grep -i "$search_text" -- $(git show --pretty=format: --name-only "$commit"))
  fi

  if [[ -z "$files" ]]; then
    echo "No matches found for '$search_text' in commit $commit."
    return 0
  fi

  # Loop through the files and show the context
  while IFS= read -r line; do
    local file=$(echo "$line" | awk -F: '{print $1}')
    echo -e "\033[1;33m\nIn file: $file\033[0m"  # Highlight "In file" in yellow
    if $case_sensitive; then
      git show "$commit:$file" | grep --color=always -C 2 "$search_text"
    else
      git show "$commit:$file" | grep --color=always -i -C 2 "$search_text"
    fi
  done <<< "$files"
}

function git_search_commits() {
  if [[ $# -lt 1 ]]; then
    echo "Usage: git_search_commits <text-to-search> [--case-sensitive]"
    return 1
  fi

  local search_text="$1"
  local case_sensitive=false

  # Check for optional case-sensitive flag
  if [[ "$2" == "--case-sensitive" ]]; then
    case_sensitive=true
  fi

  if $case_sensitive; then
    # Use git log with -G to search the commit diffs (case sensitive)
    git log --all --pretty=format:"%h - %s" -G"$search_text"
  else
    # For case-insensitive search, loop over all commits and grep each diff.
    echo "Searching commits for '$search_text' (case-insensitive)..."
    for commit in $(git rev-list --all); do
      if git show "$commit" | grep -qi "$search_text"; then
        git log -1 --pretty=format:"%h - %s" "$commit"
      fi
    done
  fi
}
