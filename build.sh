#! /bin/bash





cd  `dirname $0`

OS="`uname`"
INSTALL_DIR=${INSTALL_DIR:=_install} 
CACHE_DIR=${CACHE_DIR:=_pip_cache}


build() {
    VPYTHON=python2.7
    [ "$OS" == "Darwin" ] && VPYTHON=python
    virtualenv --no-site-packages --distribute $INSTALL_DIR
    $INSTALL_DIR/bin/pip install -E $INSTALL_DIR -r requirements.pip
}

clean() {
    rm -rf $INSTALL_DIR
    rm -rf \.coverage
    find . -iname "*.pyc" | xargs rm -rvf
}


unit_test() {
    echo ========== Building API ==========
    clean
    build
    echo ========== Removing old files ==========
    pushd ssz/ssz
    rm -rvf tests/ \.coverage
    popd
    echo ========== Setting up path ==========
    OLDPATH=$PATH
    export PATH=$PATH:_install/bin
    pushd _install/bin
    echo ========== Activating virtualenv ==========
    source activate
    COVERAGE=`which coverage`
    ./python $COVERAGE erase
    echo ========== Running tests ==========
    ./python $COVERAGE -x ./manage.py test --verbosity 0 xml-
    ./python $COVERAGE html -d tests/html;
    echo ========== Updating documentation ==========
    pushd ../../ssz/ssz
    ../../_manage.py update_documentation
    popd
    echo ========== Deactivating virtualenv ==========
    deactivate
    popd
    export PATH=$OLDPATH
    echo ========== Pushing to dev.api ==========
    pushd deploy/fabric
    fab deploy_dev
    popd
    echo ========== Done ==========
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

