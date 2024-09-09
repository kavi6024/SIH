import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from send_mail import SendMail

# def send_email(_from: str, _pass: str, _to: str, subject: str, html):
#     # Configuration
#     port = 587
#     smtp_server = "live.smtp.mailtrap.io"
#     login = _from  # Your login generated by Mailtrap
#     password = _pass  # Your password generated by Mailtrap
#     sender_email = _from
#     receiver_email = _to
#     # Create a multipart message and set headers
#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     message["Subject"] = subject
#     # Attach the HTML part
#     message.attach(MIMEText(html, "html"))
#     # Send the email
#     with smtplib.SMTP(smtp_server, port) as server:
#         server.starttls()
#         server.login(login, password)
#         server.sendmail(sender_email, receiver_email, message.as_string())

# def send_email__(_from: str, _pass: str, _to: str, subject: str, html):
#     new_mail = SendMail(
#         # List (or string if single recipient) of the email addresses of the recipients
#         [_to], 
#         # Subject of the email
#         subject,
#         # Body of the email
#         html,
#         # Email address of the sender
#         # Leave this paramter out if using environment variable 'EMAIL_ADDRESS'
#         _from
#     )
#     new_mail.send(_pass)

def send_email(_from: str, _pass: str, _to: str, subject: str, html):
    
    port = 587  # For starttls
    '''
    Ports 465 and 587 are intended for email client to email server communication - sending out email using SMTP protocol. Port 465 is for smtps (smtp secure). SSL encryption is started automatically before any SMTP level communication. Port 587 is for msa (message submission agent).
    Since, Google doesn't allow less secure apps to send mails, we use port 587 rather than port 465.
    '''
    smtp_server = "smtp.gmail.com"
    sender_email = _from
    receiver_email = _to
    password = _pass
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = _from
    message['To'] = _to
    message.attach(MIMEText(html, 'html'))
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

key = 1912

def encrypter(text: str) -> str:
    ascii_vals = [ord(i)*key for i in text]
    ascii_str = "-".join([str(i) for i in ascii_vals])
    return ascii_str

def decrypter(text: str) -> str:
    ascii_str = [int(i) for i in text.split("-")]
    ascii_vals = "".join([chr(int(i/key)) for i in ascii_str])
    return ascii_vals

'''
219880-217968-200760-204584-185464-225616-200760-214144-217968-200760-231352-185464-210320-97512-122368-196936-208408-185464-200760-206496-87952-189288-212232-208408
196936-208408-185464-200760-206496-204584-185464-225616-200760-122368-103248-91776-95600-99424
'''

# from: 191200-217968-200760-225616-193112-212232-210320-193112-93688-95600-91776-97512-122368-196936-208408-185464-200760-206496-87952-189288-212232-208408
# pwd: 206496-212232-212232-219880-223704-204584-185464-225616-200760-122368-93688-108984-93688-95600


def create_html_representation(data):
    html = f'''
    <html>
    <head>
        <style>
            /* Add your CSS styles here */
            body {{
                font-family: Arial, sans-serif;
            }}
            h1 {{
                color: #333;
                font-size: 24px;
            }}
            /* Add more styles as needed */
        </style>
    </head>
    <body>
        <p><strong>Leakage Current:</strong> {data['leakage_current']}</p>
        <p><strong>Earth Resistance:</strong> {data['earth_resistance']}</p>
        <p><strong>Temperature:</strong> {data['temperature']}</p>
        <p><strong>Humidity:</strong> {data['humidity']}</p>
        <p><strong>Voltage:</strong> {data['voltage']}</p>
        <p><strong>Continuity Status:</strong> {data['continuity_status']}</p>
        <p><strong>Phase:</strong> {data['phase']}</p>
    '''

    return html