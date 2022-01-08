import json
import re
from http import client
from bs4 import BeautifulSoup

URL = 'wiki.multitheftauto.com'

def getClientFunctionsPageHTML():
    global URL
    CLIENT_SIDE_FUNCTIONS = '/wiki/Client_Scripting_Functions'

    conn = client.HTTPSConnection(URL)
    conn.request('GET', CLIENT_SIDE_FUNCTIONS)

    response = conn.getresponse()
    status = response.status
    reason = response.reason
    body = response.read()

    if not status == 200:
        raise Exception(status, reason, body)
    else:
        return body

def getServerFunctionsPageHTML():
    global URL
    SERVER_SIDE_FUNCTIONS = '/wiki/Server_Scripting_Functions'
    conn = client.HTTPSConnection(URL)
    conn.request('GET', SERVER_SIDE_FUNCTIONS)

    response = conn.getresponse()
    status = response.status
    reason = response.reason
    body = response.read()

    if not status == 200:
        raise Exception(status, reason, body)
    else:
        return body

def isFunction(a):
    """
    Check if the link looks like a function link.
    """

    try:
        fnName = a.string
        return fnName and \
            fnName[0] == fnName[0].lower() and \
            re.search("^\/wiki", a['href']) != None and \
            re.search("^(\w+)$", a['title'], re.ASCII)
    except KeyError:
        return False

def getListOfFunctions(data):
    soup = BeautifulSoup(data, 'html.parser')
    links = list(filter(isFunction, soup.find_all('a')))

    results = []

    for link in links:
        results.append({
            'title': link['title'],
            'url': link['href'],
            'name': link.string
        })

    return results

if __name__ == '__main__':
    clientFunctionsPage = getClientFunctionsPageHTML()
    serverFunctionsPage = getServerFunctionsPageHTML()
    f = open('client.json', 'w')
    f.write(json.dumps(getListOfFunctions(clientFunctionsPage)))
    f.close()

    f = open('server.json', 'w')
    f.write(json.dumps(getListOfFunctions(serverFunctionsPage)))
    f.close()

