from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import pytz

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
    #String of time + body + newline
    if textbody != None:
        #Responding with a text message (Generic)
        resp = MessagingResponse()
        #
        for keyword in keywords.keys():
            if keyword in textbody.lower():
                resp.message(keywords[keyword])
        #
        openfile.write('['+str(''.join(nowlist))+'] '+str(textbody)+'\n')
        count =+ 1
    #Close the file to save the message
    openfile.close()
    #Statement to return
    statement = "Last Refresh was at "+str(''.join(nowlist))
    #Return a nice message
    return str(resp)

#App Route to print out all text messages when prompted
@app.route("/file", methods=['GET', 'POST'])
def updated_file():
    #Opens the appended file of messages
    openfile = open('messages.txt','r')
    #Sets message count to 0
    allmessages = ''
    #For each line in the file
    for line in openfile:
        #It forms it into one giant string
        allmessages = allmessages + line
    #Close file
    openfile.close()
    #Return the string
    return allmessages
    

if __name__ == "__main__":
    app.run(debug=True)
