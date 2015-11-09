#!/usr/local/bin/perl
use strict;
use warnings;

use lib qw {/home/t12968yy/perl5/lib/perl5};
use XML::FeedPP;

my %journals;

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

print "Content-type: text/html\n";
print '
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
  / <b>text</b>=no    # will only print titles;</p>
<h4>History</h4>
<p>2015-11-08 : Alpha version released.
</p>
';

my %param = map { /([^=]+)=(.+)/ } (split /&/, $ENV{'QUERY_STRING'});
$param{$_} =~ s/%20/ / foreach keys %param;

print "<h4>Parameters in cgi</h4>\n<ul>\n";
print "<li>".$_." : \"".$param{$_}."\"</li>\n" foreach keys %param;
print "</ul>\n<p>";
defined $param{filter} ? print 'Filter is set to "', $param{filter}, '"<br>' : print 'No filter, showing all articles<br>';
defined $param{text} ? print 'Showing only titles<br>' : print 'Showing full text<br>';
print "</p>\n";

print '<h2 id="top">Journal List</h2>'."\n".'<ul>'."\n";
foreach my $journal ( sort keys %journals ) {
    print '<li><a href="reader.cgi#'.$journal.'">'.$journal.'</a>'."</li>\n";
}
print "</ul>\n";

foreach my $journal ( sort keys %journals ) {
    print '<h2 id ='.$journal.'><b>> '.$journal."</h2>".$journals{$journal}."</b>\n\n";
#    print '<a href="reader.cgi#top>Return to top</a>'."\n";
    my $feed    = XML::FeedPP->new( $journals{$journal} );
    foreach my $item ($feed->get_item()) {
	my $flag = $item->title() =~ /$param{filter}/i || $item->description() =~ /$param{filter}/i ? 1 : 0;
	if( $flag ) {
	    print '<h3><b>', $item->title(), "</b></h3>\n";
	    unless( $param{"text"} eq "no" ) {
		print '<p>Authors:', $item->author(), "<br>\n" if length $item->author() > 3;
		print 'Date: ', $item->pubDate(), "</p>\n" if length $item->author() > 3;
		print '<p>', $item->description(), "</p>\n";
	    }
	    print '<p>URL: <a href=', $item->link(), ">".$item->link()."</a></p>\n\n";
	}
    }
    print "<p>///</p>\n\n";
}

print '</body></html>';
