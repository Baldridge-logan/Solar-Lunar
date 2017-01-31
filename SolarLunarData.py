import datetime
import urllib2

BODIES = {
	"Sun": 10,
	"Moon": 11
}

URL_PREFIX = "http://aa.usno.navy.mil"
ENDPOINT_SUFFIX = "/cgi-bin/aa_altazw.pl?form=1&body=%s&year=%s&month=%s&day=%s&intv_mag=%s&state=%s&place=%s"

class CelestialData:
	def __init__(self, location):
		self._location = location.split(", ")
		self._interval = 1 #seconds

	def get_date(self):
		return str(datetime.date.today()).split('-')

	def generate_endpoint(self):
		date = self.get_date()
		endpoint = ENDPOINT_SUFFIX % \
			(
				self._body_num,
				date[0], date[1], date[2],
				self._interval, 
				self._location[1], self._location[0]
			)
		return endpoint

	def parse_line(self, line):
		cols = (line.strip()).split()
		if len(cols) >= 2:
			time = cols[0].split(':')
			return float(time[0])*60 + float(time[1]), float(cols[1]), float(cols[2])
		else:
			return False
			
	def fetch_data(self, body, time_interval):
		self._body_num = BODIES[body]
		self._interval = time_interval

		url = URL_PREFIX + self.generate_endpoint()
		content = urllib2.urlopen(url)

		data = {
			"time_stamps": [], 
			"altitude": [], 
			"azimuth": []
		}

		record = False
		for line in content:
			if "</pre>" in line: #end of data
				record = False
			if record:
				parse = line #parse_parse
				if parse:
					ts = parse[0:5]
					data["time_stamps"].append(ts.replace(" ",""))
					al = parse[10:16]
					data["altitude"].append(al.replace(" ",""))
					az = parse[22:28]
					data["azimuth"].append(az.replace(" ",""))
			if "h  m         o           o" in line: #start of data
				record = True
		content.close()

		return data

	
