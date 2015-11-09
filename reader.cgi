B0;95;c#!/usr/local/bin/perl
use strict;
use warnings;

use lib qw {/home/t12968yy/perl5/lib/perl5};
use XML::FeedPP;

#$ENV{'QUERY_STRING'} = "filter=DNA&text=no";
my %param = map { /([^=]+)=(.+)/ } (split /&/, $ENV{'QUERY_STRING'});
$param{$_} =~ s/%20/ / foreach keys %param;


my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time);
$year += 1900;
$mon += 1;

for(;;){
    if(  -e "log/".$year."_".$mon."_".sprintf("%02d", $mday).".txt"){
	last if $param{remake} eq "yes";
	open my $fl, "<","log/".$year."_".$mon."_".sprintf("%02d", $mday).".txt";
	print join("\n", <$fl>)."\n";
	exit(0);
    }
}

my %journals;
my $output;
## Journal rss links
$journals{"Nature"}       = 'http://feeds.nature.com/nature/rss/current';
$journals{"Nat.Com."}     = 'http://feeds.nature.com/ncomms/rss/current';
$journals{"Cell"}         = 'http://www.cell.com/cell/current.rss';
$journals{"Science"}      = 'http://www.sciencemag.org/rss/current.xml';
$journals{"Genome.Biol."} = 'http://www.genomebiology.com/editorspicks/rss';
$journals{"J.Mol.Biol."}  = 'http://www.journals.elsevier.com/journal-of-molecular-biology/rss';
$journals{"EMBOJ."}       = 'http://emboj.embopress.org/rss/current.xml';
$journals{"DNA-repair"}   = 'http://www.journals.elsevier.com/dna-repair/rss/';
$journals{"PNAS"}         = 'http://www.pnas.org/rss/current.xml';
$journals{"Nuc. Acid. Res."}= 'http://nar.oxfordjournals.org/rss/current.xml';

$output .=  "Content-type: text/html\n";
$output .=  '
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<title>RSS feed on major journals</title>
</head>
<body>
<h2>RSS parser</h2>
<h3>A parser of rss of journals of my liking, if you want a journal to be added, pls contact me.</h3>
<h4>Author : |.+|<br>
Hosted on Github : https://github.com/t12968yy/Journal_rss
</h4>

<h3>Usage</h3>
<p>Access http://web.sfc.keio.ac.jp/~t12968yy/rss/reader.cgi for normal rss.<br>
For parameters, add "&" to the link and the following to your liking<br>
  / <b>filter</b>= "your filter"    # will filter the description and title with your query (not upper case sensitive & space OK)<br>
  / <b>text</b>=no    # will only $output .=  titles;</p>
  / <b>remake</b>=yes    # will remake output. Remake when adding parameters.
<h4>History</h4>
<p>2015-11-08 : Alpha version 0.01 released.
2015-11-09 : v0.21 released. Added logging system for fast access for multiple accesses
</p>
';


$output .=  "<h4>Parameters in cgi</h4>\n<ul>\n";
$output .=  "<li>".$_." : \"".$param{$_}."\"</li>\n" foreach keys %param;
$output .=  "</ul>\n<p>";

$output .= defined $param{filter} ? 'Filter is set to "'.$param{filter}.'"<br>' : 'No filter, showing all articles<br>';
$output .= defined $param{text} ? 'Showing only titles<br>' :  'Showing full text<br>';
$output .=  "</p>\n";

$output .=  '<h2 id="top">Journal List</h2>'."\n".'<ul>'."\n";
foreach my $journal ( sort keys %journals ) {
    $output .=  '<li><a href="reader.cgi#'.$journal.'">'.$journal.'</a>'."</li>\n";
}
$output .=  "</ul>\n";

foreach my $journal ( sort keys %journals ) {
    my $feed    = XML::FeedPP->new( $journals{$journal} );
    $output .=  '<h2 id ='.$journal.'><b>> '.$journal."</h2>".$journals{$journal}."</b>\n\n";
#    $output .=  '<a href="reader.cgi#top>Return to top</a>'."\n";

## Going to add these parsed elements to hash insted of $output, to fix logging system. 
## Not saving the output, but saving the hash.
    foreach my $item ($feed->get_item()) {
	my $flag =  $item->title() =~ /$param{filter}/i || $item->description() =~ /$param{filter}/i ? 1 : 0;
	if( $flag ) {
	    $output .=  '<h3><b>'.$item->title()."</b></h3>\n";
	    unless( $param{"text"} eq "no" ) {
		$output .=  '<p>Authors:'. $item->author()."<br>\n" if length $item->author() > 3;
		$output .=  'Date: '. $item->pubDate(). "</p>\n" if length $item->author() > 3;
		$output .=  '<p>'. $item->description(). "</p>\n";
	    }
	    $output .=  '<p>URL: <a href='.$item->link().">".$item->link()."</a></p>\n\n";
	}
    }
    $output .=  "<p>///</p>\n\n";
}

$output .= "<p>Parsed at ".$year."_".$mon."_".sprintf("%02d", $mday)."</p>\n";
$output .=  '</body></html>';
print $output;


system('touch log/$year."_".$mon."_".sprintf("%02d", $mday).".txt"');
system('chmod 644log/$year"_".$mon."_".sprintf("%02d", $mday).".txt"');
open my $fh, ">", "log/".$year."_".$mon."_".sprintf("%02d", $mday).".txt";
print $fh $output;
close $fh;

__END__

