#!/bin/bash
##############################################################################
#
# Bash testing functions, v2.1
# (C)'Christoph Becker, 2006-2011
# mail@ch-becker.de
# 
# Apache License Version 2.0, http://www.apache.org/licenses/LICENSE-2.0.html
#  
##############################################################################
let test_fail=0
let test_pass=0
current=

function debug {
	if [ $# -eq 1 ] ; then
		LEVEL=1
		echo " $1"	
	else
		LEVEL=$1
		MSG="$2"
		[ "$LEVEL" == "$SHELLTEST_DEBUG" ] && echo " $MSG"
	fi
}


function error {
	[ -z "$SHELLTEST_DEBUG" ] && echo -n "F" || echo " [FAILED] " >/dev/stderr
	let "test_fail=test_fail + 1"
	tests_with_error=$(echo $tests_with_error; echo " - $current; $@" )
}

function passed {
	[ -z "$SHELLTEST_DEBUG" ] && echo -n "." || echo " [OK]"
	let "test_pass=test_pass + 1"
}

function report {
	echo
	echo $test_pass OK
	echo $test_fail FAILED 
	[ $test_fail -gt 0 ] && ( echo "$tests_with_error"; exit 1)
}

function run_tests {
	tests=$(grep test\_ $0 | grep function | cut -f 2 -d" ")
	for i in $tests ; do
		[ -z "$SHELLTEST_DEBUG" ] || echo "[TEST: $i] ..." 
		current=$i
		$i
	done
	report
}

# run a cmd, redirect everything to dev/null and return exit code
function run_quiet {
	$@ &> /dev/null
	R=$?
	#echo R=$R
	return $R
}

# test against expected exitcode
# expected_rc "cmdline to run"
function assert_exits_with {
	debug 2 "exits ($2) with ($1) ?"
	X=$(run_quiet $2)
	assert_same $1 $?
}

# expected actual
function assert_same {
	debug 2 "same ($1, $2) ?"
	[ "$1" == "$2" ] || error "'$2' is not '$1', which was expected"
	passed
}

# expected actual
function assert_not_same {
	debug 2 "not same ($1, $2) ?"
	[ "$1" != "$2" ] || error "'$2' is same as '$1', which was not expected"
	passed
}
