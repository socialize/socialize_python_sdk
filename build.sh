#! /bin/bash


cd  `dirname $0`

OS="`uname`"
INSTALL_DIR=${INSTALL_DIR:=_install} 

build() {
    echo ----------- Building virtual environment ----------------
    VPYTHON=python2.7
    [ "$OS" == "Darwin" ] && VPYTHON=python
    virtualenv --no-site-packages --distribute $INSTALL_DIR
    echo ----------- INSTALL REQUIREMENTS ----------------
    $INSTALL_DIR/bin/pip install -E $INSTALL_DIR -r requirements.pip
}

clean() {
    echo ----------- Clean up -----------------
    rm -rf $INSTALL_DIR
    rm -rf \.coverage
    rm -rf html coverage.xml
    find . -iname "*.pyc" | xargs rm -rvf
}

unit_test(){
    
    clean
    build
    echo ----------- Running Unit Test ----------------
    
    _install/bin/nosetests tests --with-coverage
    _install/bin/coverage xml
}

usage() {
    echo "$0 [build|clean|unit_test]"
}

[ $# -lt 1 ] && usage && exit 1
OPT=$1

case $OPT in
    build)
        build ;;
    clean)
        clean ;;
    unit_test)
        unit_test ;;
    *)
        usage
        exit 2
        ;;
esac
