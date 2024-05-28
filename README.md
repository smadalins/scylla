## Setup

1. Clone the repository
2. Install the required packages by running `pip install -r requirements.txt`
3. Deploy a single node scyulla cluster using the following instructions [link](https://hub.docker.com/r/scylladb/scylla/)
4. Check IP address of the scylla cluster by running `docker exec -it some-scylla nodetool status`

## Running the application
`python stress.py --ip <scylla_ip> --thread <number_of_threads> -d <duration list>` - run the application with the specified parameters
`python stress.py --help` - help information

### Example
`python stress.py --ip 172.17.0.2 -d 10 15 5 10 10 -t 5` 

## Checking repository
run `tox`
