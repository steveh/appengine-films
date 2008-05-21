import cgi
import wsgiref.handlers
import os
import yaml

from google.appengine.api import users, urlfetch
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template

class Film(db.Model):
  id = db.IntegerProperty()
  title = db.StringProperty()
  status = db.StringProperty()
  year = db.IntegerProperty()
  first_imported = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
  def get(self):
    films = Film.all().order('title')

    template_values = {
      'films': films,
    }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

class ImdbPage(webapp.RequestHandler):
  def get(self):
    id = self.request.get('id')
    url = "http://us.imdb.com/title/tt" + id + "/"

    imdb = urlfetch.fetch(url)

    self.response.out.write(imdb.content)
  
class PostYaml(webapp.RequestHandler):

  def get(self):
    template_values = {}
    path = os.path.join(os.path.dirname(__file__), 'post.html')
    self.response.out.write(template.render(path, template_values))
    
  def post(self):
    y = yaml.load(self.request.get('content'))
    for m in y:
      movie = Film()
      movie.id = m['imdb_id']
      movie.title = m['title']
      movie.status = m['status']
      movie.year = m['year']
      movie.put()

def main():
  application = webapp.WSGIApplication(
    [('/', MainPage), ('/post', PostYaml), ('/imdb', ImdbPage)],
    debug=True
  )
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()