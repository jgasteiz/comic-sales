import os

import sendgrid
from sendgrid.helpers import mail as mail_helpers


def send_sale_email(sale):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get("SENDGRID_API_KEY"))
    from_email = mail_helpers.Email(os.environ.get("FROM_EMAIL"))
    to_email = mail_helpers.Email(os.environ.get("TO_EMAIL"))
    subject = f"New comic sale - {sale.title}"
    content = mail_helpers.Content("text/plain", sale.url)
    mail = mail_helpers.Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())


def send_wishlist_item_email(wishlist_comic):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get("SENDGRID_API_KEY"))
    from_email = mail_helpers.Email(os.environ.get("FROM_EMAIL"))
    to_email = mail_helpers.Email(os.environ.get("TO_EMAIL"))
    subject = f"Wishlist comic on sale - {wishlist_comic.title}"
    content = mail_helpers.Content("text/plain", wishlist_comic.url)
    mail = mail_helpers.Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())
