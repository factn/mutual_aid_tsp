# TSP with pickup and dropoff constraints

This app demonstrates the solution to the TSP problem with pickup and delivery constrains. 

## Deployment

To deploy on Heroku:

```bash
heroku login
heroku create your-deployment
git push heroku master
```

`resilience-tsp.herokuapp.com` is a deployed heroku app in the mutualaidworld team, and used for production. You can create your own deployment or just run locally `python app.py` (after installing requirements.txt into a virtualenv)

Sample request:
```bash
curl --location --request GET 'https://resilience-tsp.herokuapp.com/shortest-route' \
--header 'Content-Type: text/plain' \
--data-raw '{
    "addresses": {
      "0": "Antwerp+Belgium",
      "1": "Bruges+Belgium",
      "2": "C-Mine+Belgium",
      "3": "Dinant+Belgium",
      "4": "Ghent+Belgium",
      "5": "Grand+Place+Brussels+Belgium",
      "6": "Hasselt+Belgium",
      "7": "Leuven+Belgium",
      "8": "Mechelen+Belgium",
      "9": "Mons+Belgium",
      "10": "Montagne+de+Bueren+Belgium",
      "11": "Namur+Belgium",
      "12": "Remouchamps+Belgium",
      "13": "Waterloo+Belgium"
    },
    "pickups": [
      "0",
      "12"
    ],
    "pickup_dropoff_constraints": {
      "0": [
        "1",
        "4",
        "5",
        "13",
        "9",
        "8"
      ],
      "12": [
        "2",
        "3",
        "6",
        "7",
        "10",
        "11"
      ]
    }
  }'
```

Sample response
```JSON
{
  "geolocations": [
    {
      "latitude": 51.2211097,
      "longitude": 4.3997081
    },
    {
      "latitude": 51.0281381,
      "longitude": 4.4803453
    },
    {
      "latitude": 50.84671435,
      "longitude": 4.352514119250888
    },
    {
      "latitude": 50.7153727,
      "longitude": 4.396367
    },
    {
      "latitude": 50.4794772,
      "longitude": 5.7126031
    },
    {
      "latitude": 50.6479624,
      "longitude": 5.5775543
    },
    {
      "latitude": 50.98303985,
      "longitude": 5.490050468085652
    },
    {
      "latitude": 50.9303735,
      "longitude": 5.3378043
    },
    {
      "latitude": 50.879202,
      "longitude": 4.7011675
    },
    {
      "latitude": 50.4665284,
      "longitude": 4.8661892
    },
    {
      "latitude": 50.2591576,
      "longitude": 4.9130624
    },
    {
      "latitude": 50.4549568,
      "longitude": 3.951958
    },
    {
      "latitude": 51.2085526,
      "longitude": 3.226772
    },
    {
      "latitude": 51.0538286,
      "longitude": 3.7250121
    }
  ],
  "optimal_objective": 374.36452417964296,
  "optimal_order": [
    0,
    8,
    5,
    13,
    12,
    10,
    2,
    6,
    7,
    11,
    3,
    9,
    1,
    4
  ]
}
```

Check out the [node_client_demo](node_client_demo) directory for an example of how to access this end point using node/javascript.

Note that the geolocations have been sorted in the optimal order output by the  routing model.

## Model and data

This app implements a modified version of the TSP problem as described [here](https://python-mip.readthedocs.io/en/latest/examples.html#the-traveling-salesman-problem).
Data needed in the request payload are:

- addresses: a dictionary of indices and addresses
- pickups: a list of pickup node indices
- pickup_dropoff_constraints: pickup and dropoff requirements. The keys are pickup indices and the values are dropoff indices

In addition, a "distance_matrix" field can be included in the payload (for testing purpose). If not provided, either Google Distance Matrix API or OpenStreetMap API is used to calculate the distance matrix. In particular, if the environment variable `GOOGLE_DISTANCE_MATRIX_API_KEY` is setup is deployment, Google Distance Matrix API will be used. Otherwise, OpenStreetMap API will be used.

Note that the modified TSP formulation has extra constraints of the form `y_i >= y_j + 1` for each pickup node i and the corresponding dropoff nodes j. These constraints are to ensure that pickup nodes are visited before dropoff nodes.

__Example__

For the dataset as provided in the above TSP example, assume that we add some extra data:

- Pickup nodes: Antwerp and Remouchamps
- Dropoff nodes: remaining nodes
- Pickup/dropoff constraints:
    - Antwerp: [Bruges, Ghent, Grand-Place de Bruxelles, Mechelen, Mons, Waterloo]
    - Remouchamps: [C-Mine, Dinant, Hasselt, Leuven, Montagne de Bueren, Namur]

The optimal route in this case is:

```
Antwerp -> Mechelen -> Grand-Place de Bruxelles -> Waterloo -> Remouchamps -> Montagne de Bueren -> C-Mine -> Hasselt -> Leuven -> Namur -> Dinant -> Mons -> Bruges -> Ghent
-> Antwerp
```

![](./images/sample_opt_sol.png?raw=true)

For comparison, the original optimal route without pickup/dropoff constraints was:

```
Antwerp -> Bruges -> Ghent -> Grand-Place de Bruxelles -> Waterloo -> Mons -> Namur -> Dinant -> Remouchamps -> Montagne de Bueren -> C-Mine -> Hasselt -> Leuven -> Mechelen -> Antwerp
```

![](./images/original_opt_sol.png?raw=true)

We can see the new optimal route now respects the pickup/dropoff constraints that we introduced.



