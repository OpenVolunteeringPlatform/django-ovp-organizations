from django.db import models
from django.utils import timezone

ORGANIZATION_TYPES = (
  (0, 'Organization'),
  (1, 'School'),
  (2, 'Company'),
  (3, 'Group of volunteers'),
)

class Organization(models.Model):
  name = models.CharField('Name', max_length=150)
  website = models.URLField(blank=True, null=True, default=None)
  facebook_page = models.URLField(blank=True, null=True, default=None)
  owner = models.ForeignKey('ovp_users.User')
  address = models.OneToOneField('ovp_core.GoogleAddress', blank=True, null=True)

  type = models.PositiveSmallIntegerField("Type", choices=ORGANIZATION_TYPES)

  highlighted = models.BooleanField(("Highlighted"), default=False, blank=False)
  published = models.BooleanField("Published", default=False)
  published_at = models.DateTimeField("Published date", blank=True, null=True)
  deleted = models.BooleanField("Deleted", default=False)
  deleted_at = models.DateTimeField("Deleted date", blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)

  details = models.CharField('Details', max_length=3000, blank=True, null=True, default=None)
  description = models.CharField('Short description', max_length=160, blank=True, null=True)

  #google_page = models.URLField(blank=True, null=True, default=None)
  #twitter_handle = models.URLField(blank=True, null=True, default=None)
  #uploaded_image = models.ForeignKey('UploadedImage', related_name='uploaded_image', blank=True, null=True)
  #uploaded_cover = models.ForeignKey('UploadedImage', related_name='uploaded_cover', blank=True, null=True)
  #causes = models.ManyToManyField(Cause, blank=True, null=True)
  #volunteer_count = models.IntegerField(null=False, blank=False, default=0)

  def __init__(self, *args, **kwargs):
    super(Organization, self).__init__(*args, **kwargs)
    self.__orig_deleted = self.deleted
    self.__orig_published = self.published

  def __str__(self):
    return self.name


  def delete(self, *args, **kwargs):
    self.deleted = True
    self.save()

  #+- def image_name(self, filename):
  #+-   return NonprofitHelper.nonprofit_image_name(self, filename);

  #-+-def get_projects(self, deleted=False):
  #-+-  return Project.objects.filter(nonprofit=self, deleted=deleted)

  def get_description(self, limit=None):
    if self.description and len(self.description) > 0:
      return self.description if limit is None else Truncator(self.description).chars(limit)
    else:
      description_length = Organization._meta.get_field('description').max_length if limit is None else limit
      return Truncator(self.details).chars(description_length)

  #def get_image_url(self):
  #  return self.image.url if self.image else NONPROFIT_DEFAULT_PROFILE_IMAGE
    #+--if self.not_nonprofit:
    #+--  return self.uploaded_image.get_image_url() if self.uploaded_image else NONPROFIT_DEFAULT_PROFILE_IMAGE
    #+--else:
    #+--  if self.uploaded_image is not None:
    #+--    return self.uploaded_image.get_image_url()
    #+--  else:
    #+--    return self.image.url if self.image else NONPROFIT_DEFAULT_PROFILE_IMAGE

  #def get_cover_url(self):
  #  return self.cover.url if self.cover else NONPROFIT_DEFAULT_COVER_IMAGE
    #+--if self.not_nonprofit:
    #+--  return self.uploaded_cover.get_image_url() if self.uploaded_cover else NONPROFIT_DEFAULT_COVER_IMAGE
    #+--else:
    #+--  if self.uploaded_cover is not None:
    #+--    return self.uploaded_cover.get_image_url()
    #+--  else:
    #+--    return self.cover.url if self.cover else NONPROFIT_DEFAULT_COVER_IMAGE

  #---def get_volunteers(self):
  #---  return Volunteer.objects.filter(
  #---    Q(id__in=self.volunteers.all().values_list('id', flat=True)) |
  #---    Q(apply__project__nonprofit__id=self.id)).distinct()

  #---def get_volunteers_numbers(self):
  #---  return Volunteer.objects.filter(
  #---    Q(id__in=self.volunteers.all().values_list('id', flat=True)) |
  #---    Q(apply__project__nonprofit__id=self.id)).distinct().count


  #def mailing(self):
  #  if self.__mailing is None:
  #    self.__mailing = NonprofitMail(self)
  #  return self.__mailing

  def save(self, *args, **kwargs):
    # If _committed == False, it means the image is not uploaded to s3 yet
    # (will be uploaded on super.save()). This means the image is being updated
    # So we update other images accordingly
    #if not self.image._committed:
      # ._file because we need the InMemoryUploadedFile instance
      #+-self.image_small = self.image._file
      #+-self.image_medium = self.image._file
      #+-self.image_large = self.image._file
    #  pass

    if self.pk is not None:
      if not self.__orig_published and self.published:
        self.published_at = timezone.now()
        #self.mailing().sendApproved()

      if not self.__orig_deleted and self.deleted:
        self.deleted_at = timezone.now()

    return super(Organization, self).save(*args, **kwargs)

  class Meta:
    app_label = 'ovp_organizations'
    verbose_name = 'organization'
