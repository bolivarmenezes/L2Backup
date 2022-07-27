#!/bin/bash
watchman watch-del-all
watchman watch-project /srv/backup_switches
watchman -- trigger /srv/backup_switches  'updateFiles' -- updateBackup