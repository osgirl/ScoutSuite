# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.gcp.resources.instance_disks import InstanceDisks

class Instances(Resources):
    def __init__(self, gce_facade, project_id, zone):
        self.gce_facade = gce_facade
        self.project_id = project_id
        self.zone = zone

    def fetch_all(self, *kwargs):
        resources = self.gce_facade.get_instances(self.project_id, self.zone)
        for resource in resources:
            self._parse_resource(resource)
  
    def _parse_resource(self, instance):
        instance_dict = {}
        instance_dict['id'] = self.get_non_provider_id(instance['name'])
        instance_dict['project_id'] = self.project_id
        instance_dict['name'] = instance['name']
        instance_dict['description'] = instance['description'] if 'description' in instance and instance['description'] else 'N/A'
        instance_dict['creation_timestamp'] = instance['creationTimestamp']
        instance_dict['zone'] = instance['zone'].split('/')[-1]
        instance_dict['tags'] = instance['tags']
        instance_dict['status'] = instance['status']
        instance_dict['zone_url_'] = instance['zone']
        instance_dict['network_interfaces'] = instance['networkInterfaces']
        instance_dict['service_accounts'] = instance['serviceAccounts']
        instance_dict['deletion_protection_enabled'] = instance['deletionProtection']
        instance_dict['block_project_ssh_keys_enabled'] = self._is_block_project_ssh_keys_enabled(instance)
        instance_dict['oslogin_enabled'] = self._is_oslogin_enabled(instance)
        instance_dict['ip_forwarding_enabled'] = instance['canIpForward']
        instance_dict['serial_port_enabled'] = self._is_serial_port_enabled(instance)
        instance_dict['has_full_access_cloud_apis'] = self._has_full_access_to_all_cloud_apis(instance)
        instance_dict['disks'] = InstanceDisks(instance)
        self[instance_dict['id']] = instance_dict

    def _is_encrypted_with_csek(self, disk):
        return 'diskEncryptionKey' in disk and 'sha256' in disk['diskEncryptionKey'] and disk['diskEncryptionKey']['sha256'] != ''

    def _is_block_project_ssh_keys_enabled(self, instance):
        metadata = self._metadata_to_dict(instance['metadata'])
        return metadata.get('block-project-ssh-keys') == 'true'

    def _metadata_to_dict(self, metadata):
        return dict((item['key'], item['value']) for item in metadata['items']) if 'items' in metadata else {}

    def _get_common_instance_metadata_dict(self):
        project = self.gce_facade.get_project(self.project_id)
        return self._metadata_to_dict(project['commonInstanceMetadata'])

    def _is_oslogin_enabled(self, instance):
        instance_metadata = self._metadata_to_dict(instance['metadata'])
        if instance_metadata.get('enable-oslogin') == 'FALSE':
            return False
        elif instance_metadata.get('enable-oslogin') == 'TRUE':
            return True
        project_metadata = self._get_common_instance_metadata_dict()
        return project_metadata.get('enable-oslogin') == 'TRUE'

    def _is_serial_port_enabled(self, instance):
        metadata = self._metadata_to_dict(instance['metadata'])
        return metadata.get('serial-port-enable') == 'true'

    def _has_full_access_to_all_cloud_apis(self, instance):
        full_access_scope = 'https://www.googleapis.com/auth/cloud-platform'
        return any(full_access_scope in service_account['scopes'] for service_account in instance['serviceAccounts'])

