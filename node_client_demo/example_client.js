
const _ = require('lodash')
const axios = require("axios");

async function tsp_shortest_route() {

    /// test of the case where it has to do geolookup 

    const url = "https://resilience-tsp.herokuapp.com/shortest-route";  

    var source_data =
    {
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
    }

    console.log("-------------------------------------")
    console.log("request " + url)
    console.log(source_data);
  
    const response = await axios({
      method: 'GET',
      url: url,
      data: source_data
    });

    console.log("--------response----------")
    console.log(response.data);
    return response.data;

}


async function tsp_shortest_route_geocodes() {

    // test of the case where we supply the geocodes

    const url = "https://resilience-tsp.herokuapp.com/shortest-route-given-geocodes";
    //const url = "http://localhost:5000/shortest-route-given-geocodes";    

    var req_data =
    {
       "addresses": {
           "0": {
                "address": "0 1012 W Ventura Blvd, Camarillo, CA 93010",
                "lat": 34.2212685,
                "lng": -119.1070667
           },
           "1": {
                "address": "1 Some street address, CA 93010",
                "lat": 35.22185,
                "lng": -119.12
           },
           "2": {
                "address": "2 1012 W Ventura Blvd, Camarillo, CA 93010",
                "lat": 34.2212685,
                "lng": -119.1070667
           },
           "3": {
                "address": "3 Some other address, CA 93010",
                "lat": 35.12,
                "lng": -118.20
           }
        },
        "pickups": 
        [
        ],
        "pickup_dropoff_constraints": {
            //if we enable these constraints it gives an error !!
            "0": [
                "1"
            ],
            "2": [
                "3"
            ]
        }
    }

    console.log("-------------------------------------")
    console.log("request " + url)
    console.log(req_data);
    const response = await axios({
      method: 'POST',
      url: url,
      data: req_data
    });

    console.log("--------response----------")
    console.log(response.data);
    return response.data;

}



async function tsp_shortest_route_compare() {

    /// comparable case to above but 
    //  this time we supplu the same data as above...

    const url = "https://resilience-tsp.herokuapp.com/shortest-route-given-geocodes";    
    //const url = "http://localhost:5000/shortest-route-given-geocodes";    
   
    var source_data_explicit =
    {
        "addresses": {
            "0": {  "address": "Antwerp+Belgium", 
                    "lat": 51.2211097, "lng": 4.3997081 },
            "1": {  "address": "Bruges+Belgium", 
                    "lat": 51.0281381, "lng": 4.4803453 },
            "2": {  "address": "C-Mine+Belgium", 
                    "lat": 50.84671435, "lng": 4.352514119250888},
            "3": {  "address": "Dinant+Belgium", 
                    "lat": 50.7153727, "lng": 4.396367 },
            "4": {  "address": "Ghent+Belgium", 
                    "lat": 50.4794772, "lng": 5.7126031 },
            "5": {  "address": "Grand+Place+Brussels+Belgium", 
                    "lat": 50.6479624, "lng": 5.5775543 },
            "6": {  "address": "Hasselt+Belgium", 
                    "lat": 50.98303985, "lng": 5.490050468085652 },
            "7": {  "address": "Leuven+Belgium", 
                    "lat": 50.9303735, "lng": 5.3378043 },
            "8": {  "address": "Mechelen+Belgium", 
                    "lat": 50.879202, "lng": 4.7011675 },
            "9": {  "address": "Mons+Belgium", 
                    "lat": 50.4665284, "lng": 4.8661892 },
            "10": { "address": "Montagne+de+Bueren+Belgium", 
                    "lat": 50.2591576, "lng": 4.9130624 },
            "11": { "address": "Namur+Belgium", 
                    "lat": 50.4549568, "lng": 3.951958 },
            "12": { "address": "Remouchamps+Belgium", 
                    "lat": 51.2085526, "lng": 3.226772 },
            "13": { "address": "Waterloo+Belgium", 
                    "lat": 51.0538286, "lng": 3.7250121 }
        },
        "pickups": [
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
    }

    console.log("-------------------------------------")
    console.log("request " + url)
    console.log(source_data_explicit)
    const response = await axios({
      method: 'POST',
      url: url,
      data: source_data_explicit
    });    

    console.log("--------response----------")
    console.log(response.data);
    return response.data;
}


// MAIN

(async () => {
    
    try {
        await tsp_shortest_route_geocodes();
        //await tsp_shortest_route();
        //await tsp_shortest_route_compare();
        
    } catch (err) {
        console.error(err);
    }

})();


