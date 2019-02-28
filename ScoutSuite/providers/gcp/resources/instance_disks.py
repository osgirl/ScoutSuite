# -*- coding: utf-8 -*-

from ScoutSuite.providers.gcp.resources.disks import Disks

class InstanceDisks(Disks):
    def __init__(self, instance):
        super()
        self.instance = instance

    def fetch_all(self, *kwargs):
        resources = self.instance['disks'] if 'disks' in self.instance else {}
        for resource in resources:
            self._parse_resource(resource)
