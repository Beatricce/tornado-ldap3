import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler, url, RedirectHandler
import ldap3
import requests, cv2, os 



from ldap3 import Server, Connection, ALL, ObjectDef, Reader, Writer

# from aux_utils.pic_handler import PIChandler 
# from aux_utils import count_files_in_directory 
# from aux_utils.pq_face_recognition import PQ_face_recognition 
# from aux_utils import decode_transmission, pq_logger 

# logger = pq_logger(stdout = True, name = 'load data from bp') 
# pics = PIChandler(logger = logger) 
# fr = PQ_face_recognition(logger = logger, pic_data=pics) 



def load_data(user, pwd): 
	user = 'admin'
	pwd = 'Secret123'
	server = Server('ipa.demo1.freeipa.org', use_ssl=True, get_info=ALL)
	conn = Connection(server, 'uid=' + user +',cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', pwd, auto_bind=True)
	#conn.add('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'organizationalUnit')
	#conn.add('cn=b.young,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'inetOrgPerson', {'givenName': 'Beatrix', 'sn': 'Young', 'departmentNumber': 'DEV', 'telephoneNumber': '1111'})
	obj_inetorgperson = ObjectDef('inetOrgPerson', conn)
	r = Reader(conn, obj_inetorgperson, 'ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org')
	#json = r[0].entry_to_json(include_empty=False)
	r.search()
	#w = Writer.from_cursor(r)
	print('r:', r[0])
	#print(conn.result)
	return conn



class MainHandler(RequestHandler):
	def get(self):
		# self.write('<a href="%s">link to story 1</a>' %
		# 		self.reverse_url("story", "1"))
		# items = ["Item 1", "Item 2", "Item 3"]
		# self.render("template.html", title="My title", items=items)
		self.render("index.html")
	def post(self):
	 	username = self.get_body_argument("username")
	 	pwd = self.get_body_argument("pwd")
	 	conn = load_data(username,pwd)
	 	print(conn)
	# 	self.redirect(self.reverse_url("qqr"))


class StoryHandler(RequestHandler):


    def get(self, story_id):
        self.write("this is story %s" % story_id)

def make_app():
	return tornado.web.Application([
			url(r"/", MainHandler),
			url(r"/story/([0-9]+)", StoryHandler,  name="story"),
			url(r"/qqr", RedirectHandler,
		dict(url="https://www.google.com.br/"), name="qqr"),
			url(r"/app", RedirectHandler,
		dict(url="https://www.google.com.br/")),
		],
		template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )

if __name__ == "__main__":
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.instance().start()


# Accessing ldap3 server with auth: conn = Connection(server, user="Domain\\User", password="password", authentication=NTLM)
# Accessing DIT:conn = Connection(server, 'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', 'Secret123', auto_bind=True)



