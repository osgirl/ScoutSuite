# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.resources import Resources

class Subnetworks(Resources):
    def __init__(self, gce_facade, project_id, region):
        self.gce_facade = gce_facade
        self.project_id = project_id
        self.region = region

    def fetch_all(self, *kwargs):
        resources = self.gce_facade.get_subnetworks(self.project_id, self.region)
        for resource in resources:
            self._parse_resource(resource)

    def _parse_resource(self, subnetwork):
        subnetwork_dict = {}
        subnetwork_dict['id'] = subnetwork['id']
        subnetwork_dict['project_id'] = subnetwork['selfLink'].split('/')[-5]
        subnetwork_dict['region'] = subnetwork['region'].split('/')[-1]
        subnetwork_dict['region'] = subnetwork['region'].split('/')[-1]
        subnetwork_dict['name'] = "%s-%s" % (subnetwork['name'], subnetwork_dict['region'])
        subnetwork_dict['subnetwork'] = subnetwork['network'].split('/')[-1]
        subnetwork_dict['gateway_address'] = subnetwork['gatewayAddress']
        subnetwork_dict['ip_range'] = subnetwork['ipCidrRange']
        subnetwork_dict['creation_timestamp'] = subnetwork['creationTimestamp']
        subnetwork_dict['private_ip_google_access'] = subnetwork['privateIpGoogleAccess']
        self[subnetwork_dict['id']] = subnetwork_dict