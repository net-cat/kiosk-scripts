import subprocess
import sys

xscreensaver = subprocess.Popen(["/usr/bin/xscreensaver-command", "-watch"], stdin=None, stderr=None, stdout=subprocess.PIPE)

if len(sys.argv) == 1:
    print "This script takes the same arguments as pkill."
    sys.exit(1)

try:
    while True:
        action = xscreensaver.stdout.readline().strip().split()[0]
        if action == "BLANK":
            try:
                subprocess.check_call(["/usr/bin/pkill"] + sys.argv[1:], stdin=None)
            except subprocess.CalledProcessError as ex:
                print "Failed to pkill {}. ({})".format(repr(sys.argv[1:]), ex.returncode)

except KeyboardInterrupt:
    pass

xscreensaver.terminate()

