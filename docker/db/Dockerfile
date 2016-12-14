FROM scratch
# https://partner-images.canonical.com/core/yakkety/current/ubuntu-yakkety-core-cloudimg-amd64-root.tar.gz
ADD ubuntu-yakkety-core-cloudimg-amd64-root.tar.gz /

# a few minor docker-specific tweaks
# see https://github.com/docker/docker/blob/9a9fc01af8fb5d98b8eec0740716226fadb3735c/contrib/mkimage/debootstrap
RUN set -xe \
	\
# https://github.com/docker/docker/blob/9a9fc01af8fb5d98b8eec0740716226fadb3735c/contrib/mkimage/debootstrap#L40-L48
	&& echo '#!/bin/sh' > /usr/sbin/policy-rc.d \
	&& echo 'exit 101' >> /usr/sbin/policy-rc.d \
	&& chmod +x /usr/sbin/policy-rc.d \
	\
# https://github.com/docker/docker/blob/9a9fc01af8fb5d98b8eec0740716226fadb3735c/contrib/mkimage/debootstrap#L54-L56
	&& dpkg-divert --local --rename --add /sbin/initctl \
	&& cp -a /usr/sbin/policy-rc.d /sbin/initctl \
	&& sed -i 's/^exit.*/exit 0/' /sbin/initctl \
	\
# https://github.com/docker/docker/blob/9a9fc01af8fb5d98b8eec0740716226fadb3735c/contrib/mkimage/debootstrap#L71-L78
	&& echo 'force-unsafe-io' > /etc/dpkg/dpkg.cfg.d/docker-apt-speedup \
	\
# https://github.com/docker/docker/blob/9a9fc01af8fb5d98b8eec0740716226fadb3735c/contrib/mkimage/debootstrap#L85-L105
	&& echo 'DPkg::Post-Invoke { "rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true"; };' > /etc/apt/apt.conf.d/docker-clean \
	&& echo 'APT::Update::Post-Invoke { "rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true"; };' >> /etc/apt/apt.conf.d/docker-clean \
	&& echo 'Dir::Cache::pkgcache ""; Dir::Cache::srcpkgcache "";' >> /etc/apt/apt.conf.d/docker-clean \
	\
# https://github.com/docker/docker/blob/9a9fc01af8fb5d98b8eec0740716226fadb3735c/contrib/mkimage/debootstrap#L109-L115
	&& echo 'Acquire::Languages "none";' > /etc/apt/apt.conf.d/docker-no-languages \
	\
# https://github.com/docker/docker/blob/9a9fc01af8fb5d98b8eec0740716226fadb3735c/contrib/mkimage/debootstrap#L118-L130
	&& echo 'Acquire::GzipIndexes "true"; Acquire::CompressionTypes::Order:: "gz";' > /etc/apt/apt.conf.d/docker-gzip-indexes \
	\
# https://github.com/docker/docker/blob/9a9fc01af8fb5d98b8eec0740716226fadb3735c/contrib/mkimage/debootstrap#L134-L151
	&& echo 'Apt::AutoRemove::SuggestsImportant "false";' > /etc/apt/apt.conf.d/docker-autoremove-suggests \
# Update system
        && apt-get update \
# Upgrade system
        && apt-get upgrade \
# Install software
        && apt-get -y install joe mc wget default-jre \
# delete all the apt list files since they're big and get stale quickly
        && rm -rf /var/lib/apt/lists/* \
# enable the universe
        && sed -i 's/^#\s*\(deb.*universe\)$/\1/g' /etc/apt/sources.list \
# make systemd-detect-virt return "docker"
# See: https://github.com/systemd/systemd/blob/aa0c34279ee40bce2f9681b496922dedbadfca19/src/basic/virt.c#L434
        && mkdir -p /run/systemd \
        && echo 'docker' > /run/systemd/container \
# DynamoDB Setup using pkg from http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz
        && groupadd --gid 580 dynamo \
        && useradd --uid 580 --gid 580 --comment 'Dynamo DB' --home /opt/DynamoDB --system dynamo \
        && (cd /opt && mkdir -v pkg && chmod -v u=rwx,o=rx pkg) \
        && (cd /opt/pkg && wget http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz) \
        && (cd /opt && mkdir -v DynamoDB && chown -v dynamo:dynamo DynamoDB && chmod -v u=rwx,o=rx DynamoDB) \
        && (cd /opt/DynamoDB && su -m -c 'tar xvfz /opt/pkg/dynamodb_local_latest.tar.gz' dynamo) \
        && (cd /opt/DynamoDB && su -m -c 'mkdir data' dynamo) \
        && (cd /opt && mkdir -v bin && chmod -v u=rwx,o=rx bin) \
        && echo '#!/bin/sh'                          > /opt/bin/start-db.sh \
        && echo "PREFIX='/opt/DynamoDB'"            >> /opt/bin/start-db.sh \
        && echo 'DATA="${PREFIX}/data"'             >> /opt/bin/start-db.sh \
        && echo 'LIB="${PREFIX}/DynamoDBLocal_lib"' >> /opt/bin/start-db.sh \
        && echo 'JAR="${PREFIX}/DynamoDBLocal.jar"' >> /opt/bin/start-db.sh \
        && echo '' >> /opt/bin/start-db.sh \
        && echo '(cd ${DATA} && java -Djava.library.path=${LIB} -jar ${JAR} -sharedDb -dbPath ${DATA})' >> /opt/bin/start-db.sh \
        && chmod -v u=rwx,o=rx /opt/bin/start-db.sh \
        && echo '#!/bin/sh'                              > /opt/bin/start.sh \
        && echo "su -m -c '/opt/bin/start-db.sh' dynamo" >> /opt/bin/start.sh \
        && chmod -v u=rwx,o-rwx /opt/bin/start.sh

# overwrite this with 'CMD []' in a dependent Dockerfile
CMD ["/opt/bin/start.sh"]
