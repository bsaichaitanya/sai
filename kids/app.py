from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
# import apiai
import pandas as pd
import json
import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)
questions_dict = {};
questions_array=[];
errors_array=[];


@app.route('/kids', methods=['POST'])
def kids():
    req = request.get_json(silent=True, force=True)
    speech = "this gets ignored..."
    parameters = req.get("result").get("parameters")
    current_answer = req.get("result").get("action")
    current_question = req.get("result").get("contexts")[0].get("parameters").get("current-question")
    # case = req.get("result").get("contexts")[0].get("parameters").get("case")
    print('Q-' + current_question, 'A-' + current_answer)

    kids_csv_file = pd.read_csv('D:\kidswitherror.csv')
    if (len(questions_dict) == 0):
        for i in range(len(kids_csv_file.Questions)):
             questions_dict[kids_csv_file.Questions[i]] = kids_csv_file.answers[i];
             questions_array.append(kids_csv_file.Questions[i]);
             errors_array.append(kids_csv_file.errors[i]);
    print(questions_dict);

    if (questions_dict[current_question] == current_answer):
        if (len(questions_dict) > questions_array.index(current_question) + 1):
                next_question_index = questions_array.index(current_question) + 1;
                next_question = questions_array[next_question_index];

                print(current_question);
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

        else:
            speech = 'Enjoy the ride'
            bot_reply = {
                "speech": speech,
                "displayText": speech,
                # "data": data,
                # "contextOut": [],
                "source": "VA webhook"
            }
            print('Enjoy Ride');
    else:
        indexcurrent=questions_array.index(current_question);
        speech =errors_array[indexcurrent];
        bot_reply = {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "VA webhook"
        }


# naresh 1/6/2018
# res = json.dumps(bot_reply, indent=4)
    res = json.dumps(bot_reply, indent=4)
# print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
	

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')

