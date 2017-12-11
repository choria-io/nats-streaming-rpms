#!/bin/bash

set -e
set -x

if [ -z $NAME ]
then
  NAME="nats-streaming-server"
fi

if [ -z $BINDIR ]
then
  BINDIR="/usr/sbin"
fi

if [ -z $ETCDIR ]
then
  ETCDIR="/etc/nats-streaming-server"
fi

if [ -z $VERSION ]
then
  echo "VERSION has not been set, cannot build"
  exit 1
fi

if [ -z $RELEASE ]
then
  RELEASE="1"
fi

if [ -z $DIST ]
then
  echo "DIST has not been set, cannot build"
  exit 1
fi

if [ -z $MANAGE_CONF ]
then
  MANAGE_CONF=1
fi

if [ ! -d /build ]
then
  echo "/build is not mounted, cannot build"
  exit 1
fi

if [ ! -d "/build/dist/${DIST}" ]
then
  echo "/build/dist/${DIST} is not mounted, cannot build"
  exit 1
fi

WORKDIR="${NAME}-${VERSION}"
ZIPFILE="nats-streaming-server-v${VERSION}-linux-amd64.zip"
TARBALL="/tmp/${NAME}-${VERSION}-linux-amd64.tgz"

if [ ! -f ${ZIPFILE} ]
then
  curl -L -o ${ZIPFILE} https://github.com/nats-io/nats-streaming-server/releases/download/v${VERSION}/nats-streaming-server-v${VERSION}-linux-amd64.zip
fi

mkdir -p ${WORKDIR}/dist

find /build/dist -maxdepth 1 -type f | xargs -I {} cp -v {} ${WORKDIR}/dist
cp -v /build/dist/${DIST}/* ${WORKDIR}/dist

for i in $(find ${WORKDIR}/dist -type f); do
  sed -i "s!{{pkgname}}!${NAME}!g" ${i}
  sed -i "s!{{bindir}}!${BINDIR}!g" ${i}
  sed -i "s!{{etcdir}}!${ETCDIR}!g" ${i}
  sed -i "s!{{version}}!${VERSION}!g" ${i}
  sed -i "s!{{iteration}}!${RELEASE}!g" ${i}
  sed -i "s!{{dist}}!${DIST}!g" ${i}
  sed -i "s!{{manage_conf}}!${MANAGE_CONF}!g" ${i}
done

unzip ${ZIPFILE}
cp nats-streaming-server-v${VERSION}-linux-amd64/nats-streaming-server ${WORKDIR}

tar -cvzf ${TARBALL} ${WORKDIR}

rpmbuild -ta ${TARBALL}

cp -v /root/rpmbuild/RPMS/x86_64/* /build
cp -v /root/rpmbuild/SRPMS/* /build
