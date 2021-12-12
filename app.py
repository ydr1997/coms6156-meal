from flask import Flask, Response, render_template, request, redirect, url_for, session
import database_services.RDBService as d_service
from flask_cors import CORS

import json
import logging
import os

# from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
# from smartystreets_python_sdk.us_street import Lookup
# from flask_dance.contrib.google import make_google_blueprint, google
from middleware import security, notification

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
# app = Flask(__name__, template_folder=tmpl_dir)
app = Flask(__name__, template_folder='template')

# app = Flask(__name__)
CORS(app)

# ----------------------------- Google OAuth2 -----------------------------------

# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
# os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
#
# app.secret_key = "supersekrit"
# blueprint = make_google_blueprint(
#     client_id="314377796932-bcks1e2lbvpi2v6crbb65alcgkpl6l9i.apps.googleusercontent.com",
#     client_secret="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",
#     scope=["profile", "email"]
# )
# app.register_blueprint(blueprint, url_prefix="/login")


# ------------------------------ Middleware ----------------------------------------

# @app.before_request
# def before_request_func():
#     print("running before_request_func")
#     if security.check_security(request):
#         return render_template('auth-err.html')


# @app.after_request
# def after_request_func(response):
#     print("running after_request_func")
#     notification.NotificationMiddlewareHandler.notify(request, response)
#     return response

# -----------------------------------------------------------------------------------

# @app.route('/trytemplate')
# def try_template():
#     # data = request.form
#     # tasks = {
#     #     'ID': data.get('ID'),
#     #     'firstName': data.get('firstName'),
#     #     'lastName': data.get('lastName'),
#     #     'email': data.get('email'),
#     #     'addressID': data.get('addressID')
#     # }
#
#     #
#     # if tasks["ID"] is None or tasks["firstName"] is None or tasks["lastName"] is None or tasks["email"] is None or \
#     #         tasks["addressID"] is None:
#     #     rsp = Response(json.dumps(None), status=400, content_type="application/json")
#     # else:
#     #     res = d_service.update_users("UserResource", "User", tasks)
#     #     rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
#     # return rsp
#
#     return render_template('trytemplate.html', **context)


@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'

#
# @app.route('/sss/meals')  ####show所有的meals
# def getsss_by_prefix():
#     db_schema = "ec2_lookmeal"
#     res = d_service.get_all()
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp


@app.route('/api/meals', methods=["GET"])
def get_meals():
    meal_id = request.args.get('meal_id')       # 127.0.0.1:5000/api/meals?meal_id=1
    res = None

    if not meal_id:
        res = d_service.get_mealinformation("ec2_lookmeal", "meal_information")
    else:
        res = d_service.get_mealsfromid("ec2_lookmeal", "meal_information", meal_id)

    if not res:
        rsp = Response(json.dumps(res, default=str), status=404, content_type="application/json")
    else:
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


# @app.route('/meals/delete/<meals_id>', methods = ["GET"])         #####根据meals_id查找
# def delete_meals(meals_id):
#     res = d_service.meals_delete_id(meals_id)
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp

@app.route('/api/meals/delete', methods=["POST"])         #####根据meals_id查找
def delete_meals():
    if not request.form['id']:
        raise Exception("[add_meals] no meals_id")
    res = d_service.meals_delete_id(request.form['id'])
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


@app.route('/api/meals/add', methods=['POST'])  #####添加meals信息
def add_meals():
    if not request.form['id']:
        raise Exception("[add_meals] no user id")
    if not request.form['name']:
        raise Exception("[add_meals] no creator name")
    if not request.form['addr']:
        raise Exception("[add_meals] no address")
    if not request.form['rest']:
        raise Exception("[add_meals] no rest name")
    if not request.form['max']:
        raise Exception("[add_meals] no max cnt")
    if not request.form['cur']:
        raise Exception("[add_meals] no cur cnt")
    print("meal information retrieved!!")
    res = d_service.add_meals(request.form['id'], request.form['name'],request.form['addr'], request.form['rest'], request.form['max'], request.form['cur'])

    # TODO: error-check the result from query insertion

    rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
    return rsp
    # # print(111)
    # # data = request.form
    # data = request.form
    # print(data)
    # print(data[id])
    # print(data['name'])
    # print(data['addr'])
    #
    # tasks = {
    #     'id': data.get('id'),
    #     'name': data.get('name'),
    #     'addr': data.get('addr'),
    #     'rest': data.get('rest'),
    #     'max': data.get('max'),
    #     'cur': data.get('cur')
    # }
    # print(tasks)
    # if tasks["id"] is None or tasks["name"] is None or tasks["addr"] is None or tasks["rest"] is None or \
    #         tasks["max"] is None or tasks["cur"] is None:
    #     rsp = Response(json.dumps(None), status=400, content_type="application/json")
    # else:
    #     res = d_service.update_users("ec2_lookmeal", "meal_information", tasks)
    #     rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
    # return rsp



# @app.route('/meals/add/<id>/<creator>/<location>/<restaurant>/<max_number>/<current_number>', methods = ["POST"])         #####添加meals信息    这里是硬编码
# def add_meals(id, creator, location, restaurant, max_number, current_number):
#     res = d_service.add_meals(id, creator, location, restaurant, max_number, current_number)
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp
#

# @app.route('/meals_modificate/add/<meals_id>/<participant>', methods = ["POST"])         #####meals_modification join 一个人choose to join the meal
# def meals_modificate1(meals_id, participant):
#     res = d_service.meals_modificate_add(meals_id, participant)
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp


@app.route('/api/meals_modificate/add', methods = ["POST"])         #####meals_modification join 一个人choose to join the meal
def meals_modificate1():
    if not request.form['id']:
        raise Exception("[add_meals] no user id")
    if not request.form['name']:
        raise Exception("[add_meals] no creator name")
    print("make team retrieved!!")
    res = d_service.meals_modificate_add(request.form['id'], request.form['name'])

    rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
    return rsp

# @app.route('/meals_modificate/delete', methods = ["DELETE"])   ###有点问题 先注释掉了
# def meals_modificate2():
#     if not request.form['id']:
#         raise Exception("[add_meals] no user id")
#     if not request.form['name']:
#         raise Exception("[add_meals] no creator name")
#     print("make team retrieved!!")
#     res = d_service.meals_modificate_delete(request.form['id'], request.form['name'])
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp

# @app.route('/meals/delete', methods = ["DELETE"])         #####根据meals_id查找
# def delete_meals():
#     if not request.form['id']:
#         raise Exception("[add_meals] no meals_id")
#     res = d_service.meals_delete_id(request.form['id'])
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp


# @app.route('/meals_modificate/delete/<meals_id>/<participant>', methods = ["POST"])         #####meals_modification join 一个人choose to join the meal
# def meals_modificate2(meals_id, participant):
#     res = d_service.meals_modificate_delete(meals_id, participant)
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp


@app.route('/api/make_team', methods=["GET"])
def get_maketeam():
    res = d_service.get_maketeam("ec2_lookmeal", "make_team")
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

# @app.route('/api/meal_information', methods=["GET"])
# def get_mealinformation():
#     res = d_service.get_mealinformation("ec2_lookmeal", "meal_information")
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp

# @app.route('/meals/<meals_id>', methods = ["GET"])         #####根据meals_id查找
# def get_meals_fromid(meals_id):
#     res = d_service.get_mealsfromid(meals_id)
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp


@app.route('/api/smartystreets')                          ####smartystreet api
def smartystreet():
    auth_id = "1d668e68-7682-f1e6-c470-117ff697e192"
    auth_token = "WBsZrn15pqaJmm2J7qAQ"

    # We recommend storing your secret keys in environment variables instead---it's safer!
    # auth_id = os.environ['SMARTY_AUTH_ID']
    # auth_token = os.environ['SMARTY_AUTH_TOKEN']

    credentials = StaticCredentials(auth_id, auth_token)

    client = ClientBuilder(credentials).build_us_street_api_client()
    # client = ClientBuilder(credentials).with_proxy('localhost:8080', 'user', 'password').build_us_street_api_client()
    # Uncomment the line above to try it with a proxy instead

    # Documentation for input fields can be found at:
    # https://www.smartystreets.com/docs/us-street-api#input-fields

    lookup = Lookup()
    lookup.input_id = "24601"  # Optional ID from your system
    lookup.addressee = "John Doe"
    lookup.street = "1600 Amphitheatre Pkwy"
    lookup.street2 = "closet under the stairs"
    lookup.secondary = "APT 2"
    lookup.urbanization = ""  # Only applies to Puerto Rico addresses
    lookup.city = "Mountain View"
    lookup.state = "CA"
    lookup.zipcode = "94043"
    lookup.candidates = 3
    lookup.match = "Invalid"  # "invalid" is the most permissive match

    try:
        client.send_lookup(lookup)
    except exceptions.SmartyException as err:
        print(err)
        return

    result = lookup.result

    if not result:
        print("No candidates. This means the address is not valid.")
        return

    first_candidate = result[0]

    print("Address is valid. (There is at least one candidate)\n")
    print("Delivery Information")
    print("--------------------")
    print("Delivery line 1: {}".format(first_candidate.delivery_line_1))
    print("Delivery line 2: {}".format(first_candidate.delivery_line_2))
    print("Last line:	    {}".format(first_candidate.last_line))
    print()

    print("Address Components")
    print("-------------------")
    print("Primary number:  {}".format(first_candidate.components.primary_number))
    print("Predirection:	{}".format(first_candidate.components.street_predirection))
    print("Street name:	    {}".format(first_candidate.components.street_name))
    print("Street suffix:   {}".format(first_candidate.components.street_suffix))
    print("Postdirection:   {}".format(first_candidate.components.street_postdirection))
    print("City:			{}".format(first_candidate.components.city_name))
    print("State:		    {}".format(first_candidate.components.state_abbreviation))
    print("ZIP Code:		{}".format(first_candidate.components.zipcode))
    print("County:		    {}".format(first_candidate.metadata.county_name))
    print("Latitude:		{}".format(first_candidate.metadata.latitude))
    print("Longitude:	    {}".format(first_candidate.metadata.longitude))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
