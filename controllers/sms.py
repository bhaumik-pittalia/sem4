
import urllib # Python URL functions
import urllib2 # Python URL functions
# Prepare you post parameters
values = {
    'authkey' : "279201AURBFWjn3l5cf2082c",
    'mobiles' : "+919426817517",
    'message' : "This is a test message, you can send using application",
    'sender' : "611332",
    'route' : "default"
}
url = "http://api.msg91.com/api/sendhttp.php" # API URL
postdata = urllib.urlencode(values) # URL encoding the data here.
req = urllib2.Request(url, postdata)
response = urllib2.urlopen(req)
output = response.read() # Get Response
print output # Print Response
