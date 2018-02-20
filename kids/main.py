from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
#import apiai
import pandas as pd
import json
import os

from flask import Flask
from flask import request
from flask import make_response
app = Flask(__name__)
@app.route('/kids', methods=['POST'])
def kids():
    req = request.get_json(silent=True, force=True)
    speech = "this gets ignored..."
    parameters = req.get("result").get("parameters")
    current_answer = req.get("result").get("action")
    current_question = req.get("result").get("contexts")[0].get("parameters").get("current-question")
    #case = req.get("result").get("contexts")[0].get("parameters").get("case")
    print('Q-' + current_question,'A-' + current_answer)

    kids_csv_file =pd.read_csv('D:\kids.csv')
    if (kids_csv_file.Questions[0] == current_question and kids_csv_file.answers[0] == current_answer):
        next_question = kids_csv_file.Questions[1]
        print('in age')
        bot_reply = {
            "followupEvent": {
                "name": next_question,
                "data": {
                    # Naresh 10.Jan.2018 - added current_question also to the answer..
                    # since the current question is also added to the answer we will be able to get the right questions.
                    "user-ans": current_question + "." + current_answer
                    # "user-ans": current_answer
                }
            }
        }

    elif kids_csv_file.Questions[0] == current_question and current_answer=='no':
        speech ="Sorry you cannot ride as you need to be atleast 8 yrs"
        bot_reply = {
            "speech": speech,
            "displayText": speech,
            # "data": data,
            # "contextOut": [],
            "source": "VA webhook"
            }
    else:
        print(0)
    if (kids_csv_file.Questions[1] == current_question and kids_csv_file.answers[1] == current_answer):
        next_question = kids_csv_file.Questions[2]
        print('in height')
        bot_reply = {
            "followupEvent": {
                "name": next_question,
                "data": {
                    # Naresh 10.Jan.2018 - added current_question also to the answer..
                    # since the current question is also added to the answer we will be able to get the right questions.
                    "user-ans": current_question + "." + current_answer
                    # "user-ans": current_answer
                }
            }
        }

    elif kids_csv_file.Questions[1] == current_question and current_answer=='no':
        speech = "Sorry you cannot ride as you need to be atleast 45 inches"
        bot_reply = {
            "speech": speech,
            "displayText": speech,
            # "data": data,
            # "contextOut": [],
            "source": "VA webhook"
        }
    else:
        print(1)
    if (kids_csv_file.Questions[2] == current_question and kids_csv_file.answers[2] == current_answer):
        speech = 'Enjoy the ride'
        bot_reply = {
            "speech": speech,
            "displayText": speech,
            # "data": data,
            # "contextOut": [],
            "source": "VA webhook"
        }
    elif kids_csv_file.Questions[2] == current_question and current_answer=='no':
        speech = "Sorry you cannot ride as you need to be atleast 45 pounds"
        bot_reply = {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "VA webhook"
        }
    else:
        print(2)





#naresh 1/6/2018
    #res = json.dumps(bot_reply, indent=4)
    res = json.dumps(bot_reply, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')

