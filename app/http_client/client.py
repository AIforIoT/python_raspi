import http.client
import logging

ESP_SERVER_PORT = 80

def open_conn(host):
    conn = http.client.HTTPConnection(host, ESP_SERVER_PORT, timeout=2.0)
    return conn

class HTTP_CLIENT:

    def send_GET_request(self, host, action):
        try:
            conn = open_conn(host)
            conn.request("GET", action)
            response = conn.getresponse()
            conn.close()

            response_string = "Conn with Host: "+str(host)+" "+str(response.status)+" "+str(response.reason)
            if response.status is 200:
                logging.info(response_string)
            else:
                logging.error(response_string)
        except Exception as e:
            #print(e)
            logging.error("Impossible to establish connection with host: "+str(host))

