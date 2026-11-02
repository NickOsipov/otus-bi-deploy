#!/bin/bash

yc compute instance create \
    --name redash \
    --ssh-key ~/.ssh/yc.pub \
    --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-2004-lts,size=20,auto-delete=true \
    --network-interface subnet-name=default-ru-central1-d,nat-ip-version=ipv4 \
    --preemptible \
    --memory 4G \
    --cores 2 \
    --zone ru-central1-d \
    --hostname redash \
    --async
