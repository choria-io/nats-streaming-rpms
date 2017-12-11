# Using RPMS

These RPMs are hosted in the Choria RPM Repository, add it to your EL6 or 7 system like this:

```ini
[choria]
name=Choria Orchestrator - $architecture
baseurl=https://dl.bintray.com/choria/el-yum/el$releasever/$basearch
gpgcheck=0
repo_gpgcheck=0
enabled=1
protect=1
```

And then you can install `nats-streaming-server` using `yum`.

# Building RPMS

This downloads the official NATS Streaming release and makes a minimal RPM of it.

You need to build the Docker image that will make the RPMs.

```
docker build . --tag rpmbuilder
```

You can now build your package, this shows how to customise paths, names etc.  Dist can be either el6 or el7:

Below showing a fully custom build, most of these settings can be left alone to get it into the normal LSB locations:

```
docker run -v `pwd`:/build \
  -e NAME=myco-nats-streaming \
  -e VERSION=0.6.0 \                             # has to match the official release
  -e RELEASE=2 \
  -e DIST=el7 \                                  # uses config/spec etc in dist/el7
  -e BINDIR=/opt/myco/nats-streaming/bin \
  -e ETCDIR=/opt/myco/nats-streaming/etc \
  -e MANAGE_CONF=1 \                             # set to zero to not add config files to the package, 1 by default
  --rm rpmbuilder
```

At the end you'll have:

```
-rw-r--r-- 1 root root 2626976 Dec 11 13:28 myco-nats-streaming-0.6.0-2.el7.x86_64.rpm
-rw-r--r-- 1 root root 3095348 Dec 11 13:28 myco-nats-streaming-0.6.0-2.el7.src.rpm
```

The binaries, logs, services, etc will all reflect your chosen name and locations

```
rpm -qlp myco-nats-streaming-0.6.0-2.el7.x86_64.rpm
/etc/logrotate.d/myco-nats-streaming
/opt/myco/nats-streaming/bin/myco-nats-streaming
/opt/myco/nats-streaming/etc/myco-nats-streaming.conf
/usr/lib/systemd/system/myco-nats-streaming.service
```


