#!/bin/bash

ansible-galaxy collection install --force \
--token 94768af4b6e7ef80e18ddde0592c412bd241a646 \
--ignore-certs -s "https://10.1.4.246/api/galaxy/content/community/" \
"community.docker:1.1.0"
