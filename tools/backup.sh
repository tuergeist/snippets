#!/bin/bash

DAYOFY=$(date +"%j")
TAR=/bin/tar
TMPBACKUP_FILE=/backup/cb/level-2-$DAYOFY.tgz
LEVEL0FILE=/backup/cb/level-0-$DAYOFY.tgz
INCREMENTAL_FILE=/backup/cb/incremental.til

tar_args=/home/cb

if [ ! -d $(dirname "$TMPBACKUP_FILE") ] ; then
	echo "Backup destination directory is missing"
	echo "Backup file should have been $TMPBACKUP_FILE"
	exit 1
fi

if [ -f $TMPBACKUP_FILE ] ; then
	echo "A backup for today already exists. -> $TMPBACKUP_FILE "
	exit 2
fi

[ ! -f $INCREMENTAL_FILE ] && TMPBACKUP_FILE=$LEVEL0FILE


CMD="$TAR -czf $TMPBACKUP_FILE   \
--one-file-system --numeric-owner \
$tar_args            \
--exclude-tag=.nobackup-flag \
--exclude=Trash \
--exclude=Cache \
--exclude=*.iso \
--listed-incremental=$INCREMENTAL_FILE \
--totals "

echo "Starte Backup $CMD"
$CMD
RES=$?
if [ $RES -ne 1 ] ; then
	echo "ok"
	cp $INCREMENTAL_FILE $INCREMENTAL_FILE-$DAYOFY
else
	exit 1
fi

echo "fertig"
