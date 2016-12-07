from ovp_core.emails import BaseMail

class OrganizationMail(BaseMail):
  """
  This class is responsible for firing emails for organizations
  """
  def __init__(self, organization, async_mail=None):
    super(OrganizationMail, self).__init__(organization.owner.email, async_mail)

  def sendOrganizationCreated(self, context={}):
    """
    Sent when organization is created
    """
    return self.sendEmail('organizationCreated', 'Your organization was created', context)

  def sendOrganizationPublished(self, context={}):
    """
    Sent when organization is published
    """
    return self.sendEmail('organizationPublished', 'Your organization was published', context)
