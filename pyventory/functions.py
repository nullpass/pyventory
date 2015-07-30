from django.db import IntegrityError
from django.template.defaultfilters import slugify


def UltraSlug(string, model):
    """
    This is another point that Django lets me down.
    Why make a slugify function if there's no built-
    in way to make it unique? That'd be like providing
    and auth system that made the names and email
    addresses case sensitiv-- oh, right. :(
    Dear Dj,
        All I need is this:
        self.slug = slugify(string, unique=True)

    ps. Thank you for the trillions of ways you've
        already made my life easier.


    Example (models.py):
        def save(self, *args, **kwargs):
            self.slug = UltraSlug(self.name, self)
            return super().save()

    """
    try_this_one = string = slugify(string[:32])
    slug_list = model.__class__.objects.exclude(id=model.id).values_list('slug', flat=True).all()
    for index in range(256):
        #
        # I will try 256 times to find a unique slug,
        # after that, it's the dev's problem.
        #
        if try_this_one not in slug_list:
            return try_this_one
        try_this_one = '{0}-{1}'.format(string, index)
    raise IntegrityError('Failed to create a unique slug from {0}'.format(string))
