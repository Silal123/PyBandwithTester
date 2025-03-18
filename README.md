# Python bandwith tester
This tool is used to test the bandwith inside a network.

## Authors
- [@Silal123](https://www.github.com/Sial123)

## Installation

How to install this tester.

#### Clone the git repository to both machines you want to use
```bash
git clone https://github.com/Silal123/PyBandwithTester.git
```

#### 1. Start the Server
To start the server to wich the data is sent you need to run this command:
```bash
python tester.py server --port PORT --host HOST
```
> port and host are optional

#### 2. Connect the client
Now to start the test you need to run the client mode on your other machine
```bash 
python tester.py client --server-ip SERVERIP --port PORT --size SIZE
```
> port and size are optional
> server-ip is required. Its the ip of the machine on wich the server is running
