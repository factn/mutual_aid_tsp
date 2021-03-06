from flask import Flask, request, jsonify
import json
import traceback
from models import solve_tsp
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# @app.route('/log_test')
# def log_test():
#     app.logger.info('Testing logger info')
#     app.logger.error('Testing logger error')
#     return 'Test message written to logger'

@app.route('/ping', methods=['GET'])
def ping():
    headers = {'Content-type': 'application/json; charset=utf-8'}
    response = {
        'message': 'ok',
        'time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(response), 200, headers

@app.route('/shortest-route', methods=['GET'])
def get_shortest_route():
    # parse input data
    s_request = request.get_data()
    data = json.loads(s_request)
    fields = ['addresses', 'pickups', 'pickup_dropoff_constraints']
    if not all(key in data for key in fields):
        return 'Data JSON must have the following fields: \n {}'.format(', '.join(fields)), 400
    try:
        # solve the tsp problem
        opt_obj, opt_sol, opt_loc, opt_addr = solve_tsp(data)
        response = {'geolocations': opt_loc, 'optimal_order': opt_sol, 'optimal_objective': opt_obj}
        return jsonify(response), 200
    except Exception as e:
        tb = traceback.format_exc()
        return 'Error solving the TSP model: \n {}\n {}'.format(e, tb), 500


@app.route('/shortest-route-given-geocodes', methods=['POST'])
def get_shortest_route_given_geocodes():
    # parse input data
    s_request = request.get_data()
    data = json.loads(s_request)
    fields = ['addresses', 'pickup_dropoff_constraints']
    if not all(key in data for key in fields):
        return 'Data JSON must have the following fields: \n {}'.format(', '.join(fields)), 400
    try:
        # solve the tsp problem
        opt_obj, opt_sol, opt_loc, opt_addr = solve_tsp(data, given_geocodes=True)
        response ={ 
            'optimal_order': opt_sol, 
            'optimal_objective': opt_obj,
            'optimal_addresses': opt_addr}
        return jsonify(response), 200
    except Exception as e:
        tb = traceback.format_exc()
        return 'Error solving the TSP model: \n {}\n {}'.format(e, tb), 500

if __name__ == '__main__':
    app.run(debug=True)

