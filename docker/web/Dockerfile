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
        && apt-get -y install joe mc apache2 python3-pip git \
# Install and upgrade Python modules
        && pip3 install --upgrade pip \
        && pip3 install boto3 \
        && pip3 freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip3 install -U \
# delete all the apt list files since they're big and get stale quickly
        && rm -rf /var/lib/apt/lists/* \
# enable the universe
        && sed -i 's/^#\s*\(deb.*universe\)$/\1/g' /etc/apt/sources.list \
# make systemd-detect-virt return "docker"
# See: https://github.com/systemd/systemd/blob/aa0c34279ee40bce2f9681b496922dedbadfca19/src/basic/virt.c#L434
        && mkdir -p /run/systemd \
        && echo 'docker' > /run/systemd/container \
# HTTP Server configuration
        && a2dismod mpm_event \
        && a2enmod mpm_prefork cgi \
        && (cd /etc/apache2/sites-available \
          && mv -v 000-default.conf 000-default.conf.orig \
          && sed \
               -e '/[ tab]*#ServerName/s/#ServerName www.example.com/ServerName epgp.cerna-ruka.cz/' \
               -e '/[ tab]*ServerAdmin/s/webmaster@localhost/Tomas.Kraus@oracle.com/' \
               -e '/<\/VirtualHost>/s/\(<\/VirtualHost>\)/\n        <Directory \/var\/www\/html>\n            Options \+ExecCGI\n            DirectoryIndex index\.py\n        <\/Directory>\n\1/' \
               -e '/<\/VirtualHost>/s/\(<\/VirtualHost>\)/\n        # Python scripts\n        AddHandler cgi-script .py\n\n\1/' \
               000-default.conf.orig > 000-default.conf ) \
        && cat /etc/apache2/sites-available/000-default.conf \
        && (cd /var/www && rm -rf * && git clone https://github.com/kratz74/pyEpGp.git .) \
        && mkdir -v /opt/bin \
        && chmod -v u=rwx,og=rx /opt/bin \
        && echo '#!/bin/bash' > /opt/bin/start.sh \
        && echo 'service apache2 start' >> /opt/bin/start.sh \
        && echo 'tail -f /var/log/apache2/error.log' >> /opt/bin/start.sh \
        && chmod -v u=rwx,og-rwx /opt/bin/start.sh

# overwrite this with 'CMD []' in a dependent Dockerfile
CMD ["/opt/bin/start.sh"]
