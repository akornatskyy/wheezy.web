#!/bin/sh

SERVER='http://127.0.0.1:8080/'
N=1000
C=10

if [ ! -z $1 ]; then SERVER=$1; fi
if [ ! -z $2 ]; then N=$2; fi
if [ ! -z $3 ]; then C=$3; fi

echo Server: $SERVER
echo Number of requests: $N
echo Concurrency level: $C

AB="nice ab -n $N -c $C -k -q -H Accept-Encoding:gzip"
EXTRA=

bench() {
    LINK=$1
    RES=`$AB$EXTRA $SERVER/$LINK`
    RPS=`echo $RES | sed -r 's/.*Requests per second: ([0-9\.]+).*/\1/'`
    WRITE=`echo $RES | grep -E 'Write errors: [1-9]' | \
        sed -r 's/.*(Write errors: [0-9\.]+).*/ \1/'`
    ERROR=`echo $RES | grep -E 'Non-2xx responses' | \
        sed -r 's/.*Non-2xx responses: ([0-9\.]+).*/ Non-2xx: \1/'`
    echo $LINK $RPS$FAILED$WRITE$ERROR
}


CYCLE=1
while :
do
    echo "\nEntering cycle $CYCLE; ^C to stop."
    CYCLE=$(($CYCLE+1))

    COOKIE=`wget --max-redirect=0 --save-cookies /dev/stdout \
        --keep-session-cookies -qO /dev/null $SERVER'en/signin' | \
        grep -o '_x.*$' | sed -r 's/_x[[:blank:]]*(.*)$/\1/'`
    echo xsrf cookie: $COOKIE
    COOKIE=`wget --max-redirect=0 --save-cookies /dev/stdout \
        --keep-session-cookies -qO /dev/null \
        --post-data="username=demo&password=P%40ssw0rd&_x=$COOKIE" \
        --header="Cookie: _x=$COOKIE" $SERVER'en/signin' | \
        grep -o '_a.*$' | sed -r 's/_a[[:blank:]]*(.*)$/\1/'`
    echo auth cookie: $COOKIE

    echo public:
    EXTRA=""
    bench /
    bench /en/home
    bench /ru/home
    bench /en/about
    bench /en/signin
    bench /en/signup
    bench /en/error/404
    bench /missing

    echo secure:
    EXTRA=" -C _a=$COOKIE"
    bench /
    bench /en/home

    sleep 1
done
