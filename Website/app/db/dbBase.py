import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import logging


log = logging.getLogger(__name__)
class dbInit:

	def __init__(self):

		self.db = None

		config = {
			'user': '',
			'password': '',
			'host': '',
			'database': ''
		}

		try:
			self.db = mysql.connector.connect(**config)
		except Error as e:

			if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				log.error('DB Server Username or Password is Invalid')
			elif e.errno == errorcode.ER_BAD_DB_ERROR:
				log.error("DB Doesn't exist")

			else:
				log.error(e)
		else:
			log.info('Successfully Connected to Database')


