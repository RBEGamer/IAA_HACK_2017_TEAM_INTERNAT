
import urllib.request

msg =  "something"
with urllib.request.urlopen("http://iaahakers.mybluemix.net/main?query="+msg) as res:
   res.read().decode("utf-8")
