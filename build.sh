#! /bin/bash


cd  `dirname $0`

OS="`uname`"
INSTALL_DIR=${INSTALL_DIR:=_install} 
CACHE_DIR=${CACHE_DIR:=_pip}

build() {


    echo ----------- Building virtual environment ----------------


    PYTHON=$(which python2.7)
    #setup virtual env
    ENV_OPTS="--distribute -p $PYTHON"
    # Set to whatever python interpreter you want for your first environment:
    URL_BASE=http://pypi.python.org/packages/source/v/virtualenv
    VERSION="1.9.1"

    echo "initialization complete"
    echo "Setting up virtual env in installdir: $INSTALL_DIR"

    if [ ! -d $INSTALL_DIR ]; then
        pushd $INSTALL_DIR
        # --- Real work starts here ---
        curl -O -L $URL_BASE/virtualenv-$VERSION.tar.gz
        tar xzf virtualenv-$VERSION.tar.gz
        # Create the first "bootstrap" environment.
        echo "creating virtual environment..." 
        $PYTHON virtualenv-$VERSION/virtualenv.py $ENV_OPTS $INSTALL_DIR
        # Don't need this anymore.
        popd $INSTALL_DIR
    fi

    . $INSTALL_DIR/bin/activate

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
