#!/bin/sh

mkdir -p factbook
cd factbook

for year in {2002..2014}
do
  wget "https://www.cia.gov/library/publications/download/download-$year/fields.zip"
  unzip fields.zip -d $year
  chmod ag+w -R $year

  if [ -d $year/fields ]
  then
    mv $year/fields/* $year
    rmdir $year/fields
  fi

  if [ -d $year/factbook ]
  then
    mv $year/factbook/fields/* $year
    rmdir $year/factbook/fields
    rmdir $year/factbook
  fi

  rm fields.zip

  for html in $year/*.html
  do
    text="${html%.*}.txt"
    echo "Parsing $html"
    lynx -dump -nolist $html > $text
  done
done
