#!/bin/bash
# Dirty ugly hack to use mapnik system installation

if [ -d "/usr/share/pyshared/mapnik" ]; then
    echo "Copying /usr/share/pyshared/mapnik into virtualenv"
    cp -R /usr/share/pyshared/mapnik $VIRTUAL_ENV/lib/python2.7/site-packages/
fi

if [ -d "/usr/share/pyshared/mapnik2" ]; then
    echo "Copying /usr/share/pyshared/mapnik2 into virtualenv"
    cp -R /usr/share/pyshared/mapnik2 $VIRTUAL_ENV/lib/python2.7/site-packages/
fi

if [ -d "/usr/lib/pyshared/python2.7/mapnik" ]; then
    echo "/usr/lib/pyshared/python2.7/mapnik/* into virtualenv"
    if [ -d "$VIRTUAL_ENV/lib/python2.7/site-packages/mapnik" ]; then
        mkdir -p $VIRTUAL_ENV/lib/python2.7/site-packages/mapnik
    fi
    cp /usr/lib/pyshared/python2.7/mapnik/* $VIRTUAL_ENV/lib/python2.7/site-packages/mapnik
fi

if [ -d "/usr/lib/pyshared/python2.7/mapnik2" ]; then
    echo "/usr/lib/pyshared/python2.7/mapnik2/* into virtualenv"
    if [ -d "$VIRTUAL_ENV/lib/python2.7/site-packages/mapnik2" ]; then
        mkdir -p $VIRTUAL_ENV/lib/python2.7/site-packages/mapnik2
    fi
    cp /usr/lib/pyshared/python2.7/mapnik2/* $VIRTUAL_ENV/lib/python2.7/site-packages/mapnik2
fi
