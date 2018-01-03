#!/bin/bash

if [[ -f /witness_node_data_dir/.default_dir ]]; then
    echo "WARN: Volumes are not configured." 1>&2
fi

if [[ ! -f /witness_node_data_dir/config.ini ]]; then
    echo "WARN: Missing steemd config."
fi

if [[ ! -d /witness_node_data_dir/blockchain ]]; then
    echo "Downloading the blockchain..."
    mkdir -p /witness_node_data_dir/blockchain
    touch /witness_node_data_dir/blockchain/block_log
    # wget -O "/witness_node_data_dir/blockchain/block_log"  https://gtg.steem.house/get/blockchain/block_log
fi

${STEEMD_EXEC} ${STEEMD_ARGS} $*

if [[ $? -ne 0 ]]; then
    echo "FAIL: Exited with errors" 1>&2
    exit 1
else
    echo "INFO: Exited normally"
fi