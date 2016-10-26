from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
from django.template.loader import get_template
from django.conf import settings

import threading

class EmailThread(threading.Thread):
    def __init__(self, msg):
      self.msg = msg
      threading.Thread.__init__(self)

    def run(self):
      return self.msg.send() > 0


class BaseMail:
  """
  This class is responsible for firing emails
  """
  from_email = ''

  def __init__(self, user, async_mail=None):
    self.user = user
    self.async_mail = async_mail

  def sendEmail(self, template_name, subject, context):
    ctx = Context(context)
    text_content = get_template('email/{}.txt'.format(template_name)).render(ctx)
    html_content = get_template('email/{}.html'.format(template_name)).render(ctx)

    msg = EmailMultiAlternatives(subject, text_content, self.from_email, [self.user.email])
    msg.attach_alternative(text_content, "text/plain")
    msg.attach_alternative(html_content, "text/html")

    if self.async_mail:
      async_flag="async"
    else:
      async_flag=getattr(settings, "DEFAULT_SEND_EMAIL", "async")

    if async_flag == "async":
      t = EmailThread(msg)
      t.start()
      return t
    else:
      return msg.send() > 0

class UserMail(BaseMail):
  """
  This class is responsible for firing emails for Users
  """
  def sendWelcome(self, context={}):
    """
    Sent when user registers
    """
    return self.sendEmail('welcome', 'Welcome', context)


  def sendRecoveryToken(self, context):
    """
    Sent when volunteer requests recovery token
    """
    return self.sendEmail('recoveryToken', 'Password recovery', context)

