# !bin/bash
BIGBYTES_CLI="python3 -m bigbytes.cli.main"
PIP="python3 -m pip"

POSITIONAL=()
while [ $# -gt 0 ]; do
    key="$1"
    case $key in
        --name)
        REPO_NAME="$2"
        shift
        ;;
        *)    # unknown option
        POSITIONAL+=("$1")
        ;;
    esac
    shift
done

: "${REPO_NAME:="default_repo"}"

ssh -i ${POSITIONAL[0]} -f -L 6789:localhost:6789 ${POSITIONAL[1]}@${POSITIONAL[2]} sleep 120
ssh -t -i ${POSITIONAL[0]} ${POSITIONAL[1]}@${POSITIONAL[2]} "if ! $PIP list | grep bigbytes; then $PIP install bigbytes; fi;" \
"$BIGBYTES_CLI init $REPO_NAME; $BIGBYTES_CLI start $REPO_NAME;"
