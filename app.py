from flask import Flask, request, render_template
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import pytz
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import urllib
import requests
import numpy as np
import matplotlib.pyplot as plt
from string import punctuation

account_sid = 'AC5c0df5a188c9e3d4d0e222fbe9541f32'
auth_token = 'd1f8d9f67e61ab158cda87ce21516958'
client = Client(account_sid, auth_token)

app = Flask(__name__)

#App Route to get body of a text messages, appends to a text file
@app.route("/sms", methods=['GET', 'POST'])
def sms_response_and_send():
    #Keywords to send a personalized message
    keywords = {'suicide':'Hello, you have mentioned the word suicide, if you would like to get some help, please do not hesitate to call the 24/7 hotline dedicated to helping people with serious issues related to suicide. 1-800-273-8255.',\
                'lonely':'Hello, you have mentioned the word lonely, if you would like to talk to someone, please do not hesitate to call the 24/7 hotline with trained volunteers who will listen and talk to you. 1-800-932-4616.',\
                'stress':'Hello, you have mentioned the word stress, if you are looking for a way to destress, a few recommendations are: yoga, meditation, exercise, and unplug. If you would like to discuss other ideas, go to https://www.wecarecommunity.club/breathe.',\
                'burnout':'Hello, you have mentioned the word burnout, if you are looking for a way to destress, a few recommendations are: yoga, meditation, exercise, and unplug. If you would like to discuss other ideas, go to https://www.wecarecommunity.club/breathe.'}
    #Body of the incoming Text Message
    textbody = request.values.get('Body', None)
    #Creating a timestamp for the message
    now = datetime.datetime.now(pytz.timezone('US/Pacific'))
    nowlist = list(str(now))
    nowlist = nowlist[0:nowlist.index('.')]
    #Opens the file that needs to be appended
    openfile = open('messages.txt','a')
    notimefile = open('notimestamp.txt','a')
    #String of time + body + newline
    if textbody != None:
        #Responding with a text message (Generic)
        resp = MessagingResponse()
        #Checking for keywords and sending messages
        for keyword in keywords.keys():
            if keyword in textbody.lower():
                resp.message(keywords[keyword])
        #Writes the text to a file
        openfile.write('['+str(''.join(nowlist))+'] '+str(textbody)+'\n')
        count =+ 1
        #Write to a file without time stamp
        notimefile.write(str(textbody)+'\n')
    #Close the file to save the message
    openfile.close()
    notimefile.close()
    #Statement to return
    statement = "Last Refresh was at "+str(''.join(nowlist))
    #Return a nice message
    return str(resp)

#App Route to print out all text messages when prompted
@app.route("/file", methods=['GET', 'POST'])

def updated_file():
    #Opens the appended file of messages
    notimefile = open('notimestamp.txt','r')
    #Sets message count to 0
    messages = ['test']
    #For each line in the file
    for line in notimefile:
        if line:
            #It forms it into one giant string
            messages = messages.append(line)
    #Close file
    notimefile.close()
    #Return the string
    return render_template('messages.html', my_string="Wheeeee!", my_message_list=messages)
    

if __name__ == "__main__":
    app.run(debug=True)
