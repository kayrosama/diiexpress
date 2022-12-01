#!/bin/bash
NPID=`ps -efa | grep "manage.py runserver 0:10666" | grep -v grep | wc -l`
if [[ $NPID > 0 ]]
then
    echo -e "Cantidad de procesos corriendo :--> [$NPID]"
else 
    FECINI=`date +"%Y%m%d %T"`
    echo -e "$FECINI - Proceso no existe para este sistema."
    DJANGO_DIR=$(dirname $(cd `dirname $0` && pwd))
    DJANGO_SETTINGS_MODULE=config.settings
    cd $DJANGO_DIR
    source $DJANGO_DIR/venv/bin/activate
    export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
    exec /usr/bin/python3 manage.py runserver 0:10666 &
    FECFIN=`date +"%Y%m%d %T"`
    echo -e "$FECFIN - Proceso iniciado."
fi

