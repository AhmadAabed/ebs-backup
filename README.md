##Backup script for EBS

## Description
Helps you with the backup of EBS volumes.

## Usage

Usage: python ebs_snapshot.py -i [volume_id] -k [number of snapshots to be kept] --daily|--monthly|--weekly

example usage: python ebs_snapshot.py -i vol-f4fe5b75 -k 2 --monthly

you can set -k 0 to delete all snapshots of a specific backup i.e "monthly""

you can use -d,-m,-w instead of --daily --monthly --weekly 
