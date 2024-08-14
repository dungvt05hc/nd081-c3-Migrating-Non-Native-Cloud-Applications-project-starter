import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime

def main(msg: func.ServiceBusMessage):
    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s', notification_id)

    # Connection string to your PostgreSQL database
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        
        cursor = conn.cursor()

        # Query to get the notification message and subject
        cursor.execute("SELECT subject, message FROM notification WHERE id = %s", (notification_id,))
        notification = cursor.fetchone()

        if notification is None:
            logging.warning('Notification ID %s not found.', notification_id)
            return

        subject, message = notification
        logging.info('Retrieved notification - Subject: %s, Message: %s', subject, message)

        # Query to get attendees' email and first name
        cursor.execute("SELECT email, first_name FROM attendee")
        attendees = cursor.fetchall()

        if not attendees:
            logging.warning('No attendees found.')
            return

        # # Send personalized emails to each attendee
        # for attendee in attendees:
        #     email, first_name = attendee
        #     personalized_subject = f"{subject} - {first_name}"
        #     personalized_message = Mail(
        #         from_email=os.getenv('FROM_EMAIL'),
        #         to_emails=email,
        #         subject=personalized_subject,
        #         plain_text_content=message
        #     )

        #     try:
        #         sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        #         response = sg.send(personalized_message)
        #         logging.info('Email sent to %s, status code: %s', email, response.status_code)
        #     except Exception as e:
        #         logging.error('Error sending email to %s: %s', email, str(e))

        # Update the notification status
        completed_date = datetime.utcnow()
        attendees_count = len(attendees)
        cursor.execute(
            "UPDATE notification SET status = %s, completed_date = %s WHERE id = %s",
            (f'Notified {attendees_count} attendees', completed_date, notification_id)
        )
        conn.commit()
        logging.info('Notification status updated for ID %s with %d attendees notified.', notification_id, attendees_count)

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error('Database error: %s', error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            logging.info('Database connection closed.')
