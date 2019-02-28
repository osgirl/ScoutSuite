# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.resources import Resources

class Snapshots(Resources):
    def __init__(self, gce_facade, project_id):
        self.gce_facade = gce_facade
        self.project_id = project_id

    def fetch_all(self, *kwargs):
        resources = self.gce_facade.get_snapshots(self.project_id)
        for resource in resources:
            self._parse_resource(resource)

    def _parse_resource(self, snapshot):
        snapshot_dict = {}
        snapshot_dict['id'] = snapshot['id']
        snapshot_dict['name'] = snapshot['name']
        snapshot_dict['description'] = snapshot['description'] if 'description' in snapshot and snapshot['description'] else 'N/A'
        snapshot_dict['creation_timestamp'] = snapshot['creationTimestamp']
        snapshot_dict['status'] = snapshot['status']
        snapshot_dict['source_disk_id'] = snapshot['sourceDiskId']
        snapshot_dict['source_disk_url'] = snapshot['sourceDisk']
        self[snapshot_dict['id']] = snapshot_dict