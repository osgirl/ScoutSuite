# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.resources import Resources

class Networks(Resources):
    def __init__(self, gce_facade, project_id):
        self.gce_facade = gce_facade
        self.project_id = project_id

    def fetch_all(self, *kwargs):
        resources = self.gce_facade.get_networks(self.project_id)
        for resource in resources:
            self._parse_resource(resource)

    def _parse_resource(self, network):
        network_dict = {}
        network_dict['id'] = network['id']
        network_dict['project_id'] = network['selfLink'].split('/')[-4]
        network_dict['name'] = network['name']
        network_dict['description'] = network['description'] if 'description' in network and network['description'] else 'N/A'
        network_dict['creation_timestamp'] = network['creationTimestamp']
        network_dict['network_url'] = network['selfLink']
        network_dict['subnetwork_urls'] = network.get('subnetworks', None)
        network_dict['auto_subnet'] = network.get('autoCreateSubnetworks',  None)
        network_dict['routing_config'] = network['routingConfig']
        self[network_dict['id']] = network_dict