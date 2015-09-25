#!/bin/sh

git=$(which git)

get_git_timestamp() {
    $git show -s --pretty=format:%ct
}


dev_version_tag() {
    date -d  "@$(get_git_timestamp)" "+%Y-%m-%d-%H:%M"
}


get_current_version() {

    version=$($git describe --tags)
    echo "${version}:dev:$(dev_version_tag)"
}



# replace %%version%% 

[ -z "$FILES" ] && FILES="HISTORY.rst"

version=$(get_current_version)

for file in $FILES; do
    if [ -e "$file" ]; then
        sed -ri "s#%%version%%#$version#g" "$file"
    fi
done

