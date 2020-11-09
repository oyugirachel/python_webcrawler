import abc 
import urllib 
import urllib.error 
import urllib.request 
from bs4 import BeautifulSoup 

class AbstractFactory(object, metaclass=abc.ABCMeta): 
	""" Abstract Factory Interface """
	
	def __init__(self, is_secure): 
		self.is_secure = is_secure 

	@abc.abstractmethod 
	def create_protocol(self): 
		pass

	@abc.abstractmethod 
	def create_port(self): 
		pass

	@abc.abstractmethod 
	def create_crawler(self): 
		pass

class HTTPConcreteFactory(AbstractFactory): 
	""" Concrete Factory for building HTTP connection. """
	
	def create_protocol(self): 
		if self.is_secure: 
			return HTTPSecureProtocol() 
		return HTTPProtocol() 

	def create_port(self): 
		if self.is_secure: 
			return HTTPSecurePort() 
		return HTTPPort() 

	def create_crawler(self): 
		return HTTPCrawler() 

class FTPConcreteFactory(AbstractFactory): 
	""" Concrete Factory for building FTP connection """
	
	def create_protocol(self): 
		return FTPProtocol() 

	def create_port(self): 
		return FTPPort() 

	def create_crawler(self): 
		return FTPCrawler() 

class ProtocolAbstractProduct(object, metaclass=abc.ABCMeta): 
	""" An abstract product, represents protocol to connect """
	
	@abc.abstractmethod 
	def __str__(self): 
		pass
	
class HTTPProtocol(ProtocolAbstractProduct): 
	""" An concrete product, represents http protovol """
	
	def __str__(self): 
		return 'http'

class HTTPSecureProtocol(ProtocolAbstractProduct): 
	""" An concrete product, represents https protovol """
	
	def __str__(self): 
		return 'https'

class FTPProtocol(ProtocolAbstractProduct): 
	""" An concrete product, represents ftp protovol """
	
	def __str__(self): 
		return 'ftp'

class PortAbstractProduct(object, metaclass=abc.ABCMeta): 
	""" An abstract product, represents port to connect """
	
	@abc.abstractmethod 
	def __str__(self): 
		pass

class HTTPPort(PortAbstractProduct): 
	""" A concrete product which represents http port. """
	
	def __str__(self): 
		return '80'

class HTTPSecurePort(PortAbstractProduct): 
	""" A concrete product which represents https port """
	def __str__(self): 
		return '443'

class FTPPort(PortAbstractProduct): 
	""" A concrete products which represents ftp port. """
	
	def __str__(self): 
		return '21'

class CrawlerAbstractProduct(object, metaclass=abc.ABCMeta): 
	""" An Abstract product, represents parser to parse web content """
	
	@abc.abstractmethod 
	def __call__(self, content): 
		pass

class HTTPCrawler(CrawlerAbstractProduct): 
	def __call__(self, content): 
		""" Parses web content """
		
		filenames = [] 
		soup = BeautifulSoup(content, "html.parser") 
		links = soup.table.findAll('a') 

		for link in links: 
			filenames.append(link['href']) 
			
		return '\n'.join(filenames) 

class FTPCrawler(CrawlerAbstractProduct): 
	def __call__(self, content): 
		
		""" Parse Web Content """
		content = str(content, 'utf-8') 
		lines = content.split('\n') 
		filenames = [] 
		
		for line in lines: 
			splitted_line = line.split(None, 8) 
			if len(splitted_line) == 9: 
				filenames.append(splitted_line[-1]) 

		return '\n'.join(filenames) 

class Connector(object): 
	""" A client """
	
	def __init__(self, abstractfactory): 
		""" calling all attributes 
of a connector according to abstractfactory class. """
		
		self.protocol = abstractfactory.create_protocol() 
		self.port = abstractfactory.create_port() 
		self.crawl = abstractfactory.create_crawler() 

	def read(self, host, path): 
		url = str(self.protocol) + '://' + host + ':' + str(self.port) + path 
		print('Connecting to', url) 
		return urllib.request.urlopen(url, timeout=10).read() 

if __name__ == "__main__": 
	con_domain = 'ftp.freebsd.org'
	con_path = '/pub/FreeBSD/'

	con_protocol = input('Choose the protocol \ (0-http, 1-ftp): ') 
	
	if con_protocol == '0': 
		is_secure = input('Use secure connection? (1-yes, 0-no):') 
		if is_secure == '1': 
			is_secure = True
		else: 
			is_secure = False
		abstractfactory = HTTPConcreteFactory(is_secure) 
	else: 
		is_secure = False
		abstractfactory = FTPConcreteFactory(is_secure) 

	connector = Connector(abstractfactory) 

	try: 
		data = connector.read(con_domain, con_path) 
	except urllib.error.URLError as e: 
		print('Cannot access resource with this method', e) 
	else: 
		print(connector.crawl(data)) 
