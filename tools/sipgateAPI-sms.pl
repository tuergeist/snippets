#!/usr/bin/perl -w
#
# Sam Buca, indigo networks GmbH, 08/2007
#
# This script is a very basic perl-client to the SAMURAI service 
# provided by sipgate (indigo networks GmbH) without any claim to 
# completeness and without any warranty!
#
# The following code shows how to use the service to send messages 
# via SMS using a sipgate account.
#

use strict;
use Frontier::Client;	# needed for XMLRPC

# declare some variables for later use:
my $VERSION = "1.0";
my $NAME	= "sipgateAPI-sms.pl";
my $VENDOR	= "indigo networks GmbH";
my $url;
my $xmlrpc_client;
my $xmlrpc_result;
my $args_identify;
my $args;

# check the count of commandline parameters and show usage information 
# if not matching:
unless (@ARGV == 4) {
	print "\n";
	print "This script needs 4 parameters supplied on the commandline:\n";
	print "\n";
	print "parameter 1 -> the username (not SIPID) used to login to sipgate\n";
	print "parameter 2 -> the password associated with the username\n";
	print "parameter 3 -> the number to send the message to\n";
	print "               (with national prefix, e.g. 4917xxxxxxxxx)\n";
	print "parameter 4 -> the message to send quoted in \" or \'\n";
	print "\n";

	exit 0;
}

# define URL for XMLRPC:

$url = "https://$ARGV[0]:$ARGV[1]\@samurai.sipgate.net/RPC2";

# create an instance of the XMLRPC-Client:

$xmlrpc_client = Frontier::Client->new( 'url' => $url );

# identify the script to the server calling XMLRPC-method "samurai.ClientIdentify"
# providing client-name, -version and -vendor:

$args_identify = { ClientName => $NAME, ClientVersion => $VERSION, ClientVendor => $VENDOR };

$xmlrpc_result = $xmlrpc_client->call( "samurai.ClientIdentify", $args_identify );

# the check for success is not necessary in this case since the Frontier::Client module 
# dies with an exception in case of a fault, but we do it for completeness:

if ($xmlrpc_result->{'StatusCode'} == 200) {
    print "Successfully identified to the server!\n";
} else {
	# we should never get here!
	print "There was an error during identification to the server!\n";
}

# create the input argument set for XMLRPC:

$args = { RemoteUri => "sip:$ARGV[2]\@sipgate.net", TOS => "text", Content => $ARGV[3] };

# do the call and store the result / answer to $xmlrpc_result:

$xmlrpc_result = $xmlrpc_client->call( "samurai.SessionInitiate", $args );

# again we do the check on success for completeness:

if ($xmlrpc_result->{'StatusCode'} == 200) {
    print "Your request was successfully send to the server!\n";
} else {
	# we should never get here!
	print "There was an error!\n";
}
