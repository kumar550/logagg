from basescript import BaseScript
from collect.collector import LogCollector
from forward.forwarder import LogForwarder

class LogaggCommand(BaseScript):
    DESC = 'Logagg command line tool'

    def collect(self):
        collector = LogCollector(
                        self.log,
                        self.args,
                        self.args.file,
                        self.args.nsqtopic,
                        self.args.nsqchannel,
                        self.args.nsqd_http_address,
                        self.args.depth_limit_at_nsq,
                        self.args.exception_logs_file)
        collector.start()

    def forward(self):
        forwarder = LogForwarder(self.log,self.args,self.args.nsqtopic,\
                        self.args.nsqchannel,self.args.nsqd_tcp_address,\
                        self.args.mongodb_server_url,self.args.mongodb_port,\
                        self.args.mongodb_user_name,self.args.mongodb_password,\
                        self.args.mongodb_database,self.args.mongodb_collection,\
                        self.args.influxdb_server_url,self.args.influxdb_port,\
                        self.args.influxdb_user_name,self.args.influxdb_password,\
                        self.args.influxdb_database)
        forwarder.start()

    def define_subcommands(self, subcommands):
        super(LogaggCommand, self).define_subcommands(subcommands)

        collect_cmd = subcommands.add_parser('collect',
            help='Collects the logs from different processes and sends to nsq')
        collect_cmd.set_defaults(func=self.collect)
        collect_cmd.add_argument('file', nargs='+',
            help='Provide absolute path of logfile including module name and function name, '
                    'eg: /var/log/nginx/access.log:logagg.collect.handlers.nginx_access')
        collect_cmd.add_argument('nsqtopic', help='Topic name to publish messages. Ex: logs_and_metrics')
        collect_cmd.add_argument('--nsqchannel', help='Channel of nsqd')
        collect_cmd.add_argument('--nsqd-http-address',
            default='localhost:4151', help='nsqd http address where we send the messages')
        collect_cmd.add_argument('--depth-limit-at-nsq', type=int, default=10000000,
            help='To limit the depth at nsq channel')
        collect_cmd.add_argument('--exception-logs-file',
                default='/var/log/logagg/exception_logs.log', help='If collector fails to publish messages to nsq, will write the logs to a file')

        forward_cmd = subcommands.add_parser('forward', help='Collects all the messages from nsq and pushes to storage engine')
        forward_cmd.set_defaults(func=self.forward)
        forward_cmd.add_argument('--nsqtopic', help='NSQ topic name to read messages from. Ex: logs_and_metrics')
        forward_cmd.add_argument('--nsqchannel', help='channel of nsqd')
        forward_cmd.add_argument('--nsqd-tcp-address',
            default='localhost:4150', help='nsqd tcp address where we get the messages')

        forward_cmd.add_argument('--mongodb-server-url', help='DNS of the server where mongo is running')
        forward_cmd.add_argument('--mongodb-port', help='port where mongo is running')
        forward_cmd.add_argument('--mongodb-user-name', help='username of mongodb')
        forward_cmd.add_argument('--mongodb-password', help='password to authenticate mongodb')
        forward_cmd.add_argument('--mongodb-database', help='database to store logs')
        forward_cmd.add_argument('--mongodb-collection', help='collection to store logs')

        forward_cmd.add_argument('--influxdb-server-url', help='DNS of the server where influxdb is running')
        forward_cmd.add_argument('--influxdb-port', help='port where influxdb is running')
        forward_cmd.add_argument('--influxdb-user-name', help='username of influxdb')
        forward_cmd.add_argument('--influxdb-password', help='password to authenticate influxdb')
        forward_cmd.add_argument('--influxdb-database', help='database to store metrics')

def main():
    LogaggCommand().start()

if __name__ == '__main__':
    main()
