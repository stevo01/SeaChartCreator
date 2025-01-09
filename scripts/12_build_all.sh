#!/bin/bash

source ./scripts/common.sh

set +e


# build map
MAP_DESCR_FILE="chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-test.xml"

# Loop over array and execute command
for MAP_DESCR_FILE in "${MAP_FILES[@]}"; do
{
    $RUN python3 build.py -t kap -d $DB_DIR -s -i $MAP_DESCR_FILE
    $RUN python3 build.py -t mbtiles -d $DB_DIR -s -i $MAP_DESCR_FILE
} || {
    echo "Error occurred while fetching tiles for $MAP_DESCR_FILE"
    exit 1
}
done