#!/usr/bin/env python3

import socket, httplib2, urllib, json, yaml

with open('Socket_Stellarium_Client_Parameters.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

HOST = data['server_host']
PORT = data['server_port']

http = httplib2.Http()

Stlm = {    "above_horizon":'',
            "altitude":'',
            "altitude_geometric":'',
            "azimuth":'',
            "azimuth_geometric":'',
            "type":'',
            "index":'',
        }

i = 0

#Variables
satellite = 'moon'

def Data_Streamming():
    global i

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    content = http.request("http://%s:%s/api/objects/info?name=%s&format=%s"
        %(data['api_host'], str(data['api_port']), satellite, data['format']), method="GET")[1]
    get_data = content.decode()
    json_st = json.loads(get_data)

    Stlm['above_horizon'] = json_st['above-horizon']
    Stlm['altitude'] = json_st['altitude']
    Stlm['altitude_geometric'] = json_st['altitude-geometric']
    Stlm['azimuth'] = json_st['azimuth']
    Stlm['azimuth_geometric'] = json_st['azimuth-geometric']
    Stlm['type'] = json_st['type']
    Stlm['index'] = i
    st = json.dumps(Stlm)

    client.send(st.encode())
    from_server = client.recv(255)
    client.close()
    print(from_server.decode())

    i = i+1

def Stellarium_Calibration(lat,lon,alt):
    body = {'id':data['id'],
            'latitude': lat,
            'longitude': lon,
            'altitude': alt,
            'name': data['name'],
            'country': data['country'],
            'planet': data['planet']
            }
    url = "http://localhost:8090/api/location/setlocationfields"
    content = http.request(url, method="POST", headers={'Content-type': 'application/x-www-form-urlencoded'},
                       body=urllib.parse.urlencode(body))[1]
    return content

def Stellarium_Status():
    url = "http://localhost:8090/api/main/status"
    content = http.request(url, method="GET")[1]
    return content

try:
    print(Stellarium_Calibration('14.64072', '-90.51327', '1508'))
    print(Stellarium_Status())
    #while True:
        #Data_Streamming()

except KeyboardInterrupt:
    http.close()

except Exception as exception_error:
    print("Error: " + str(exception_error))

finally:
    pass