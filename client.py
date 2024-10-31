import argparse
import socket
import struct

def create_packet(version, header_length, service_type, payload):
    # TODO: Implement packet creation based on parameters
    # TODO: use the python struct module to create a fixed length header
    # TODO: Fixed length header -> Version (1 byte), Header Length (1 byte), Service Type (1 byte), Payload Length (2 bytes)
    # TODO: payload -> variable length
    # TODO: depending on the service type, handle encoding of the different types of payload.
    # TODO: service_type 1 = payload is int, service_type 2 = payload is float, service_type 3 = payload is string

    # Encode the payload based on service type
    if service_type == 1:
        encoded_payload = struct.pack('!i', int(payload))
    elif service_type == 2:
        encoded_payload = struct.pack('!f', float(payload))
    elif service_type == 3:
        encoded_payload = payload.encode('utf-8')
    else:
        raise ValueError("Invalid service type")

    payload_length = len(encoded_payload)
    
    # Create the header
    header = struct.pack('!BBBH', version, header_length, service_type, payload_length)
    
    # Combine header and payload
    return header + encoded_payload

def handle_response(response):
    try:
        header, payload = response.split('\n', 1)
        print("Received from server:")
        print(header)
        print(payload)
    except ValueError:
        print("Unexpected response format from server:", response)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Client for packet creation and sending.")
    parser.add_argument('--version', type=int, required=True, help='Packet version')
    parser.add_argument('--header_length', type=int, required=True, help='Length of the packet header')
    parser.add_argument('--service_type', type=int, required=True, help='Service type of the payload (1 for int, 2 for float, 3 for string)')
    parser.add_argument('--payload', type=str, required=True, help='Payload to be packed into the packet')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=12345, help='Server port')

    args = parser.parse_args()

    try:
        packet = create_packet(args.version, args.header_length, args.service_type, args.payload)

        print(f"Attempting to connect to {args.host}:{args.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((args.host, args.port))
            print(f"Connected to {args.host}:{args.port}")
            s.sendall(packet)
            print("Packet sent successfully")

            response = s.recv(1024).decode('utf-8')
            handle_response(response)
    except ConnectionRefusedError:
        print(f"Error: Unable to connect to the server at {args.host}:{args.port}. Make sure the server is running and the address is correct.")
    except Exception as e:
        print(f"An error occurred: {e}")