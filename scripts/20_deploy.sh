#!/bin/bash

set -x
ls ./work/kap/
ls ./work/mbtiles/

rsync -e "ssh -i ~/.ssh/id_osm" -av work/kap/*.7z osm-trans@golf.franken.de:charts/kap/
rsync -e "ssh -i ~/.ssh/id_osm" -av work/history/kap/*.7z osm-trans@golf.franken.de:charts/history/kap/
rsync -e "ssh -i ~/.ssh/id_osm" -av work/history/kap/*.geojson osm-trans@golf.franken.de:charts/history/kap/

rsync -e "ssh -i ~/.ssh/id_osm" -av work/mbtiles/*.mbtiles osm-trans@golf.franken.de:charts/mbtiles/
rsync -e "ssh -i ~/.ssh/id_osm" -av work/history/mbtiles/*.mbtiles osm-trans@golf.franken.de:charts/history/mbtiles/
rsync -e "ssh -i ~/.ssh/id_osm" -av work/history/mbtiles/*.geojson osm-trans@golf.franken.de:charts/history/mbtiles/

# ssh -i ~/.ssh/id_osm osm-trans@golf.franken.de