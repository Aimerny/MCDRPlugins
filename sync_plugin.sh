#!/bin/bash

MCDR_MAIN_PLUGIN_HOME=~/mcdr/main/plugins
MCDR_MIRROR_PLUGIN_HOME=~/mcdr/mirror1/plugins

mcdreforged pack && mv *.mcdr $MCDR_MAIN_PLUGIN_HOME
mcdreforged pack && mv *.mcdr $MCDR_MIRROR_PLUGIN_HOME