import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from helperFunctions.auth import get_gmail_service


def _encode_message(message):
    return base64.urlsafe_b64encode(message.as_bytes()).decode()


def list_messages(query="", max_results=10):
    """query uses Gmail search syntax e.g. 'is:unread', 'from:someone@email.com'"""
    service = get_gmail_service()
    result = (
        service.users()
        .messages()
        .list(userId="me", q=query, maxResults=max_results)
        .execute()
    )
    return result.get("messages", [])


def get_message(msg_id: str, format="full"):
    service = get_gmail_service()
    return service.users().messages().get(userId="me", id=msg_id, format=format).execute()


def get_unread_messages(max_results=10):
    return list_messages(query="is:unread", max_results=max_results)


def search_messages(query: str, max_results=10):
    return list_messages(query=query, max_results=max_results)


def send_email(to: str, subject: str, body: str, sender="me"):
    service = get_gmail_service()
    message = MIMEText(body)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    return (
        service.users()
        .messages()
        .send(userId="me", body={"raw": _encode_message(message)})
        .execute()
    )


def reply_to_email(msg_id: str, to: str, subject: str, body: str):
    service = get_gmail_service()
    original = get_message(msg_id, format="metadata")
    thread_id = original.get("threadId")

    message = MIMEText(body)
    message["to"] = to
    message["subject"] = f"Re: {subject}"

    return (
        service.users()
        .messages()
        .send(userId="me", body={"raw": _encode_message(message), "threadId": thread_id})
        .execute()
    )


def create_draft(to: str, subject: str, body: str):
    service = get_gmail_service()
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    return (
        service.users()
        .drafts()
        .create(userId="me", body={"message": {"raw": _encode_message(message)}})
        .execute()
    )


def mark_as_read(msg_id: str):
    service = get_gmail_service()
    service.users().messages().modify(
        userId="me", id=msg_id, body={"removeLabelIds": ["UNREAD"]}
    ).execute()


def mark_as_unread(msg_id: str):
    service = get_gmail_service()
    service.users().messages().modify(
        userId="me", id=msg_id, body={"addLabelIds": ["UNREAD"]}
    ).execute()


def trash_message(msg_id: str):
    service = get_gmail_service()
    service.users().messages().trash(userId="me", id=msg_id).execute()


def list_labels():
    service = get_gmail_service()
    result = service.users().labels().list(userId="me").execute()
    return result.get("labels", [])
