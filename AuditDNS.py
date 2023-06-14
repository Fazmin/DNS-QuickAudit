#!/usr/bin/python3

import dns.resolver
import os
import argparse
import platform

def parse_arguments():
    arg_parser = argparse.ArgumentParser(description="Simple DNS auditing script")
    arg_parser.add_argument("ip_list_file", type=str, help="Input file with list of IP's")
    arg_parser.add_argument("dns_server_ip", type=str, help="IP address of DNS server")
    return arg_parser.parse_args()

args = parse_arguments()

def remove_files():
    files_to_remove = ['duplicates.txt', 'errors.txt', 'no_reverse.txt']
    for file in files_to_remove:
        try:
            os.remove(file)
        except OSError:
            print(f'File {file} does not exist')

def format_ip(ip):
    return '.'.join(reversed(ip.split("."))) + ".in-addr.arpa"

def is_host_responsive(host):
    ping_str = "-n 2" if platform.system().lower() == "windows" else "-c 2"
    return os.system("ping " + ping_str + " " + host) == 0

def query_dns(ip):
    request = format_ip(ip)
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [args.dns_server_ip]

    try:
        answers = resolver.query(request, "PTR")
        if len(answers) > 1:
            dns_duplicates += 1
            print("Resolving  " + request)
            with open("duplicates.txt", 'a') as file:
                file.write(ip + "\n")
                for rdata in answers:
                    file.write(str(rdata) + '\n')
                file.write('\n')
    except dns.resolver.NXDOMAIN:
        print("No reverse record for " + ip)
        dns_no_entries += 1
        with open("no_reverse.txt", 'a') as file:
            file.write("No reverse record for " + ip + "\n")
    except Exception as e:
        dns_errors += 1
        print("Resolving  " + request)
        print("Query Failed with error:  " + repr(e))
        with open("errors.txt", 'a') as file:
            file.write("Query Failed for " + ip + " with error:  " + repr(e) + "\n")

dns_errors = 0
dns_no_entries = 0
dns_duplicates = 0

def main():
    with open(args.ip_list_file) as file:
        for ip in file:
            ip = ip.strip()
            query_dns(ip)

    print(f"Total DNS Errors: {dns_errors}")
    print(f"Total DNS Duplicates: {dns_duplicates}")
    print(f"Total IPs with no reverse: {dns_no_entries}")

if __name__ == '__main__':
    main()
