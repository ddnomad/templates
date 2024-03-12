#!/usr/bin/env bash
set -euo pipefail

# shellcheck disable=SC2155
readonly SCRIPT_HELP_MESSAGE="$(cat <<EOF
Usage: $0 <PYPROJECT_PATH> <PACKAGE_META_PATH>

Synchronise package meta information between pyproject.toml and package's meta.py.
The former file is treated as an authoritative source.

The following values are synchronised:

* tool.poetry.name        -> $(tput sitm)<package>$(tput sgr0).meta.PACKAGE_NAME
* tool.poetry.description -> $(tput sitm)<package>$(tput sgr0).meta.DESCRIPTION
* tool.poetry.license     -> $(tput sitm)<package>$(tput sgr0).meta.LICENSE
* tool.poetry.version     -> $(tput sitm)<package>$(tput sgr0).meta.VERSION
* tool.poetry.authors     -> $(tput sitm)<package>$(tput sgr0).meta.AUTHOR
EOF
)"

# shellcheck disable=SC2209
SED=sed
if command -v gsed &> /dev/null; then
    SED=gsed
fi
readonly SED

function main {
    if test "$#" -ne 2; then
        >&2 echo "${SCRIPT_HELP_MESSAGE}"
        exit 1
    fi

    local pyproject_path
    pyproject_path="$1"
    shift

    local package_init_path
    package_init_path="$1"
    shift

    local value_name_pairs
    # shellcheck disable=SC2054
    value_name_pairs=(name,PACKAGE_NAME description,DESCRIPTION license,LICENSE version,VERSION authors,AUTHOR)

    local value_name_pair
    for value_name_pair in "${value_name_pairs[@]}"; do
        local pyproject_value_name
        pyproject_value_name="$(cut -f1 -d',' <<<"${value_name_pair}")"

        local package_value_name
        package_value_name="$(cut -f2 -d',' <<<"${value_name_pair}")"

        local pyproject_value
        pyproject_value="$(sed -n 's@'"${pyproject_value_name}"'.*=.*"\(.*\)".*@\1@p' < "${pyproject_path}")"
        pyproject_value="${pyproject_value/@/\\@}"

        "${SED}" -i 's@\('"${package_value_name}"'.*=.*'\''\).*\('\''\)@\1'"${pyproject_value}"'\2@' "${package_init_path}"
    done
}

main "$@"
