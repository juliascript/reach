from sqlalchemy.orm import Session

from . import schemas, crud

def construct_subject(event: schemas.Event):
	return "%s has changed its location, date, or time" % event.name

def construct_body(event: schemas.Event):
    message = ("Here are the latest details on %s - \n"
                "\nDate: %s"
                "\nTime: %s"
                "\nLocation: %s"
                "\n\n%s"
                ) % (event.name, event.date, event.time, event.location, event.description)
    return message

def send_email_update(db: Session, event_id: int):
	db_event = crud.get_event(db, event_id=event_id)
	subject = construct_subject(db_event)
	body = construct_body(db_event)

	for user in db_event.participants:
		email = user.email 
		# send the email message with subject 

		# the email is going to be the same for every user

		# thinking that the email is the only thing that needs 
		#   to be sent in the queue. if it fails, just add it
		#   back to the queue (deprioritization isn't an issue
		#   in this specific use case, but if it was, an error 
		#   queue would be made)
		print(email)
		print(subject)
		print(body)

