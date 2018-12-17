# jcdssync #

## Overview ##

jcdssync is a simple script, built on the python-jss library, that synchronises distribution point content from or to a
jamfcloud instance.

## Setup ##

You need to create a preferences file to specify the address of your JSS, and credentials.

To do so, issue the following commands:

	defaults write ~/Library/Preferences/com.github.sheagcraig.python-jss.plist jss_user <username>
	defaults write ~/Library/Preferences/com.github.sheagcraig.python-jss.plist jss_pass <password>
	defaults write ~/Library/Preferences/com.github.sheagcraig.python-jss.plist jss_url <url>

You can also supply the username and password as environment variables `JSS_USER` and `JSS_PASSWORD`.

## Usage ##

To sync a local directory to a remote jamfcloud instance, with the local directory taking precedence.

	$ jcdssync ./content https://foo.jamfcloud.com
	
To sync a jamfcloud instance to a local directory, with the jamfcloud instance taking precedence.

	$ jcdssync https://foo.jamfcloud.com ./content
	
### What does precedence mean? ###

- The authoritative source will overwrite files with exactly the same name but different checksums.
- With the `-d|--delete` flag, files not present in the authoritative source will be deleted in the destination.
