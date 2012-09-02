from django.core.paginator import Paginator, Page

# http://stackoverflow.com/questions/2679370/extend-django-core-paginator-paginator-to-work-with-google-app-engine

class GAEPaginator(Paginator):
  def page(self, number):
    "Returns a Page object for the given 1-based page number."
    number = self.validate_number(number)
    offset = (number - 1) * self.per_page
    if offset+self.per_page + self.orphans >= self.count:
      top = self.count
    return Page(self.object_list.fetch(self.per_page, offset), number, self)
