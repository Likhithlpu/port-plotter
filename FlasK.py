from flask import Flask, render_template, request
from tabulate import tabulate
import socket

app = Flask(__name__)

def check_port(target, port, kill=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((target, port))
        if kill:
            sock.shutdown(socket.SHUT_RDWR)
        return [port, 'Open', 'Killed' if kill else '']
    except socket.error:
        return [port, 'Closed or Unreachable', '']
    finally:
        sock.close()

def scan_ports(target, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        result = check_port(target, port)
        open_ports.append(result)
    return open_ports

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target_host = request.form['target_host']
        option = request.form['option']

        if option == 'S':
            start_port = int(request.form['start_port'])
            end_port = int(request.form['end_port'])

            results = scan_ports(target_host, start_port, end_port)

            if results:
                return render_template('results.html', target_host=target_host, result_table=results)
            else:
                return render_template('results.html', target_host=target_host, message="No open ports found.")
        
        elif option == 'C':
            target_port = int(request.form['target_port'])
            kill_option = request.form['kill_option']

            if kill_option == 'K':
                result = check_port(target_host, target_port, kill=True)
            else:
                result = check_port(target_host, target_port)

            return render_template('results.html', target_host=target_host, result=result)

        else:
            return render_template('results.html', message="Invalid option. Please enter 'S' or 'C'.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
