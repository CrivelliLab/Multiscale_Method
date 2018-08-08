#!/usr/bin/perl

open(FILENAME, "<CG_data.dat");
@input = <FILENAME>;
close FILENAME;
my @sorted = sort { (split(' ', $a))[0] <=> (split(' ', $b))[0] } @input;
#print $sorted;

open(OUT0, ">BiomolecularData.dat");
for (my $h = 0; $h <= $#sorted; ++$h) {
#    print $sorted[$h];
    #my $round = sprintf("%.4f",$sorted[$h]);
    print OUT0 "$sorted[$h]";
}
close(OUT0);

system("rm CG_data.dat")
