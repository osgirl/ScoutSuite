
class GCEFacade:
    def __init__(self, gce_client):
        self.gce_client = gce_client

    def get_disks(self, project_id, zone):
        return self.gce_client.disks().list(project=project_id, zone=zone).execute()

    def get_firewalls(self, project_id):
        return self.gce_client.firewalls().list(project=project_id).execute()

    def get_instances(self, project_id, zone):
        return self.gce_client.instances().list(project=project_id, zone=zone).execute()

    def get_networks(self, project_id):
        return self.gce_client.networks().list(project=project_id).execute()

    def get_project(self, project_id):
        return self.gce_client.projects().get(project=project_id).execute()

    def get_snapshots(self, project_id):
        return self.gce_client.snapshots().list(project=project_id).execute()

    def get_subnetworks(self, project_id, region):
        return self.gce_client.subnetworks().list(project=project_id, region=region).execute()
