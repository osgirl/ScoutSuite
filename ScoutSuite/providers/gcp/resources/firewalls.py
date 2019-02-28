# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.resources import Resources

class Firewalls(Resources):
    def __init__(self, gce_facade, project_id):
        self.gce_facade = gce_facade
        self.project_id = project_id

    def fetch_all(self, *kwargs):
        resources = self.gce_facade.get_firewalls(self.project_id)
        for resource in resources:
            self._parse_resource(resource)

    def _parse_resource(self, firewall):
        firewall_dict = {}
        firewall_dict['id'] = firewall['id']
        firewall_dict['project_id'] = firewall['selfLink'].split('/')[-4]
        firewall_dict['name'] = firewall['name']
        firewall_dict['description'] = firewall['description'] if \
            'description' in firewall and firewall['description'] else 'N/A'
        firewall_dict['creation_timestamp'] = firewall['creationTimestamp']
        firewall_dict['network'] = firewall['network'].split('/')[-1]
        firewall_dict['network_url'] = firewall['network']
        firewall_dict['priority'] = firewall['priority']
        firewall_dict['source_ranges'] = firewall['sourceRanges'] if 'sourceRanges' in firewall else []
        firewall_dict['source_tags'] = firewall['sourceTags'] if 'sourceTags' in firewall else []
        firewall_dict['target_tags'] = firewall['targetTags'] if 'targetTags' in firewall else []
        firewall_dict['direction'] = firewall['direction']
        firewall_dict['disabled'] = firewall['disabled']

        # Parse FW rules
        for direction in ['allowed', 'denied']:
            direction_string = '%s_traffic' % direction
            firewall_dict[direction_string] = {
                'tcp': [],
                'udp': [],
                'icmp': []
            }
            if direction in firewall:
                firewall_dict['action'] = direction
                for rule in firewall[direction]:
                    if rule['IPProtocol'] not in firewall_dict[direction_string]:
                        firewall_dict[direction_string][rule['IPProtocol']] = ['*']
                    else:
                        if rule['IPProtocol'] == 'all':
                            for protocol in firewall_dict[direction_string]:
                                firewall_dict[direction_string][protocol] = ['0-65535']
                            break
                        else:
                            if firewall_dict[direction_string][rule['IPProtocol']] != ['0-65535']:
                                if 'ports' in rule:
                                    firewall_dict[direction_string][rule['IPProtocol']] += rule['ports']
                                else:
                                    firewall_dict[direction_string][rule['IPProtocol']] = ['0-65535']

        self.firewalls[firewall_dict['id']] = firewall_dict
