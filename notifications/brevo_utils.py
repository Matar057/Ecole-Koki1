import re
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings


def _parse_email_from_header(header):
    match = re.search(r'<([^>]+)>', header)
    return match.group(1) if match else header


def send_brevo_email(subject, content, recipient_list, sender_name=None, sender_email=None):
    if not recipient_list:
        return False

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    sender_email = sender_email or _parse_email_from_header(settings.DEFAULT_FROM_EMAIL)
    sender_name = sender_name or "Ecole Elementaire Koki 1"

    to = [{'email': email} for email in recipient_list]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        sender={'name': sender_name, 'email': sender_email},
        to=to,
        subject=subject,
        text_content=content,
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        return True
    except ApiException:
        return False
