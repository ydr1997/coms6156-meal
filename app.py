from flask import Flask, Response, render_template,request
import database_services.RDBService as d_service
from flask_cors import CORS


# from flask_mysqldb import MySQL

import json

import logging

import os

from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from application_services.imdb_artists_resource import IMDBArtistResource
from application_services.UsersResource.user_service import UserResource




tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

#
# app = Flask(__name__)
CORS(app)








@app.route('/trytemplate')
def try_template():
    # data = request.form
    # tasks = {
    #     'ID': data.get('ID'),
    #     'firstName': data.get('firstName'),
    #     'lastName': data.get('lastName'),
    #     'email': data.get('email'),
    #     'addressID': data.get('addressID')
    # }





    #
    # if tasks["ID"] is None or tasks["firstName"] is None or tasks["lastName"] is None or tasks["email"] is None or \
    #         tasks["addressID"] is None:
    #     rsp = Response(json.dumps(None), status=400, content_type="application/json")
    # else:
    #     res = d_service.update_users("UserResource", "User", tasks)
    #     rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
    # return rsp

    return render_template('trytemplate.html',**context)


@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'


@app.route('/imdb/artists/<prefix>')
def get_artists_by_prefix(prefix):
    res = IMDBArtistResource.get_by_name_prefix(prefix)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp


@app.route('/users')
def get_users():
    res = UserResource.get_by_template(None)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


@app.route('/<db_schema>/<table_name>/<column_name>/<prefix>')
def get_by_prefix(db_schema, table_name, column_name, prefix):
    res = d_service.get_by_prefix(db_schema, table_name, column_name, prefix)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/ss/<table_name>/<column_name>/<prefix>')
def getss_by_prefix( table_name, column_name, prefix):
    db_schema = "ec2_lookmeal"
    res = d_service.get_by_prefix(db_schema, table_name, column_name, prefix)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/sss/meals')                          ####show所有的meals
def getsss_by_prefix():
    db_schema = "ec2_lookmeal"
    res = d_service.get_all()
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

# @app.route('/meals/<meals_id>', methods = ["GET"])         #####根据meals_id查找
# def get_meals_fromid(meals_id):
#     res = d_service.get_mealsfromid(meals_id)
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp



@app.route('/meals/delete/<meals_id>', methods = ["GET"])         #####根据meals_id查找
def delete_meals(meals_id):
    res = d_service.meals_delete_id(meals_id)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/meals/add/<id>/<creator>/<location>/<restaurant>/<max_number>/<current_number>', methods = ["POST"])         #####添加meals信息    这里是硬编码
def add_meals(id, creator, location, restaurant, max_number, current_number):
    res = d_service.add_meals(id, creator, location, restaurant, max_number, current_number)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


@app.route('/meals_modificate/add/<meals_id>/<participant>', methods = ["POST"])         #####meals_modification join 一个人choose to join the meal
def meals_modificate1(meals_id, participant):
    res = d_service.meals_modificate_add(meals_id, participant)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


@app.route('/meals_modificate/delete/<meals_id>/<participant>', methods = ["POST"])         #####meals_modification join 一个人choose to join the meal
def meals_modificate2(meals_id, participant):
    res = d_service.meals_modificate_delete(meals_id, participant)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp




@app.route('/make_team', methods=["GET"])
def get_maketeam():
    res = d_service.get_maketeam("ec2_lookmeal", "make_team")
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


@app.route('/meal_information', methods=["GET"])
def get_mealinformation():
    res = d_service.get_mealinformation("ec2_lookmeal", "meal_information")
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


@app.route('/meals/<meals_id>', methods=["GET"])
def get_meals_fromid(meals_id):
    res = d_service.get_mealsfromid("ec2_lookmeal", "meal_information", meals_id)
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




#
# @app.route('/users/email', methods=["POST"])
# def update_email():
#     data = request.form
#     ID = data.get('ID')
#     email = data.get('email')
#     if ID is None:
#         rsp = Response(json.dumps(None), status=422, content_type="application/json")
#     else:
#         res = d_service.update_email("UserResource", "User", ID, email)
#         rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
#     return rsp



# @app.route('/meals/<meals_id>', methods = ["GET"])         #####根据meals_id查找
# def get_meals_fromid(meals_id):
#     res = d_service.get_mealsfromid(meals_id)
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp




@app.route('/smartystreets')                          ####smartystreet api
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
