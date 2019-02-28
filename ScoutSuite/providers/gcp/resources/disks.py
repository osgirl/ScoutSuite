# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.resources import Resources

class Disks(Resources):
    def _parse_resource(self, disk):
        disk_dict = {}
        disk_dict['id'] = self.get_non_provider_id(disk['deviceName'])
        disk_dict['type'] = disk['type']
        disk_dict['mode'] = disk['mode']
        disk_dict['source_url'] = disk['source']
        disk_dict['source_device_name'] = disk['deviceName']
        disk_dict['bootable'] = disk['boot']
        disk_dict['encrypted_with_csek'] = self._is_encrypted_with_csek(disk)
        self[disk_dict['id']] = disk_dict

    def _is_encrypted_with_csek(self, disk):
        return 'diskEncryptionKey' in disk and 'sha256' in disk['diskEncryptionKey'] and disk['diskEncryptionKey']['sha256'] != ''
