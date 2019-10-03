#!/bin/bash

echo "Connecting WiFi..."
sleep 5
sudo connect_wifi
sleep 5

echo "Starting xscreensaver..."
xscreensaver &
sleep 1
echo "Starting purge-kiosk..."
python purge-kiosk.py firefox &

while true; do
	echo "Restarting firefox..."
	sleep 2
	rm -rf .mozilla
	firefox &
	kiosk_pid=$!
	sleep 1
	xdotool search --sync --onlyvisible --class "Firefox" windowactivate key F11
	echo "Firefox is started."
	wait $kiosk_pid
done

