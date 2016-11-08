import os.path
import torndb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
"""
create table Book(
    id int primary key,
    author text foreign key references Author (id) on delete cascade,
    title text,
    p_year datetime,
    ISBN int unique);

create table Author(
    id int primary key,
    a_date datetime,


"""


define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="test", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="imonomy", help="blog database password")


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class HomeHandler(BaseHandler):
    def get(self):
        auth_count = [
            self.db.query('Select count(*) ')
        ]
        self.render('base.html', auth_count=auth_count, book_count=[40, 100, 500])


class MyApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
        ]
        settings = dict(
            blog_title=u"Tornado Test Search",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "templates", "static"),
            debug=True,
        )
        super(MyApplication, self).__init__(handlers, **settings)
        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


def main():
    app = MyApplication()
    server = tornado.httpserver.HTTPServer(app)

    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    #tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()