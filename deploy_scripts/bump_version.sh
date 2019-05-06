#!/usr/bin/env bash

BUMP_PART="$(./deploy_scripts/get_bump_part.sh)"

function bump_or_exit(){
    if  [[ ${BUMP_PART} != "no bump" ]]; then
        cd ..
        echo "$(bump2version --dry-run --list --verbose ${BUMP_PART})"
        return 0
    else
        echo "No version bump specified in commit."
        return 1
    fi
}

bump_or_exit

exit
