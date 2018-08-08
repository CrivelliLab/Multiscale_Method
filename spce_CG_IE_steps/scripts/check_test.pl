#!/usr/bin/perl

my ($rsn0) = @ARGV;

open(OUT, ">G1.txt");
print OUT "del 1\n";
print OUT "r $rsn0\n";
print OUT "name 1 G1\n";
print OUT "q \n";
close(OUT);

system("gmx make_ndx -f aa.gro -n water.ndx -o water1.ndx < G1.txt &>/dev/null");
system("gmx select -f aa.gro -s run_prep.tpr -n water1.ndx -rmpbc -pbc -select 'within 0.6 of com of group G1' -oi -seltype mol_com &>/dev/null");

open(DATA, "<index.dat") or die "Couldn't open file file.txt, $!";
my $line2 = <DATA>;
my @array = split(" ", $line2);

close(DATA) || die "Couldn't close file properly";

# write output to single file
my $i = 0;

#	foreach $_ (@array[2..$#array]) {
foreach $_(@array[2]){
		if ($_ =~ /[#@]/) {
			# do nothing, it's a comment or formatting line
		} else {
			my @line = split(" ", $_);
			my $rsn = $line[0];

			$i = $i + 1;
      print "Processing Molecule #$i...\n";

			if($rsn != $rsn0) {
				open(OUT, ">aa.txt");
					print OUT "del 2\n";
					print OUT "r $rsn\n";
					print OUT "name 2 G2\n";
					print OUT "q \n";
				close(OUT);

			system("gmx make_ndx -f aa.gro -n water1.ndx -o index.ndx  < aa.txt &>/dev/null");
			system("gmx grompp -f grompp.mdp -c aa.gro -n index.ndx -p water.top -o run_aa.tpr &>/dev/null");
			system("gmx mdrun -s run_aa.tpr -rerun aa.gro -e aa.edr &>/dev/null");
			system("gmx energy -f aa.edr -o aa.xvg");
			system("gmx  distance -n index.ndx -select 'com of group G1 plus com of group G2' -oall aa1.xvg -f aa.gro -s run_prep.tpr &>/dev/null");

			open(IN, "< aa.xvg");
			my @array1 = <IN>;

			my $energy;

			foreach $_ (@array1) {
				if ($_ =~ /[#@]/) {
					# do nothing, it's a comment or formatting line
				} else {
					my @line1 = split(" ", $_);
					$energy = $line1[1];
				}
			}

			close(IN);

      open(IN, "< aa1.xvg");
      my @array1 = <IN>;

      my $distance;

      foreach $_ (@array1) {
            if ($_ =~ /[#@]/) {
                # do nothing, it's a comment or formatting line
            } else {
                my @line1 = split(" ", $_);
                $distance = $line1[1];
            }
      }

      close(IN);

			print "Distance (nm) \t Energy (KJ/mol)\n";
			print "$distance \t\t $energy\n";

			#print $rsn,"\n";

                        system("rm md.log");
                        system("rm run_aa.tpr");
                        system("rm aa.xvg");
                        system("rm aa1.xvg");
			system("rm aa.edr");
			system("rm index.ndx");
			system("rm aa.txt");

			}
		}
	}

system("rm index.dat");
system("rm water1.ndx");
system("rm aa.gro");
