from ruamel import yaml

dockerpath = "/home/pi/ei23-docker/"

ei23 = yaml.load(open(dockerpath+"compose_templates/ei23.yml", 'r'), Loader=yaml.RoundTripLoader)['ei23']
influxdb = yaml.load(open(dockerpath+"compose_templates/influxdb.yml", 'r'), Loader=yaml.RoundTripLoader)['influxdb']
tasmoadmin = yaml.load(open(dockerpath+"compose_templates/tasmoadmin.yml", 'r'), Loader=yaml.RoundTripLoader)['tasmoadmin']
grafana = yaml.load(open(dockerpath+"compose_templates/grafana.yml", 'r'), Loader=yaml.RoundTripLoader)['grafana']

with open(dockerpath+"docker-compose.yml", 'r') as ymlfile:
    docker_config = yaml.load(ymlfile, Loader=yaml.RoundTripLoader)
    # del docker_config['services']['ei23']
    docker_config['services']['ei23'] = ei23
    docker_config['services']['influxdb'] = influxdb
    docker_config['services']['tasmoadmin'] = tasmoadmin
    docker_config['services']['grafana'] = grafana
    # docker_config['services'].insert(len(docker_config['services']), "test", "hi")

    # print(docker_config['services'])
    # for item in docker_config['services']:
    #     print(item)



with open(dockerpath+"docker-compose.yml", 'w') as newconf:
    yaml.dump(docker_config, newconf, Dumper=yaml.RoundTripDumper)