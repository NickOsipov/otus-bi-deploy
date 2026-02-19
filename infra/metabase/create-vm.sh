#!/bin/bash

yc compute instance create \
    --name metabase \
    --ssh-key ~/.ssh/yc.pub \
    --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-2004-lts,size=100,auto-delete=true \
    --network-interface subnet-name=default-ru-central1-a,nat-ip-version=ipv4 \
    --preemptible \
    --memory 16G \
    --cores 4 \
    --zone ru-central1-a \
    --hostname metabase