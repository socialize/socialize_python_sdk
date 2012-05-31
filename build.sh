#! /bin/bash


cd  `dirname $0`

OS="`uname`"
INSTALL_DIR=${INSTALL_DIR:=_install} 
CACHE_DIR=${CACHE_DIR:=_pip}

build() {
    echo ----------- Building virtual environment ----------------
    VPYTHON=python2.7
    [ "$OS" == "Darwin" ] && VPYTHON=python
    virtualenv --no-site-packages --distribute $INSTALL_DIR
    echo ----------- INSTALL REQUIREMENTS ----------------
    $INSTALL_DIR/bin/pip install -M \
        -i http://ssz-pip.s3-website-us-east-1.amazonaws.com/ \
        --download-cache $CACHE_DIR -r requirements.pip --log=./_pip.log
}

clean() {
    echo ----------- Clean up -----------------
    rm -rf $INSTALL_DIR
    rm -rf \.coverage
    rm -rf tests/html coverage.xml
    find . -iname "*.pyc" | xargs rm -rvf
}
run_test(){
    echo ----------- Running Unit Test ----------------
    $INSTALL_DIR/bin/nosetests tests --with-xunit --with-coverage --cover-package=socialize -v --cover-html
    $INSTALL_DIR/bin/coverage html -d tests/html      
}

unit_test(){
    clean
    build
    run_test
}

usage() {
    echo "$0 [build|clean|unit_test|run_test]"
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
    run_test)
        run_test ;;    
    *)
        usage
        exit 2
        ;;
esac
