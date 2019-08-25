from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import sys

# Setup the Gmail API
SCOPES = 'https://mail.google.com/'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))
me = "email@gmail.com"
keyword = "larger:1"
print("The keyword is " + keyword)

# Get messages
req = service.users().messages().list(userId='me', q=keyword)
res = req.execute()
messages = res.get('messages')

if messages is None or len(messages) <= 0:
    print("No Email found")
    sys.exit(0)

# Show message titles
print("Here is some of the mails.")
print()
for m in messages[:10]:
    mail = service.users().messages().get(userId=me, id=m['id'],
            format='metadata').execute()
    print(mail['snippet'])
print()
print("Is these looks like the mails you want to delete? Print enter to continue, Ctrl+C to exit.")

total = 0

print("Start delete mails, search keyword: " + keyword)
while messages != None and len(messages) > 0:
    count = len(messages)
    print("Deleting %d emails" % count)
    ids = {'ids': [m['id'] for m in messages]}
    deleted = service.users().messages().batchDelete(userId='me',
            body=ids).execute()
    total += count
    print("Deleted %d emails" % total)
    req = service.users().messages().list_next(req, res)
    if req is None:
        break
    res = req.execute()
    messages = res.get('messages')
