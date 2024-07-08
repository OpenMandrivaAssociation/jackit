#!/bin/sh
# "1.90" is older than "v1.9" -- only care about tags starting with a "v".
git ls-remote --tags https://github.com/jackaudio/jack2 2>/dev/null|awk '{ print $2; }' |sed -e 's,refs/tags/,,;s,_,.,g;s,\^{},,' |grep '^v' |sed -e 's,^v,,' |sort -V |tail -n1
