Description: Tools for finding and combining duplicates within a TitaniumBackup SMS/MMS backup file.

Threads are combined according to "address" field (the phone number), and messages are largely considered duplicates if they have the same date. If the contents of duplicate messages differ, they are both retained, even if they have identical dates.


Usage:
First, run parse.sh on the file to add some newlines where expected
Second, run sms_merge.py on "parsable.xml". The results are placed in out.xml
