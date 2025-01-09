#!/bin/bash

RUN="docker compose exec SeaChartCreator /SeaChartCreator/scripts/run.sh"

MAP_DESCR_FILE="./sample/atlas/osmcb/sea/osmcb-catalog-test.xml"
MAPSOURCE="./sample/mapsource/mp-OpenSeaMap-Bravo.yaml"
DB_DIR="./work/cache/"

LOG_FILE="logs/fetch.log"

mkdir -p ./logs

# array with all map files used for offline map generation
declare -a MAP_FILES=(
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-Adria.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-ArabianSea.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-Baltic.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-Caribbean.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-Channel.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-EastChineseSea.xml"
  "chart-projectfiles/atlas/mobac/inland-water-ways/mobac-profile-Europa1.xml"
  "chart-projectfiles/atlas/mobac/inland-water-ways/mobac-profile-Bodensee.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-GreatLakes.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-GulfOfBengal.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-GulfOfBiscay.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-MagellanStrait.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-MediEast.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-MediWest.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-Niederlande-Binnen.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-NorthernAtlantic.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-NorthSea.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-NorthWestPassage.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-Saimaa.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-SouthChineseSea.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-SouthPacificIslands.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-test.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-USWestCoast.xml"
  "chart-projectfiles/atlas/osmcb/sea/osmcb-catalog-Germany-NorthEast.xml"
)
