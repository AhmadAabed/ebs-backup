#!/usr/bin/python
import getopt, sys
from boto.ec2.connection import EC2Connection
from datetime import datetime
import sys

#please note that i hold no responsibility of using this script use it on your own
#please make sure your file system is consistent before using the script "i.e locking a database"
#using this script in a careless way may leave the snapshot in inconsistent state

def main():

  aws_access_key = 'SOME_KEY'
  aws_secret_key = 'SOME_SECRET'
  
  try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:k:dwm", ["help", "disk_id=","keep=","daily","weekly","monthly"])

  except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
  for o, a in opts:

    if o in ("-h", "--help"):
      usage()
      sys.exit()
 
    elif o in ("-i", "--disk_id"):
      disk_id = a

    elif o in ("-d", "--daily"):
      mode = "daily"

    elif o in ("-w", "--weekly"):
      mode = "weekly"

    elif o in ("-m", "--monthly"):
      mode ="monthly"

    elif o in ("-k", "--keep"):
      keep = int(a)

    else:
      assert False, "unhandled option"
  
  description = datetime.today().isoformat(' ') +" ("+ mode +")"
  conn = EC2Connection(aws_access_key, aws_secret_key)
  volumes = conn.get_all_volumes([disk_id])
  volume = volumes[0]
  if volume.create_snapshot(description):
    print 'Snapshot created with description: ' + description

  snapshots = volume.snapshots()
  snapshots_daily = [snap for snap in snapshots if 'daily' in snap.description ]
  snapshots_weekly = [snap for snap in snapshots if 'weekly' in snap.description ]
  snapshots_monthly = [snap for snap in snapshots if 'monthly' in snap.description ]
  
  snapshot = snapshots[0]

  def date_compare(snap1, snap2):
     if snap1.start_time < snap2.start_time:
         return -1
     elif snap1.start_time == snap2.start_time:
         return 0
     return 1

  snapshots_daily.sort(date_compare)
  snapshots_weekly.sort(date_compare)
  snapshots_monthly.sort(date_compare)

  if mode == "daily":
    delta = len(snapshots_daily) - keep
    for i in range(delta):
      print 'Deleting snapshot ' + snapshots_daily[i].description
      snapshots_daily[i].delete()

  elif mode == "weekly":
    delta = len(snapshots_weekly) - keep
    for i in range(delta):
      print 'Deleting snapshot ' + snapshots_weekly[i].description
      snapshots_weekly[i].delete()

  elif mode == "monthly":
    delta = len(snapshots_monthly) - keep
    for i in range(delta):
      print 'Deleting snapshot ' + snapshots_monthly[i].description
      snapshots_monthly[i].delete()

def usage():
    print"\nbefore using please open the script and set \naws_access_key = 'YOUR_ACCESS_KEY'\naws_secret_key = 'YOUR SECRET_KEY'\n"
    print "Usage: python ebs_snapshot.py -i [volume_id] -k [number of snapshots to be kept] --daily|--monthly|--weekly"
    print "you can use -d,-m,-w instead of --daily --monthly --weekly "
    print "\nexample usage: python ebs_snapshot.py -i vol-f4fe5b75  -k 2 --monthly"
    print "\nyou can set -k 0 to delete all snapshots of a specific backup i.e \"monthly\""


if __name__ == "__main__":
	main()
