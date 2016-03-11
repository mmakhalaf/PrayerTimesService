#!/usr/bin/perl -w
#
# Files were downloaded from www.mosquedirectory.co.uk using wget
# Those were put in a directory, which should passed in to the script on the
# command line.

use warnings;
use strict;
use JSON;

my $arg = $ARGV[0];
if (!defined $arg)
{
	die "No file / directory provided\n";
}

my $mosques = ();
if (-f $arg)
{
	my $info = get_mosque_info($arg);
	push(@$mosques, $info);
}
elsif (-d $arg)
{
	my @files = <$arg/*>;
	my $i = 0;
	for my $f (@files)
	{
		++$i;
		#print("$i out of ", scalar(@files), "\n");
		my $info = get_mosque_info($f);
		push(@$mosques, $info);
	}
}

print "** Creating and Writing JSON\n";
my $txt = to_json($mosques, {pretty => 1});
open(my $h_outfile, ">", "$arg.JSON");
print $h_outfile "$txt\n";
close $h_outfile;


###############################################################################
# Process a mosque information page
# Return a map with various info
#  name      ->
#  address   ->
#  postcode  ->
#  gender    ->
#  telephone ->
#  capacity  ->
#
sub get_mosque_info
{
	my ($webfile) = @_;
	
	my $info = {};
	#	"name"      => "",
	#	"address"   => "",
	#	"postcode"  => "",
	#	"gender"    => "",
	#	"telephone" => "",
	#	"capacity"  => "",
	#   "longitude" => "",
	#   "latitude"  => ""
	#);
	
	open(my $h_webfile, "<", $webfile) or die "Could not read: $!\n";
	
	# Get all lines in the HTML, and remove empty lines
	my @lines = <$h_webfile>;
	@lines = grep { $_ !~ /^\s*$/ } @lines;
	
	# For each line, look for key words to identify each bit of information
	my $line_num = -1;
	my $nlines = scalar(@lines) - 1;
	while ($line_num < $nlines)
	{
		$line_num = $line_num + 1;
		my $line = $lines[$line_num];
		
		if ($line eq "")
		{
			next;
		}
		
		if (! defined $info->{"name"})
		{
			if ($line =~ /^\s*<title>\s*(.*)/)
			{
				$info->{"name"} = $1;
				if ($info->{"name"} =~ /(.*)\s*\(.*\)/)
				{
					$info->{"name"} = $1;
				}
				next;
			}
		}
		
		if (! defined $info->{"address"})
		{
			if ($line =~ />Address : </)
			{
				my $next_line = $lines[++$line_num];
				if ($next_line =~ />\s*(.*)\s*</)
				{
					$info->{"address"} = $1;
				}
				next;
			}
		}
		
		if (! defined $info->{"postcode"})
		{
			if ($line =~ />Postcode :</)
			{
				my $next_line = $lines[++$line_num];
				if ($next_line =~ />\s*(.*)\s*</)
				{
					$info->{"postcode"} = $1;
				}
				next;
			}
		}
		
		if (! defined $info->{"gender"})
		{
			if ($line =~ />Gender Allowed :</)
			{
				my $next_line = $lines[++$line_num];
				if ($next_line =~ />\s*(.*)\s*</)
				{
					$info->{"gender"} = $1;
				}
				next;
			}
		}
		
		if (! defined $info->{"telephone"})
		{
			if ($line =~ />Telephone :</)
			{
				my $next_line = $lines[++$line_num];
				if ($next_line =~ />\s*(.*)\s*</)
				{
					$info->{"telephone"} = $1;
				}
				next;
			}
		}
		
		if (! defined $info->{"capacity"})
		{
			if ($line =~ />Capacity : </)
			{
				my $next_line = $lines[++$line_num];
				if ($next_line =~ />\s*(.*)\s*</)
				{
					$info->{"capacity"} = $1;
				}
				next;
			}
		}
		
		if (! defined $info->{"longitude"} and
		    ! defined $info->{"latitude"})
		{
			if ($line =~ /map\.setCenter\(new\s*GLatLng\((-?\d+\.\d+),\s*(-?\d+\.\d+)/)
			{
				$info->{"latitude"} = $1;
				$info->{"longitude"} = $2;
				next;
			}
		}
	}

	close($h_webfile);
	
	my $msg = "";
	if (!defined $info->{"longitude"})
	{
		$msg = "$msg No longitude\n";
	}
	if (!defined $info->{"latitude"})
	{
		$msg = "$msg No latitude\n";
	}
	if (!defined $info->{"address"})
	{
		$msg = "$msg No address\n";
	}
	if (!defined $info->{"postcode"})
	{
		$msg = "$msg No postcode\n";
	}
	if (!defined $info->{"capacity"})
	{
		$msg = "$msg No capacity\n";
	}
	if (!defined $info->{"gender"})
	{
		$msg = "$msg No gender\n";
	}
	if (!defined $info->{"name"})
	{
		$msg = "$msg No name\n";
	}
	
	if ($msg ne "")
	{
		print "$webfile\n$msg";
	}
	
	return $info;
}
