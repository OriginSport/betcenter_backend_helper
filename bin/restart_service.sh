#!/bin/bash

set -e

##
# DEFINE
##

PROJECT_PATH=$(cd $(dirname $(realpath "$0")); cd ..; pwd -P)
APP=betcenter_backend_helper
VENV_NAME=venv_${APP}
APPLICATION_NAME=exp_application
GUNICORN_CONFIG_PATH=${PROJECT_PATH}/gunicorn_config/gunicorn_cfg.py
PIDFILE=/tmp/gunicorn_${APP}.pid
PYTHON_EXEC=python3
export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

##
# STATUS
##
status(){
    check_venv
    check_process
}

check_venv(){
    if [[ -r ${PROJECT_PATH}/${VENV_NAME} ]]; then
        echo "venv exists"
        ${PROJECT_PATH}/${VENV_NAME}/bin/python --version
    else
        echo "venv not exists"
    fi
}

check_process(){
    if [[ -r "${PIDFILE}" ]]; then
        ps f --pid "$(cat ${PIDFILE})" --ppid "$(cat ${PIDFILE})"
    else
        echo "${APP} not running"
    fi
}

##
# START
##
start(){
    init_venv
    start_gunicorn
}


init_venv(){
    mkdir -p ~/logs
    cd "${PROJECT_PATH}"
    ${PYTHON_EXEC} -m venv ${VENV_NAME}
    source ${VENV_NAME}/bin/activate
    echo "pip install pre requires"
    pip install -U wheel
    echo "pip installing requirements...."
    pip install -U -r requirements.txt
    echo "pip complete"
}

start_gunicorn(){
    echo 'start service ...'
    gunicorn -c  "${GUNICORN_CONFIG_PATH}" \
        "applications.${APPLICATION_NAME}:app"
    sleep 2
    if [[ $? = 0 ]]; then
        echo "start success"
    else
        echo "start failed"
    fi
}

##
# STOP
##
stop(){
    stop_gunicorn_force
}


stop_gunicorn_force(){
    kill -INT "$(cat ${PIDFILE})"
    sleep 2
    if [ $? = 0 ]; then
        echo "kill success"
    fi
}

stop_gunicorn_graceful(){
    kill -TERM "$(cat ${PIDFILE})"
}

##
# RELOAD
##
reload(){
    reload_gunicorn
}

reload_gunicorn(){
    kill -HUP "$(cat ${PIDFILE})"
}

##
# MAIN
##

case "${1:-''}" in
    'start')
        start
        ;;

    'stop')
        stop
        ;;

    'restart'|'forece-reload')
        restart
        ;;

    'reload')
        reload
        ;;

    'status')
        status
        ;;

    *)
        eval "$1"
        echo "usage: $0 start|stop|restart|reload|status"
        ;;
esac
