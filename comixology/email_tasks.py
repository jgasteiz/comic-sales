import datetime

from django.conf import settings

import sendgrid
from sendgrid.helpers import mail as mail_helpers


def send_sale_email(sale):
    subject = f"Comic sale - {sale.title}"
    content_txt = f"""{sale.title}, ends on {sale.date_end.isoformat()}
    {sale.url}"""
    content = mail_helpers.Content("text/plain", content_txt)
    _send_email(subject, content)


def send_wishlist_item_email(wishlist_comic):
    subject = f"Wishlist comic on sale - {wishlist_comic.title}"
    content = mail_helpers.Content("text/plain", wishlist_comic.url)
    _send_email(subject, content)


def _send_email(subject, content):
    client = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    mail = mail_helpers.Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=settings.TO_EMAIL,
        subject=subject,
        plain_text_content=content,
    )
    client.client.mail.send.post(request_body=mail.get())
