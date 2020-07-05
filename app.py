#!/usr/bin/env python
import re
from datetime import datetime

def parsefile(logfile):
  '''
  Parses the provided logfile into a list of dictionaries
  '''

  parsedData = []
  
  lineformat = re.compile(r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<referrer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""", re.IGNORECASE)

  for l in logfile.readlines():
    data = re.search(lineformat, l)
    if data:
      datadict = data.groupdict()
      
      parsedData.append({
        "ip": datadict["ipaddress"],
        "time": datetime.strptime(datadict["dateandtime"], "%d/%b/%Y:%H:%M:%S %z"),
        "url": datadict["url"],
        "bytessent": datadict["bytessent"],
        "referrer": datadict["referrer"],
        "useragent": datadict["useragent"],
        "status": datadict["statuscode"],
        "method": data.group(6)
      })
  
  return parsedData


def analyser(logfilename, starttimestr, endtimestr, errorcode):
  '''
  Analyses the logs to find the number of successful and error responses
  '''

  logfile = open(logfilename)
  starttime = datetime.strptime(starttimestr, "%d/%b/%Y:%H:%M:%S %z")
  endtime = datetime.strptime(endtimestr, "%d/%b/%Y:%H:%M:%S %z")

  logs = parsefile(logfile)

  numOfRequests, numOfSuccess, numOfError = 0, 0, 0
  for log in logs:
    if log["time"] >= starttime and log["time"] <= endtime:
      numOfRequests += 1
      if log["status"] == "200":
        numOfSuccess += 1
      elif log["status"] == errorcode:
        numOfError += 1
  
  print("The site has returned a total of", numOfSuccess, "200 responses, and", \
    numOfError, errorcode, "responses, out of total", numOfRequests, "requests between time", \
    starttimestr, "and time", endtimestr, "That is a", str(numOfError / numOfRequests * 100) + "%", \
    errorcode, "errors and", str(numOfSuccess / numOfRequests * 100) + "% of 200 responses.")


def main():
  logfilename = input("Enter logfile name: ")
  starttime = input("Enter start time: ")
  endtime = input("Enter end time: ")
  errorcode = input("Enter error code: ")

  analyser(logfilename, starttime, endtime, errorcode)

main()