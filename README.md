This Python script is a simple DNS auditing tool. It takes a list of IP addresses from a file and a DNS server IP address as inputs. The script performs reverse DNS lookups on each IP address in the list against the provided DNS server.

##The script keeps track of three types of outcomes:
###If multiple PTR records are returned for an IP address, it's considered a duplicate and the IP address along with the returned PTR **records are written to a file named "duplicates.txt".
###If no PTR record is found for an IP address, it's considered a missing entry and the IP address is written to a file named "no_reverse.txt".
###If there's an error during the DNS query, the error is logged along with the IP address to a file named "errors.txt".
###At the end of the script, it prints out the total number of DNS errors, duplicates, and missing entries encountered during the execution.

This script can be useful to audit DNS records and identify potential issues such as misconfigurations or inconsistencies.
