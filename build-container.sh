#!/usr/bin/env bash
set -euo pipefail

BASEDIR=$(dirname $(readlink -f $0))
cd "$BASEDIR"

msg () {
    printf "%-10s %s\n" "$1" "$2"
}

msg "BUILD" "checksql"
python -m build -w .

# Create container
ctr=$(buildah from "opensuse/tumbleweed")
msg "CONTAINER" "$ctr"

msg "USER" "app"
buildah run "$ctr" -- useradd -d /checksql -s /bin/sh -u 2342 -U -c 'checksql app' checksql

msg "ZYPPER" "python"
buildah run "$ctr" -- zypper install -y python312 python312-pip

msg "COPY" "checksql"
buildah copy "$ctr" dist/checksql*.whl /tmp/
buildah run "$ctr" -- ls /tmp

msg "PIP" "checksql"
buildah run "$ctr" -- python3.12 -m pip install --break-system-packages --find-link=/tmp/ checksql

## Run our server and expose the port
buildah config --created-by "olafm" "$ctr"
buildah config --author "Olaf Mersmann <olafm@p-value.net>" --label "name=checksql" "$ctr"
buildah config --cmd "python3.12 -m checksql --host=0.0.0.0 --port=8080" "$ctr"
buildah config --port 8080 "$ctr"
buildah config --user checksql "$ctr"

## Commit this container to an image name
buildah commit "$ctr" "checksql:latest"
buildah rm "$ctr"
