import datetime
import json
import smtplib

from django.conf import settings
from django.core import mail
from django.utils import timezone

from comixology import models
from sendgrid.helpers import mail as mail_helpers


class UnableToSendEmail(Exception):
    pass


def send_sale_email(sale: models.Sale):
    _send_email(
        subject=f"New comixology sale - {sale.title}",
        body_text=f"{sale.title}, ends on {sale.date_end.isoformat()}\n{sale.url}",
        from_address=settings.FROM_EMAIL,
        to_address=settings.TO_EMAIL,
        item_id=sale.id,
        item_title=sale.title,
    )


def send_wishlist_item_email(wishlist_comic: models.WishListComic):
    _send_email(
        subject=f"Wishlist comic on sale - {wishlist_comic.title}",
        body_text=wishlist_comic.url,
        from_address=settings.FROM_EMAIL,
        to_address=settings.TO_EMAIL,
        item_id=wishlist_comic.id,
        item_title=wishlist_comic.title,
    )


def _send_email(
    *,
    subject: str,
    body_text: str,
    from_address: str,
    to_address: str,
    item_id: int,
    item_title: str,
):
    with mail.get_connection() as connection:
        email = mail.EmailMultiAlternatives(
            subject=subject,
            body=body_text,
            from_email=from_address,
            to=[to_address],
            connection=connection,
        )

    email.extra_headers = {
        "X-SMTPAPI": json.dumps(_get_smtp_api_headers(item_id, item_title))
    }

    try:
        email.send(fail_silently=False)
    except smtplib.SMTPException as e:
        raise UnableToSendEmail(str(e))


def _get_smtp_api_headers(item_id, item_title):
    send_at = timezone.now() + datetime.timedelta(minutes=2)
    return {
        "unique_args": {"sale_id": item_id, "sale_title": item_title},
        "send_at": int(send_at.timestamp()),
    }
