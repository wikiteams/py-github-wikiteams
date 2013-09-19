import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# me == my email address
# you == recipient's email address
me = "sender@wikiteams.pl"
you = "oskar.jarczyk@pjwstk.edu.pl"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "WikiTeams.pl - GitHub repo getter reporting"
msg['From'] = me
msg['To'] = you

# Create the body of the message (a plain-text and an HTML version).
text = "GitHub repo getter reporting!!\nGitHub API quota stands as below:\nGranted: __QUOTA_GRANTED Quota left: __QUOTA__LEFT"
html = """\
<html>
  <head></head>
  <body>
    <p>GitHub repo getter reporting!<br>
       GitHub API quota stands as below:<br>
       Granted: __QUOTA_GRANTED Quota left: __QUOTA__LEFT.
    </p>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Send the message via local SMTP server.
s = smtplib.SMTP('mail.wikiteams.pl', 587)
s.set_debuglevel(1)
s.ehlo()
s.starttls()
s.login('', '')
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
s.sendmail(me, you, msg.as_string())
s.quit()
