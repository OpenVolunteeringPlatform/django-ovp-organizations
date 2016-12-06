from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

ORGANIZATION_TYPES = (
  (0, 'Organization'),
  (1, 'School'),
  (2, 'Company'),
  (3, 'Group of volunteers'),
)

class Organization(models.Model):
  # Relationships
  owner = models.ForeignKey('ovp_users.User')
  address = models.OneToOneField('ovp_core.GoogleAddress', blank=True, null=True)
  image = models.ForeignKey('ovp_uploads.UploadedImage', blank=False, null=True)
  causes = models.ManyToManyField('ovp_core.Cause')

  # Fields
  slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
  name = models.CharField('Name', max_length=150)
  website = models.URLField(blank=True, null=True, default=None)
  facebook_page = models.CharField(max_length=255, blank=True, null=True, default=None)
  type = models.PositiveSmallIntegerField("Type", choices=ORGANIZATION_TYPES)
  details = models.CharField('Details', max_length=3000, blank=True, null=True, default=None)
  description = models.CharField('Short description', max_length=160, blank=True, null=True)

  # Meta
  highlighted = models.BooleanField(("Highlighted"), default=False, blank=False)
  published = models.BooleanField("Published", default=False)
  published_at = models.DateTimeField("Published date", blank=True, null=True)
  deleted = models.BooleanField("Deleted", default=False)
  deleted_at = models.DateTimeField("Deleted date", blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)


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


  #def mailing(self):
  #  if self.__mailing is None:
  #    self.__mailing = NonprofitMail(self)
  #  return self.__mailing

  def save(self, *args, **kwargs):
    if self.pk is not None:
      if not self.__orig_published and self.published:
        self.published_at = timezone.now()
        #self.mailing().sendApproved()

      if not self.__orig_deleted and self.deleted:
        self.deleted_at = timezone.now()
    else:
      # Organization being created
      self.slug = self.generate_slug()
      #self.mailing().

    return super(Organization, self).save(*args, **kwargs)


  def generate_slug(self):
    if self.name:
      slug = slugify(self.name)[0:99]
      append = ''
      i = 0

      query = Organization.objects.filter(slug=slug + append)
      while query.count() > 0:
        i += 1
        append = '-' + str(i)
        query = Organization.objects.filter(slug=slug + append)
      return slug + append
    return None

  class Meta:
    app_label = 'ovp_organizations'
    verbose_name = 'organization'
