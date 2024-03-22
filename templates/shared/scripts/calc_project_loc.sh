#!/usr/bin/env bash
set -euo pipefail


function main {
    if test "$#" -ne 2; then
        >&2 echo "Usage: $0 <BASE_DIR> <FILE_EXT>"
        exit 1
    fi

    local base_dir
    base_dir="$1"
    shift

    local file_ext
    file_ext="$1"
    shift

    find "${base_dir}"/ -type f | grep -E "\.${file_ext}"'$' | xargs -n1 cat | wc -l
}


main "$@"
