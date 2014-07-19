import sqlite3
import urllib2
from hashlib import sha1
import json
import ConfigParser
from configobj import ConfigObj
import os,sys
import time

wd = os.path.dirname(os.path.abspath(__file__))
os.chdir(wd)
sys.path.insert(1, wd)

def trakt_notif_downloaded():
	cfgfile                  = "python_trakt.ini"
	cfg                      = ConfigObj(cfgfile)
	dronedbfile              = cfg["nzbdrone"]["dbfile"]

	api      = cfg["trakt"]["api"]
	username = cfg["trakt"]["username"]
	password = sha1(cfg["trakt"]["password"]).hexdigest()
	method   = "show/episode/library/"
	method  += "%API%"

	method = method.replace("%API%", api)

	db = sqlite3.connect(dronedbfile)
	cur = db.cursor()
	cmd = "select Series.Tvdbid, Series.Title, Series.Year, Episodes.SeasonNumber, Episodes.EpisodeNumber, History.id "+\
						"from History, Series, Episodes "+\
						"where History.SeriesId = Series.Id and History.EpisodeId = Episodes.id and History.EventType=3 "+\
						"		 and History.Id>"+str(cfg["config"]["last_check"])+" "+\
						"order by History.Date"
	cur.execute(cmd)
	for episode in cur.fetchall():
		print("{0} S{1}E{2}".format(episode[1],episode[3],episode[4]))
		data = {
							'tvdb_id': episode[0],
							'title': episode[1],
							'year': episode[2],
							'episodes': [ {
										'season': episode[3],
										'episode': episode[4]
										} ]
							}
		data["username"] = username
		data["password"] = password
		encoded_data = json.dumps(data)
		url = "http://api.trakt.tv/" + method
		try:
			stream = urllib2.urlopen(url, encoded_data)

			resp = stream.read()
			resp = json.loads(resp)
			if ("error" in resp):
				raise Exception(resp["error"])

			if (resp["status"] == "success"):
				print "Succeeded calling method. Result: " + resp["message"]
				cfg["config"]["last_check"] = episode[5]
			else:
				print "Failed calling method"

		except urllib2.HTTPError as e:
			print url
			print e.code
			print e.reason

	cfg.write()
	cfg.clear()

if __name__ == "__main__":
	while True:
		print "Starting trakt"
		trakt_notif_downloaded()
		print "End trakt"
		time.sleep(300)

