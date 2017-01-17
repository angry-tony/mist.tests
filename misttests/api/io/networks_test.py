from itertools import chain
import requests
import misttests.api.helpers
from misttests.api.core.conftest import owner_api_token

create_network_params = {
    'ec2': {'network': {'name': 'ec2apitestnet',
                        'description': 'api-test-net',
                        'cidr': '10.1.0.0/16'}},

    'gce': {'network': {'name': 'gceapitestnet',
                        'description': 'api-test-net',
                        'mode': 'custom'}},

    'openstack': {'network': {'name': 'openstackapitestnet',
                              'description': 'api-test-net',
                              'admin_state_up': True}}
}
create_subnet_params = {
    'ec2': {'name': 'ec2apitestsubnet',
            'cidr': '10.1.1.0/24',
            'description': 'api-test-subnet',
            'availability_zone': 'ap-northeast-1a'
            },

    'gce': {'name': 'gceapitestsubnet',
            'cidr': '10.1.1.0/24',
            'description': 'api-test-subnet',
            'region': 'us-west1'},

    'openstack': {'name': 'openstackapitestsubnet',
                  'cidr': '10.1.1.0/24',
                  'description': 'api-test-subnet',
                  'enable_dhcp': True,
                  'gateway_ip': '10.1.1.1',
                  'allocation_pools': [{'start':'10.1.1.2',
                                        'end':'10.1.1.100'}]
                  }
}

network_listing_dict = {
    'ec2': {'cidr': '10.1.0.0/16',
            'instance_tenancy': 'default'},

    'gce': {'mode': 'custom',
            'cidr': None},

    'openstack': {'admin_state_up': True}
}

subnet_listing_dict = {
    'ec2': {'cidr': '10.1.1.0/24',
            'availability_zone': 'ap-northeast-1a'},

    'gce': {'region': 'us-west1',
            'cidr': '10.1.1.0/24'},

    'openstack': {'cidr': '10.1.1.0/24',
                  'enable_dhcp': True,
                  'gateway_ip': '10.1.1.1',
                  'allocation_pools': [{'start': '10.1.1.2',
                                        'end': '10.1.1.100'}],
                  'ip_version': 4
                  }
    }


def assert_dict_contains(superset_dict, subset_dict):
    
    for key, val in subset_dict.iteritems():
        assert superset_dict.get(key) == val,\
            'Value for key %s differs: %s != %s' % (key, val, 
                                                    superset_dict.get(key))


def test_001_create_network(pretty_print, mist_io, owner_api_token,
                            network_test_cloud, network_test_cleanup):
    provider =  network_test_cloud.ctl.provider
    # Creating a network
    response = mist_io.create_network(cloud_id=network_test_cloud.id,
                                      network_params=create_network_params[provider],
                                      api_token=owner_api_token).post()
    # Testing the API response
    print 'Response: code:{0}, body:{1}'.format(response.status_code,
                                                response.text)
    assert response.status_code == requests.codes.ok

    response_content = response.json()
    misttests.api.helpers.assert_is_instance(response_content, dict)

    assert response_content['name'] == \
           create_network_params[provider]['network'][
               'name']
    assert response_content['description'] == 'api-test-net'


def test_002_create_subnet(pretty_print, mist_io, owner_api_token,
                           network_test_cloud, network_test_cleanup):
    provider =  network_test_cloud.ctl.provider
    # Creating a network
    network_response = mist_io.create_network(cloud_id=network_test_cloud.id,
                                              network_params=
                                              create_network_params[provider],
                                              api_token=owner_api_token).post()
    assert network_response.status_code == requests.codes.ok

    # Creating a subnet
    response = mist_io.create_subnet(cloud_id=network_test_cloud.id,
                                     subnet_params=create_subnet_params[provider],
                                     network_id=network_response.json()['id'],
                                     api_token=owner_api_token).post()

    # Testing the API response
    print 'Response: code:{0}, body:{1}'.format(response.status_code,
                                                response.text)
    assert response.status_code == requests.codes.ok

    response_content = response.json()
    misttests.api.helpers.assert_is_instance(response_content, dict)

    assert response_content['name'] == create_subnet_params[provider]['name']
    assert response_content['description'] == 'api-test-subnet'
    

def test_003_list_networks(pretty_print, mist_io, owner_api_token,
                           network_test_cloud, network_test_cleanup):
    
    provider =  network_test_cloud.ctl.provider
    # Getting a network listing
    response = mist_io.list_networks(cloud_id=network_test_cloud.id,
                                     api_token=owner_api_token).get()
    print 'Response: code:{0}, body:{1}'.format(response.status_code,
                                                response.text)
    assert response.status_code == requests.codes.ok

    # Verifying that the API response has the correct structure
    response_content = response.json()
    misttests.api.helpers.assert_is_instance(response_content, dict)
    for base_key in ['public', 'private', 'routers']:
        assert base_key in response_content

    network_dict_required_keys = ['name', 'id', 'network_id', 'cloud']

    for network in chain(response_content['public'],
                         response_content['private']):
        for required_key in network_dict_required_keys:
            assert network.get(required_key)
        assert 'description' in network
        misttests.api.helpers.assert_is_instance(network['subnets'], list)

        # Specifically test the network we just created for provider-specific
        # values
        if network['description'] == 'api-test-net':
            assert_dict_contains(network, network_listing_dict[provider])



def test_004_list_subnets(pretty_print, mist_io, owner_api_token,
                          network_test_cloud, network_test_cleanup):
    provider =  network_test_cloud.ctl.provider
    # Creating a network
    network_response = mist_io.create_network(cloud_id=network_test_cloud.id,
                                              network_params=
                                              create_network_params[
                                                 provider],
                                              api_token=owner_api_token).post()
    assert network_response.status_code == requests.codes.ok

    # Creating a subnet
    subnet_response = mist_io.create_subnet(cloud_id=network_test_cloud.id,
                                            subnet_params=create_subnet_params[
                                               provider],
                                            network_id=network_response.json()[
                                                'id'],
                                            api_token=owner_api_token).post()

    assert subnet_response.status_code == requests.codes.ok

    # Getting a subnet listing
    subnet_listing = mist_io.list_subnets(cloud_id=network_test_cloud.id,
                                          api_token=owner_api_token,
                                          network_id=network_response.json()[
                                              'id']).get()

    print 'Response: code:{0}, body:{1}'.format(subnet_listing.status_code,
                                                subnet_listing.text)
    assert subnet_listing.status_code == requests.codes.ok

    # Verifying that the API response has the correct structure
    subnets = subnet_listing.json()
    misttests.api.helpers.assert_is_instance(subnets, list)
    misttests.api.helpers.assert_equal(len(subnets), 1)

    subnet_dict_required_keys = ['name', 'id', 'subnet_id', 'cloud', 'cidr',
                                 'network']

    for subnet in subnets:
        for required_key in subnet_dict_required_keys:
            assert subnet.get(required_key)
        assert 'description' in subnet
        # Specifically test the subnet we just created for provider-specific
        # values
        assert_dict_contains(subnet, subnet_listing_dict[provider])


def test_005_delete_network(pretty_print, mist_io, owner_api_token,
                            network_test_cloud, network_test_cleanup):
    provider =  network_test_cloud.ctl.provider
    # Creating a network
    network_response = mist_io.create_network(cloud_id=network_test_cloud.id,
                                              network_params=
                                              create_network_params[
                                                 provider],
                                              api_token=owner_api_token).post()
    assert network_response.status_code == requests.codes.ok

    network_db_id = network_response.json()['id']

    # Deleting the network and testing the response
    delete_response = mist_io.delete_network(cloud_id=network_test_cloud.id,
                                             network_id=network_db_id,
                                             api_token=owner_api_token).delete()
    print 'Response: code:{0}, body:{1}'.format(delete_response.status_code,
                                                delete_response.text)
    assert delete_response.status_code == requests.codes.ok

    # Getting a network listing
    network_listing_response = mist_io.list_networks(
        cloud_id=network_test_cloud.id,
        api_token=owner_api_token).get()
    assert network_listing_response.status_code == requests.codes.ok

    # Verifying that the deleted network is no longer present in the listing
    networks = network_listing_response.json()
    api_network_ids = [network['id'] for network in
                       chain(networks['public'], networks['private'])]
    assert network_db_id not in api_network_ids


def test_006_delete_subnet(pretty_print, mist_io, owner_api_token,
                           network_test_cloud, network_test_cleanup):
    provider =  network_test_cloud.ctl.provider
    # Creating a network
    network_response = mist_io.create_network(cloud_id=network_test_cloud.id,
                                              network_params=
                                              create_network_params[
                                                 provider],
                                              api_token=owner_api_token).post()
    assert network_response.status_code == requests.codes.ok

    network_db_id = network_response.json()['id']

    # Creating a subnet
    subnet_response = mist_io.create_subnet(cloud_id=network_test_cloud.id,
                                            subnet_params=create_subnet_params[
                                               provider],
                                            network_id=network_response.json()[
                                                'id'],
                                            api_token=owner_api_token).post()

    assert subnet_response.status_code == requests.codes.ok

    subnet_db_id = subnet_response.json()['id']

    # Deleting the subnet and testing the response
    delete_response = mist_io.delete_subnet(cloud_id=network_test_cloud.id,
                                            network_id=network_db_id,
                                            subnet_id=subnet_response.json()[
                                                'id'],
                                            api_token=owner_api_token).delete()
    print 'Response: code:{0}, body:{1}'.format(delete_response.status_code,
                                                delete_response.text)
    assert delete_response.status_code == requests.codes.ok

    # Getting a subnet listing
    subnet_listing_response = mist_io.list_subnets(
        cloud_id=network_test_cloud.id,
        api_token=owner_api_token,
        network_id=network_response.json()['id']).get()
    assert subnet_listing_response.status_code == requests.codes.ok

    # Verifying that the deleted subnet is no longer present in the listing
    subnets = subnet_listing_response.json()
    api_subnet_ids = [subnet['id'] for subnet in subnets]
    assert subnet_db_id not in api_subnet_ids