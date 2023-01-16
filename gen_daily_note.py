import datetime
import os.path
import get_gcall as gc
import time
import random
import string

# Generate a random ID for dendron
dendron_id = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=24))
todays_date= '{0:%Y-%m-%d}'.format(datetime.datetime.now())
now = int(time.time()*1000)

BODY = """---
id: {}
title: '{}'
desc: ''
updated: {}
created: {}
traitIds:
- journalNote
---

## Meetings
{}
## General
""".format(dendron_id,todays_date,now,now,"{}")

print(BODY)


MEETING_BLOB =  """---
id: {}
title: {}
desc: ''
updated: {}
created: {}
traitIds:
  - meetingNote
---

## Attendees

<!-- Meeting attendees. If you prefix users with an '@', you can then optionally click Ctrl+Enter to create a note for that user. -->

- {}
## Questions to ask

## Goals

<!-- Main objectives of the meeting -->

## Agenda

<!-- Agenda to be covered in the meeting -->

## Minutes

<!-- Notes of discussion occurring during the meeting -->

## Action Items
- [ ] Goldfish Actions


- [ ] Client Actions
"""

def generate_meeting_md(event_name,event_description,attendees_emails):
    """
    Generates a new markdown file for a meeting with the specified event name, description, and attendee emails. 
    The file will be named in the format "meet.YYYY.MM.DD.event_name.md" and will include a unique dendron_id, 
    the event name, and the attendee emails.
    :param event_name: str, name of the event
    :param event_description: str, event description
    :param attendees_emails: list of str, emails of the attendees
    :return: None
    """
    dendron_id = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=24))
    now = int(time.time()*1000)                             
    formatted_meeting = MEETING_BLOB.format(dendron_id,event_name,now,now,attendees_emails)
    
    date = '{0:%Y.%m.%d}'.format(datetime.datetime.now())
    fname = "meet."+ date +"."+event_name + ".md"
    with open(fname, 'w') as f:
        f.write(formatted_meeting)


def format_gc():
    event_info = gc.main()
    finial_meetings_text_blob = ""
    date = '{0:%Y.%m.%d}'.format(datetime.datetime.now())
    
    for event in event_info:
        meetings_text_blob = """\n ### {} \n ({}) \n Attendees:{}"""
        
        formated_event_name = event['event_name'].strip().replace(":","--").replace(".","").replace("@","").replace("/","").replace("<","").replace(">","").replace("|","").replace("&","")

        event_name_journal = formated_event_name + "[[{}]]".format("meet."+ date +"."+ formated_event_name + ".md")
        
        event_name = event['event_name'].replace(":","--")
        event_description = event['event_description']
        attendees_emails = ""
        for attendees in event['attendees']:
            print(attendees['email'])
            attendees_emails = attendees_emails + " " + attendees['email']
        print(attendees_emails)
        meetings_text_blob = meetings_text_blob.format(
            event_name_journal, event_description, attendees_emails)
        finial_meetings_text_blob = finial_meetings_text_blob + meetings_text_blob
        generate_meeting_md(formated_event_name,'',attendees_emails)
    return(finial_meetings_text_blob)


def main():
    date = '{0:%m-%d-%Y}'.format(datetime.datetime.now())
    # fname = "./goldfish/daily/" + date + ".md"
    # fname = date + ".md"
    # daily.journal.2022.11.07
    fname  = "daily.journal." + '{0:%Y.%m.%d}'.format(datetime.datetime.now()) + ".md"
    meetings = format_gc()
    body =  BODY.format(meetings)
    # print(body)
    if os.path.exists(fname):
        print("FILE ALREADY EXISTS")
        exit(1)

    with open(fname, 'w') as f:
        f.write(body)

    folder_name  = "transcripts/" + date
    if os.path.exists(folder_name):
        print("Folder already Exists")
        exit(1)
    
    else:
        os.mkdir(folder_name)
        print("Generated Transcripts Folder")

    print("generated new daily entry file")


if __name__ == "__main__":
    main()
