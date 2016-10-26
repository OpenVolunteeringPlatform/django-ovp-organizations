from django.utils import text as text_utils

class NonprofitHelper:
	def nonprofit_image_name(self, filename):
		left_path, extension = filename.rsplit('.', 1)
		return 'nonprofit/{}.{}'.format(text_utils.slugify(self.name), extension)

	def nonprofit_cover_name(self, filename):
		left_path, extension = filename.rsplit('.', 1)
		return 'nonprofit-cover/{}.{}' % (text_utils.slugify(self.name), extension)
