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


function error {
	echo " $@ in '$current' " >/dev/stderr
	let "test_fail=test_fail + 1"
	tests_with_error="$current $tests_with_error"
}

function passed {
	echo -n "."
	let "test_pass=test_pass + 1"
}

function report {
	echo
	echo $test_pass OK
	echo $test_fail FAILED 
	[ $test_fail -gt 0 ] && ( echo "  -> $tests_with_error"; exit 1)
}

function run_tests {
	tests=$(grep test\_ $0 | grep function | cut -f 2 -d" ")
	for i in $tests ; do
		#echo $i
		current=$i
		$i
	done
	report
}

# expected actual
function assert_same {
	[ "$1" == "$2" ] || error "'$2' is not '$1', which was expected"
	passed
}

# expected actual
function assert_not_same {
	[ "$1" != "$2" ] || error "'$2' is same as '$1', which was not expected"
	passed
}
# === === === Define tests here === === ===
function test_self_same {
	assert_same 1 1
	assert_same 2 "2"
	assert_same "" ""
}
function test_self_not_same {
	assert_not_same 1 2
	assert_not_same 2 "1"
	assert_not_same "" "bla bnla"
}

# === === === Run === === ===
#run_tests
