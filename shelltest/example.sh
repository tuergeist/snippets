#!/bin/bash
# example test file
# 
SUT=ls
. testsh.sh

# set empty .. default
# 1 for some verbosity
# 2 for most verbosity
SHELLTEST_DEBUG=

# === === === Define tests here === === ===

function test_column_with_error {
	$SUT -qwe &>/dev/null
	assert_same 2 $?	
}

function test_assert_exit_with {
	# same as test_column_with_error but with automatic output redirection
	assert_exits_with 2 "$SUT -qwe"
}

function test_has_output {
	output=$($SUT)
	assert_same 0 $?
	assert_not_same "" $output
}

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
# finding and running tests is provided by the framework
# this will also report statistics to the console
run_tests