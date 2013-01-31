import urllib2 as url
import urllib
import httplib as http

#I tried to use threading, unsuccessfully
import thread as thr


#This simply cuts the extra characters to isolate the ID
def fmtId( string ):
    return string[1:len( string ) - 1]


#Talk to people
def talk(id,req):

    #Show the server that we're typing
    typing = url.urlopen('http://omegle.com/typing', '&id='+id)
    typing.close()

    #Show the user that we can write now
    msg = str(raw_input('> '))

    #Send the string to the stranger ID
    msgReq = url.urlopen('http://omegle.com/send', '&msg='+msg+'&id='+id)

    #Close the connection
    msgReq.close()


#This is where all the magic happens, we listen constantly to the page for events
def listenServer( id, req ):
    while True:

        site = url.urlopen(req)

        #We read the HTTP output to get what's going on
        rec = site.read()

        if 'waiting' in rec:
            print("Waiting...")

        elif 'connected' in rec:
            print('Found one')
            print(id)
            #Since this isn't threaded yet, it executes the talk function (yeah, turn by turn)
            talk(id,req)
            
        elif 'strangerDisconnected' in rec:
            print('He is gone')
            #We start the whole process again
            omegleConnect()
            
        elif 'typing' in rec:
            print("He's typing something...")

        #When we receive a message, print it and execute the talk function            
        elif 'gotMessage' in rec:
            print(rec[16:len( rec ) - 2])
            talk(id,req)


#Here we listen to the start page to acquire the ID, then we "clean" the string to isolate the ID
def omegleConnect():
    site = url.urlopen('http://omegle.com/start','')
    id = fmtId( site.read() )
    print(id)
    req = url.Request('http://omegle.com/events', urllib.urlencode( {'id':id}))
    print('Gotta find one')

    #Then we open our ears to the wonders of the events page, where we know if anything happens
    #We have to pass two arguments: the ID and the events page.
    listenServer(id,req)


# I just didn't use the __init__ method    
omegleConnect()
