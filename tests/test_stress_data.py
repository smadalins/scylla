# flake8: noqa
STRESS_OUTPUT = """
******************** Stress Settings ********************
Command:
  Type: write
  Count: -1
  Duration: 15 SECONDS
  No Warmup: false
  Consistency Level: LOCAL_ONE
  Serial Consistency Level: SERIAL
  Target Uncertainty: not applicable
  Key Size (bytes): 10
  Counter Increment Distibution: add=fixed(1)
Rate:
  Auto: false
  Thread Count: 10
  OpsPer Sec: 0
Population:
  Sequence: 1..1000000
  Order: ARBITRARY
  Wrap: true
Insert:
  Revisits: Uniform:  min=1,max=1000000
  Visits: Fixed:  key=1
  Row Population Ratio: Ratio: divisor=1.000000;delegate=Fixed:  key=1
  Batch Type: not batching
Columns:
  Max Columns Per Key: 5
  Column Names: [C0, C1, C2, C3, C4]
  Comparator: AsciiType
  Timestamp: null
  Variable Column Count: false
  Slice: false
  Size Distribution: Fixed:  key=34
  Count Distribution: Fixed:  key=5
Errors:
  Ignore: false
  Tries: 10
Log:
  No Summary: false
  No Settings: false
  File: null
  Interval Millis: 1000
  Level: NORMAL
Mode:
  API: JAVA_DRIVER_NATIVE
  Connection Style: CQL_PREPARED
  CQL Version: CQL3
  Protocol Version: V4
  Username: null
  Password: null
  Auth Provide Class: null
  Max Pending Per Connection: null
  Connections Per Host: 8
  Compression: NONE
Node:
  Nodes: [172.17.0.2]
  Is White List: false
  Datacenter: null
  Rack: null
Schema:
  Keyspace: keyspace1
  Replication Strategy: org.apache.cassandra.locator.SimpleStrategy
  Replication Strategy Options: {replication_factor=1}
  Table Compression: null
  Table Compaction Strategy: null
  Table Compaction Strategy Options: {}
Transport:
  factory=org.apache.cassandra.thrift.TFramedTransportFactory; truststore=null; truststore-password=null; keystore=null; keystore-password=null; ssl-protocol=TLS; ssl-alg=SunX509; store-type=JKS; ssl-ciphers=TLS_RSA_WITH_AES_128_CBC_SHA,TLS_RSA_WITH_AES_256_CBC_SHA;
Port:
  Native Port: 9042
  Thrift Port: 9160
  JMX Port: 7199
Send To Daemon:
  *not set*
Graph:
  File: null
  Revision: unknown
  Title: null
  Operation: WRITE
TokenRange:
  Wrap: false
  Split Factor: 1
CloudConf:
  File: null

===== Using optimized driver!!! =====
Connected to cluster: , max pending requests per connection null, max connections per host 8
Datatacenter: datacenter1; Host: /172.17.0.2; Rack: rack1
Created keyspaces. Sleeping 1s for propagation.
Sleeping 2s...
Warming up WRITE with 50000 iterations...
Running WRITE with 10 threads 15 seconds
type       total ops,    op/s,    pk/s,   row/s,    mean,     med,     .95,     .99,    .999,     max,   time,   stderr, errors,  gc: #,  max ms,  sum ms,  sdv ms,      mb
total,          3672,    3672,    3672,    3672,     0.4,     0.3,     1.0,     2.4,     4.7,     5.2,    1.0,  0.00000,      0,      0,       0,       0,       0,       0
total,         26580,   22908,   22908,   22908,     0.4,     0.4,     0.7,     1.1,     5.1,    13.5,    2.0,  0.51315,      0,      0,       0,       0,       0,       0
total,         49589,   23009,   23009,   23009,     0.4,     0.4,     0.7,     1.0,     4.5,     9.2,    3.0,  0.31808,      0,      0,       0,       0,       0,       0
total,         72812,   23223,   23223,   23223,     0.4,     0.4,     0.7,     0.9,     3.4,    17.8,    4.0,  0.23095,      0,      0,       0,       0,       0,       0
total,         96481,   23669,   23669,   23669,     0.4,     0.4,     0.6,     0.9,     3.4,     4.1,    5.0,  0.18137,      0,      0,       0,       0,       0,       0
total,        122125,   25644,   25644,   25644,     0.4,     0.3,     0.6,     0.8,     2.2,    23.8,    6.0,  0.15133,      0,      0,       0,       0,       0,       0
total,        154722,   32597,   32597,   32597,     0.3,     0.3,     0.5,     0.6,     2.9,     9.7,    7.0,  0.13984,      0,      0,       0,       0,       0,       0
total,        187737,   33015,   33015,   33015,     0.3,     0.3,     0.5,     0.6,     3.9,     6.6,    8.0,  0.12713,      0,      0,       0,       0,       0,       0
total,        195572,    7835,    7835,    7835,     1.3,     1.9,     2.1,     2.2,     4.0,     4.2,    9.0,  0.14362,      0,      0,       0,       0,       0,       0
total,        213724,   18152,   18152,   18152,     0.5,     0.3,     2.0,     2.1,     4.0,     6.9,   10.0,  0.13248,      0,      0,       0,       0,       0,       0
total,        251040,   37316,   37316,   37316,     0.3,     0.2,     0.4,     0.5,     3.0,    10.2,   11.0,  0.12797,      0,      0,       0,       0,       0,       0
total,        299515,   48475,   48475,   48475,     0.2,     0.2,     0.3,     0.4,     2.0,    11.5,   12.0,  0.13506,      0,      0,       0,       0,       0,       0
total,        346435,   46920,   46920,   46920,     0.2,     0.2,     0.3,     0.4,     2.9,    10.0,   13.0,  0.13165,      0,      0,       0,       0,       0,       0
total,        395870,   49435,   49435,   49435,     0.2,     0.2,     0.3,     0.4,     0.8,     3.6,   14.0,  0.12760,      0,      0,       0,       0,       0,       0
total,        444813,   48943,   48943,   48943,     0.2,     0.2,     0.3,     0.4,     1.1,     2.2,   15.0,  0.12191,      0,      0,       0,       0,       0,       0
total,        485906,   49007,   49007,   49007,     0.2,     0.2,     0.3,     0.4,     1.9,     4.5,   15.8,  0.11611,      0,      0,       0,       0,       0,       0


Results:
Op rate                   :   30,679 op/s  [WRITE: 30,679 op/s]
Partition rate            :   30,679 pk/s  [WRITE: 30,679 pk/s]
Row rate                  :   30,679 row/s [WRITE: 30,679 row/s]
Latency mean              :    0.3 ms [WRITE: 0.3 ms]
Latency median            :    0.2 ms [WRITE: 0.2 ms]
Latency 95th percentile   :    0.6 ms [WRITE: 0.6 ms]
Latency 99th percentile   :    2.0 ms [WRITE: 2.0 ms]
Latency 99.9th percentile :    3.1 ms [WRITE: 3.1 ms]
Latency max               :   23.8 ms [WRITE: 23.8 ms]
Total partitions          :    485,906 [WRITE: 485,906]
Total errors              :          0 [WRITE: 0]
Total GC count            : 0
Total GC memory           : 0.000 KiB
Total GC time             :    0.0 seconds
Avg GC time               :    NaN ms
StdDev GC time            :    0.0 ms
Total operation time      : 00:00:15

END
"""
