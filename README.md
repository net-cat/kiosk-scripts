# kiosk-scripts

## What is this?

Once a year, I run an event that uses a registration kiosk. Since I am tired of
using a series of sketchy, poorly-translated Firefox addons that change every
year to accomplish this, I've decided to create a solution that uses as much
open source software as possible, all tied together with a simple script.

## How does the installer work?

1. Create a "staff" account. This will be a full account that you cause use
   sudo with. (This is the currently logged account by default.)
2. Create a "kiosk" account. This will be limited account that can only log in
   it should have no administrative privileges. (The script will automatically
   use the account with the highest UID with "kiosk" in the name, but this can
   be overridden.
3. The following packages will be installed:
   * fluxbox
   * xscreensaver
   * python-toml
   * xdotool
4. xscreensaver's blanking will be set to 2 minutes and locking will be
   disabled. This can be changed with 
4. policies.json will be installed in /usr/lib/firefox/distribution
   * *NOTE:* The default policies are very restrictive and apply system-wide.
     You should install an alternative browser for the staff account to use
	 such as Chromium.
5. Stripped down fluxbox environment will be placed in the kiosk user's home
   directory.
6. Kiosk user's default session will be set to fluxbox.
7. Kiosk user's password will be scrambled.
8. Kiosk user will be set to auto-login.
9. A "connect_wifi" script will be installed in /usr/local/bin. It's
   configuration file will be placed in /etc/kiosk.conf. A sudoers file will
   be added to /etc/sudoers.d to allow the kiosk user to execute that script.
10. run_kiosk will be installed in /usr/local/bin. This script does not need
    admin rights to run and will be automatically invoked when the kiosk user
	logs in.

## How does the kiosk mode work?

1. The kiosk user will automatically log in on boot.
2. run_kiosk will launch xscreensaver.
3. run_kiosk will launch connect_wifi.
4. Once the initialization has run, the following steps will run in a loop:
   1. Firefox profile is erased.
   2. Firefox is launched with the homepage in profiles.json
   3. xdotool sends an F11 keystroke to Firefox. (Fullscreen.)
   4. Wait until firefox closes.
5. If xscreensaver activates, firefox will be killed (and the loop above will
   run again.)
   
## How do I configure this?

| What             | Where (before install) | Where (after install)                        |
| ---------------- | ---------------------- | -------------------------------------------- |
| Wireless network | kiosk.toml             | /etc/kiosk.toml                              |
| Default sites    | policies.json          | /usr/lib/firefox/distribution/policies.json  |
| Site whitelist   | policies.json*         | /usr/lib/firefox/distribution/policies.json* |
| Screen timeout   | ???                    | Run xscreensaver-demo, or ~/.xscreensaver    |
| Change user      | Run installer          | Re-run installer                             |

Site whitelisting requires Firefox 62 or better.

## Where is the installer script?

I haven't written it yet.

## TODO

* Easier way to store firefox profile.
* Uninstaller.
* List of all the things the script changes.
* Maybe do something to purge kiosk account's home directory at login?

## Where files go

* 50-autologin.conf : /etc/lightdm/lightdm.conf.d
* 50-connect-wifi : /etc/sudoers.d
* connect_wifi : /usr/local/bin

## Notes for setting up Ubuntu 18.04

NOTE: Don't set password for kiosk user to keep it off login screen.

> ```sudo useradd <kiosk>
> sudo cp -r /etc/skel /home/<kiosk>
> sudo chown -R <kiosk>:<kiosk> /home/<kiosk>
> sed -e "s/XSession=.*/XSession=fluxbox/" /var/lib/AccountService/users/<staff> | sudo tee /var/lib/AccountService/users/<kiosk>
> # edit /etc/gdm3/custom.conf for auto login
> # [daemon]
> # AutomaticLoginEnable = true
> # AutomaticLogin = <kiosk>```