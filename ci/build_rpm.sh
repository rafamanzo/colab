#!/bin/bash

BRANCH=${TRAVIS_BRANCH:-${CIRCLE_BRANCH}}

case $BRANCH in
    "master")
        repo="colab-unstable" ;;
    "stable")
        repo="colab-stable" ;;
    "test")
        repo="colab-testing" ;;
    *)
        exit 1;;
esac


repo_url="https://packagecloud.io/seocam/$repo/el/7/x86_64"

version=`python setup.py --version`
python setup.py sdist

sudo apt-get install rinse > /dev/null

sudo rinse --arch="amd64" --distribution="centos-7" --directory="/tmp/centos-7" --config="ci/rinse.conf" --pkgs-dir="ci/"

sudo mkdir -p /tmp/centos-7/root/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
sudo cp dist/colab-*.tar.gz /tmp/centos-7/root/rpmbuild/SOURCES/
sudo cp colab.spec /tmp/centos-7/root/rpmbuild/SPECS/
sudo cp ci/colab.repo /tmp/centos-7/etc/yum.repos.d/
sudo cp ci/softwarepublico.key /tmp/centos-7/etc/yum.repos.d/

# Commands on chroot

sudo chroot /tmp/centos-7/ yum install rpm-build -y --quiet
sudo chroot /tmp/centos-7/ yum install python-virtualenv colab-deps -y --quiet

sudo chroot /tmp/centos-7/ repoquery --repofrompath="$repo,$repo_url" --repoid=$repo colab --info > /tmp/colab-latest-info

latest_version=`grep -i version /tmp/colab-latest-info | awk '{ print $3 }'`
latest_release=`grep -i release /tmp/colab-latest-info | awk '{ print $3 }'`

if [ "$version" == "$latest_version" ]; then
    # Using awk because it can deal with floating points
    release=`echo $latest_release | awk '{ $1++; print $1 }'`
else
    release=1
fi

echo "Building package: $version-$release"

sudo HOME=/root chroot /tmp/centos-7/ rpmbuild --define "version $version" --define "release $release" -ba /root/rpmbuild/SPECS/colab.spec --quiet
sudo cp /tmp/centos-7/root/rpmbuild/RPMS/noarch/colab-$version-$release.noarch.rpm .


## Send to packagecloud

gem install package_cloud
package_cloud push seocam/$repo/el/7 colab-$version-$release.noarch.rpm && \
package_cloud yank seocam/$repo/el/7 colab-$latest_version-$latest_release.noarch.rpm
