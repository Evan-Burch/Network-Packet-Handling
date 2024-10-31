import socket
import struct

def unpack_packet(conn, header_format):
    # TODO: Implement header unpacking based on received bytes
    # TODO: Create a string from the header fields
    # return the string - this will be the payload

    # Receive the header
    header_data = conn.recv(struct.calcsize(header_format))
    if not header_data:
        return None

    # Unpack the header
    version, header_length, service_type, payload_length = struct.unpack(header_format, header_data)

    # Receive the payload
    payload_data = conn.recv(payload_length)

    # Decode the payload based on service type
    if service_type == 1:  # Integer
        payload = struct.unpack('!i', payload_data)[0]
    elif service_type == 2:  # Float
        payload = struct.unpack('!f', payload_data)[0]
    elif service_type == 3:  # String
        payload = payload_data.decode('utf-8')
    else:
        payload = f"Unknown service type: {service_type}"

    # Create a string from the header fields and payload
    packet_header_as_string = f"Version: {version}, Header Length: {header_length}, Service Type: {service_type}, Payload Length: {payload_length}"
    return packet_header_as_string, payload

def create_response(header_string, payload):
    return f"{header_string}\nPayload: {payload}"

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 12345
    # Fixed length header -> Version (1 byte), Header Length (1 byte), Service Type (1 byte), Payload Length (2 bytes)
    # TODO: Specify the header format using "struct"
    header_format = '!BBBH'  # ! for network byte order, B for unsigned char (1 byte), H for unsigned short (2 bytes)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            s.listen()
            print(f"Server listening on {host}:{port}")
            print(f"Local IP: {socket.gethostbyname(socket.gethostname())}")
            
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by: {addr}")
                    while True:
                        try:
                            # TODO: Receive and unpack packet using the unpack_packet function

                            # Receive and unpack packet
                            result = unpack_packet(conn, header_format)
                            if result is None:
                                print("Client disconnected")
                                break
                            
                            header_string, payload = result
                            print(f"Received: {header_string}")
                            print(f"Payload: {payload}")

                            #TODO: create header
                            #TODO: add payload
                            #TODO: send to client

                            # Create and send response
                            response = create_response(header_string, payload)
                            conn.sendall(response.encode('utf-8'))
                        except Exception as e:
                            print(f"Error: {e}")
                            break
                    print("Connection closed")
        except Exception as e:
            print(f"Error starting the server: {e}")