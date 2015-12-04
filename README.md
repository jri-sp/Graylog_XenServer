# Graylog_XenServer

A basic set of Python scripts to send XenServer data information to GrayLog2 through GELF

## Introduction

[GrayLog](https://www.graylog.org/) is a great tool for logs aggregation. It offers a good subset of functionalities for logs collection, search, analysis and it's open-source.

This set of [Python](https://www.python.org/) scripts aims to provide a data source for [XenServer](http://xenserver.org/), which feed GrayLog to make an overview of your virtualization infrastucture.
The scripts aims to be as simple as possible and requires only **Python 2.4** and **simplejson** that should hopefully be installed in any XenServer server. 
Information is transmitted using the **GELF** format via **UDP** datagram, but TCP or HTTP could be added later for more reliability and security. 
The scripts are triggered by **cron**.

## Installation

The installation is done by the following steps:

   1. Launch a new input in GrayLog
   
   2. Clone repo and configuring the scripts
   
   3. Set up a cron job to run the script periodically

### Graylog's Input

An input need to be set up in GrayLog to receive the messages that scripts are going to send. 
Go to GrayLog > System > Inputs and launch a new **GELF UDP** input on port that you want, for example 12201.

### Set up Scripts

The scripts are developped to reside on the file system of a XenServer, but the config file permit to host them to any host that have Python compatible version and packages, and possibility to setting up cron job on it.
 
You can just copy the script to the server or simply clone the Git repository.
Unfortunately `git` command is not present on XenServer distribution, but you can download the zip archive:`

`wget https://github.com/jri-sp/Graylog_XenServer/archive/master.zip -O Graylog_XenServer.zip`

Then extract it:

`unzip -j Graylog_XenServer.zip -d Graylog_XenServer` 

Go in unzipped folder and copy the **config.ini.sample** file in **config.ini** and replace the variables with your XenServer/GrayLog credentials and the locations.

Now, you can test the XenServer connection by executing a test script:

`python connectionTest.py`

### Cron Job

The last step is to create multiple cron job that will trigger the script periodicaly. 
Depends on the level of granularity you are trying to achieve, you can decide how often to trigger the script. 

Here is a proposal:
`crontab -e`

```
# Get Pool Info Every Hour
0 * * * * /root/Graylog_XenServer/getPoolInfo.py
# Get Pool Tasks Every Minute
* * * * * /root/Graylog_XenServer/getPoolTasks.py
# Get Pool Virtual Machines Every five minutes
*/5 * * * * /root/Graylog_XenServer/getPoolVM.py
# Get Hosts in the Pool Every five minutes
*/5 * * * * /root/Graylog_XenServer/getHostsInfo.py
# Get Hosts CPUs Every five minutes
*/5 * * * * /root/Graylog_XenServer/getHostCPUInfo.py
# Get SR Info in the Pool every five minutes
*/5 * * * * /root/Graylog_XenServer/getSRInfo.py
# Get VM Performance Data every minute
* * * * * /root/Graylog_XenServer/getVMPerf.py
# Get Hosts Performance Data every minute
* * * * * /root/Graylog_XenServer/getHostsPerf.py
# Get Pool last 24h messages every 5 minutes
*/5 * * * * /root/Graylog_XenServer/getPoolMessages.py
```

Make sure the scripts have executable permission set.

## Limitations

* Doesn't support messages chunking. 
* Due to cron mechanism, smallest granularity that can be achieved with the script is 1 minute. 
* Don't support TCP or HTTP input for now.

## To Do

* Add GELF TCP and HTTP
* Add Dashboard json example
* Make a complete content pack for Graylog

## Contributions Welcome!

This is a very basic set of scripts. 
It can become a much better if we all add our enhancements into it. 
Please feel free to fork the repo and send pull requests to any enhancements you have had the chance to write. 
Thank you.

## Sources
http://xapi-project.github.io/xen-api

http://xenserver.org/partners/developing-products-for-xenserver/18-sdk-development/96-xs-dev-rrds.html

http://xenserver.org/partners/developing-products-for-xenserver/18-sdk-development/102-xs-deve-py-parse.html

https://github.com/xapi-project/xen-api/blob/master/scripts/examples/python/XenAPI.py

http://xenserver.org/partners/developing-products-for-xenserver/2-uncategorised/104-xs-dev-rrd-example-script.html