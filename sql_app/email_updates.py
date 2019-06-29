from sqlalchemy.orm import Session
from email.message import EmailMessage
import smtplib

from . import schemas, crud, config

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

def compose_message(subject: str, body: str, email: str):
	msg = EmailMessage()
	msg.set_content(body)
	msg["Subject"] = subject
	msg["From"] = "aurum.luna333@gmail.com"
	msg["To"] = email
	return msg

def create_server():
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(config.GMAIL_USERNAME, config.GMAIL_PASSWORD)
	return server


def quit_server(s):
	s.quit()


def send_email_update(db: Session, event_id: int):
	db_event = crud.get_event(db, event_id=event_id)
	subject = construct_subject(db_event)
	body = construct_body(db_event)

	s = create_server()

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

		message = compose_message(subject=subject, body=body, email=email)
		s.send_message(message)

	quit_server(s)

