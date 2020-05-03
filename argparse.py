#!/usr/bin/python3.5
import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

# required arguments
parser.add_argument("-num","--number", help="Required. indicates the number of top lines", nargs=1, type=int, required=True)
parser.add_argument("-d","--day", help="Required. indicates the day range", nargs=1, type=str, required=True)

# the following mutually exclusive arguments (i.e. only one from the list can be applied)
group.add_argument("-r","--resources", help="counts how many times each resource has been requested. The output is two columns. The first is the count and the second is the name of the resource. The output should be sorted by count in descending order.",
action="store_true")
group.add_argument("-req","--requesters", help="counts how many times each source IP has requested a resource. The output is two columns. The first is the count and the second is the IP. The output should be sorted by count in descending order.",
action="store_true")
group.add_argument("-err","--errors", help="has the same specification as the --resources option except, that it only shows log entries that have HTTP status codes in the 400's or the 500's.",
action="store_true")
group.add_argument("-hour","--hourly", help="counts the requests that come in each hour (from 0–23). The output is two columns. The first is the count and the second is the date/hour. The output should be sorted by count in descending order. This option is always sorted by hour.", 
action="store_true")

# positional argument does not begin with a hyphen
parser.add_argument("file", help="Required. Enter file path to be parsed.", type=str)

args = parser.parse_args();
days = args.day[0].split('-')
print(args)
http_log = open(args.file, encoding="ISO-8859-1")

if args.resources:
 print('... doing resources ..')
 resource_list = []
 for line in http_log:
  x = line.split(' ')
  try:
   date = x[3]
  except:
   continue
  y = line.split('"')
  if int(x[3][1:3]) > int(days[0]) and int(x[3][1:3]) < int(days[1]):
   try:
    resource = y[1]
   except:
    continue
   resource_list.append(resource)
 d = dict((w,resource_list.count(w)) for w in set(resource_list))
 sorted_d = sorted(d.items(), key=lambda x: x[1], reverse=True)
 try:
  for i in range(args.number[0]):
   print(sorted_d[i][0], sorted_d[i][1])
 except:
  print("Wrong number range.") 

if args.requesters:
 print('... doing requesters ..')
 requester_list = []
 for line in http_log:
  x = line.split(' ')
  try:
   date = x[3]
  except:
   continue
  if int(x[3][1:3]) > int(days[0]) and int(x[3][1:3]) < int(days[1]):
   try:
    requester = x[0]
   except:
    continue
   requester_list.append(requester)
 d = dict((w,requester_list.count(w)) for w in set(requester_list))
 sorted_d = sorted(d.items(), key=lambda x: x[1], reverse=True)
 try:
  for i in range(args.number[0]):
   print(sorted_d[i][0], sorted_d[i][1])
 except:
  print("Wrong number range.")

if args.errors:
 print('... doing errors ..')
 resource_list = []
 for line in http_log:
  x = line.split(' ')
  try:
   code = line.split()[-2]
  except:
   continue
  y = line.split('"')
  if int(x[3][1:3]) > int(days[0]) and int(x[3][1:3]) < int(days[1]):
   if int(code) >= 400 and int(code) < 600:
    try:
     int(y[2][1:4])
     resource = y[1]
    except:
     resource = y[1]+y[2]
    resource_list.append(resource)
 d = dict((w,resource_list.count(w)) for w in set(resource_list))
 sorted_d = sorted(d.items(), key=lambda x: x[1], reverse=True)
 try:
  for i in range(args.number[0]):
   print(sorted_d[i][0], sorted_d[i][1])
 except:
  print("Wrong number range.")
if args.hourly:
 date_list = []
 for line in http_log:
  x = line.split(' ')
  try:
   date = x[3][1:15]
  except:
   continue
  if int(x[3][1:3]) > int(days[0]) and int(x[3][1:3]) < int(days[1]):
   date_list.append(date)
 d = dict((w,date_list.count(w)) for w in set(date_list))
 sorted_d = sorted(d.items(), key=lambda x: x[1], reverse=True)
 try:
  for i in range(args.number[0]):
   print(sorted_d[i][0], sorted_d[i][1])
 except:
  print("Wrong number range.")
