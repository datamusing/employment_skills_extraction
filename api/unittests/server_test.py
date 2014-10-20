import json
import urllib2
import requests

url = 'http://174.129.34.133:8080/post'
url = 'http://localhost:8080/post'

def main():
    f = open("test_vector.json", "r")
    test_vec = json.load(f)
    f.close()

    for d in test_vec:
        print "\nRequest:\n  %s"%d
        data = json.dumps(d)
        print "data", data
        clen = len(data)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json', 'Content-Length': clen})
        f = urllib2.urlopen(req)
        response = f.read()
        print "\nResponse:\n  %s"%response
        f.close()


if __name__ == '__main__':
    main()

