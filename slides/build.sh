#!/bin/bash

set -e

big-presentation-compose
sed -i -e 's/lang-yaml/yaml/g' index.html