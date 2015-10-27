zenoss-smstrade
================

Plugin for Zenoss to send SMS Alerts using the smstrade.de service

Script source: https://github.com/victorhahncastell/zenoss-smstrade

Published on BSD License


Installation instructions
-------------------------

1.	Save the script to the location: $ZENHOME/bin/zenoss_smstrade.py (where $ZENHOME is your Zenoss directory). Ensure that it's executable (chmod 755 zenoss_smstrade.py).


3. Add a cell phone number to the "Pager" field of each Zenoss user account.


4. Go to Advanced->Settings and modify the "Page Command" to:

     $ZENHOME/bin/zenoss_smstrade.py zenoss_smstrade \<API key\> $RECIPIENT \<route\> [from] [debug] [log]

     Where:

     API KEY: your personal key as assigned by smstrade

     Recipient: Recipient's cell number -- use $RECIPIENT to have Zenoss automatically expand this

     Route: One of basic, gold, direct -- refer to smstrade website

     From: Sender information (max 11 characters or 16 digits)

     Debug: If set to 1, tell the smstrade API we're just testing and don't want to really send SMS.

     Log: Set to 1 to log to [ZENHOME]/log/smstrade.log


5. When finished, test by using the "test" link next to the cell number
shown in the Pager column of each user.


6. If testing is successful (a SMS message is received at the cell phone) create alerts in Zenoss and specify "page" as the action for an alert.
