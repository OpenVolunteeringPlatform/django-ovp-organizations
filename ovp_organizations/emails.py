from ovp_core.emails import BaseMail

class OrganizationMail(BaseMail):
  """
  This class is responsible for firing emails for organizations
  """
  def __init__(self, organization, async_mail=None, override_receiver=False):
    self.async_mail=async_mail

    receiver = organization.owner.email
    if override_receiver:
      receiver = override_receiver

    super(OrganizationMail, self).__init__(receiver, self.async_mail)

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

  def sendUserInvited(self, context={}):
    """
    Sent when user is invited to organization
    """
    # invited user email
    self.__init__(context['invite'].organization, async_mail=self.async_mail, override_receiver=context['invite'].invited.email)
    self.sendEmail('userInvited-toUser', 'You are invited to an organization', context)

    if context['invite'].organization.owner == context['invite'].invitator:
      self.__init__(context['invite'].organization, async_mail=self.async_mail, override_receiver=context['invite'].organization.owner.email)
      self.sendEmail('userInvited-toInviter', 'You invited a member to an organization you own', context)
    else:
      self.__init__(context['invite'].organization, async_mail=self.async_mail, override_receiver=context['invite'].organization.owner.email)
      self.sendEmail('userInvited-toOwner', 'A member has been invited to your organization', context)

      self.__init__(context['invite'].organization, async_mail=self.async_mail, override_receiver=context['invite'].invitator.email)
      self.sendEmail('userInvited-toInviter', 'You invited a member to an organization you are part of', context)

  def sendUserInvitationRevoked(self, context={}):
    """
    Sent when user is invitation is revoked
    """
    # invited user email
    self.__init__(context['invite'].organization, async_mail=self.async_mail, override_receiver=context['invite'].invited.email)
    self.sendEmail('userInvitedRevoked-toUser', 'Your invitation to an organization has been revoked', context)

    if context['invite'].organization.owner == context['invite'].invitator:
      self.__init__(context['invite'].organization, async_mail=self.async_mail, override_receiver=context['invite'].organization.owner.email)
      self.sendEmail('userInvitedRevoked-toInviter', 'You have revoked an user invitation', context)
    else:
      self.__init__(context['invite'].organization, async_mail=self.async_mail, override_receiver=context['invite'].organization.owner.email)
      self.sendEmail('userInvitedRevoked-toOwner', 'An invitation to join your organization has been revoked', context)

      self.__init__(context['invite'].organization, async_mail=self.async_mail, override_receiver=context['invite'].invitator.email)
      self.sendEmail('userInvitedRevoked-toInviter', 'You have revoked an user invitation', context)


  def sendUserLeft(self, context={}):
    """
    Sent when user leaves organization
    """
    self.__init__(context['organization'], async_mail=self.async_mail, override_receiver=context['user'].email)
    self.sendEmail('userLeft-toUser', 'You have left an organization', context)

    self.__init__(context['organization'], async_mail=self.async_mail, override_receiver=context['organization'].owner.email)
    self.sendEmail('userLeft-toOwner', 'An user has left an organization you own', context)


  def sendUserRemoved(self, context={}):
    """
    Sent when user is removed from organization
    """
    self.__init__(context['organization'], async_mail=self.async_mail, override_receiver=context['user'].email)
    self.sendEmail('userRemoved-toUser', 'You have have been removed from an organization', context)

    self.__init__(context['organization'], async_mail=self.async_mail, override_receiver=context['organization'].owner.email)
    self.sendEmail('userRemoved-toOwner', 'You have removed an user from an organization you own', context)

  def sendUserJoined(self, context={}):
    """
    Sent when user joins organization
    """
    self.__init__(context['organization'], async_mail=self.async_mail, override_receiver=context['user'].email)
    self.sendEmail('userJoined-toUser', 'You have joined an organization', context)

    self.__init__(context['organization'], async_mail=self.async_mail, override_receiver=context['organization'].owner.email)
    self.sendEmail('userJoined-toOwner', 'An user has joined an organization you own', context)
