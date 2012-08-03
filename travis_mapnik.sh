#!/bin/bash
# Dirty ugly hack to use mapnik system installation

cp -R /usr/share/pyshared/mapnik2 $VIRTUAL_ENV/lib/python2.7/site-packages/
# cp /usr/lib/pyshared/python2.7/mapnik2/* $VIRTUAL_ENV/lib/python2.7/site-packages/mapnik2
