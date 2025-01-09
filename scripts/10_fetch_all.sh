#!/bin/bash

source ./scripts/common.sh

# Loop over array and execute command
for MAP_DESCR_FILE in "${MAP_FILES[@]}"; do
{
  python3 fetch.py -m "${MAPSOURCE}" -d $DB_DIR -q -s -f -i "${MAP_DESCR_FILE}" 2>&1 | tee -a "$LOG_FILE"
} || {
    echo "Error occurred while fetching tiles for $MAP_DESCR_FILE"
    exit 1
}
done
