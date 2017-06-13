#!/usr/bin/env python
# Copyright 2017, Cleawing, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DOCUMENTATION = """
---
module: docker_swarm_join
short_description:
    - A module for join a swarm that has already been created.
description:
    - A module for join a swarm that has already been created.
author: unitymind

options:
  remote_addrs:
    description:
      - Addresses of one or more manager nodes already participating in the Swarm to join.
    required: true
  join_token:
    description:
      - Secret token for joining this Swarm.
    required: true
  listen_addr:
    description:
      - Listen address used for inter-manager communication if the node gets promoted to manager, as well as determining the networking interface used for the VXLAN Tunnel Endpoint (VTEP).
    required: false
    default: "0.0.0.0:2377"
  advertise_addr:
    description:
      - Externally reachable address advertised to other nodes. This can either be an address/port combination in the form 192.168.1.1:4567, or an interface followed by a port number, like eth0:4567. If the port number is omitted, the port number from the listen address is used. If AdvertiseAddr is not specified, it will be automatically detected when possible.
    required: false
    default: null

extends_documentation_fragment:
    - docker
requirements:
    - "python >= 2.7"
    - "docker >= 2.3.0"
    - "Docker API >= 1.24"
"""
# FIXME
EXAMPLES = """
- name: Leave node from a cluster
  docker_swarm_join:

- name: Force leave node from a cluster
  docker_swarm_leave:
    force: True
"""


from ansible.module_utils.docker_common import AnsibleDockerClient, DockerBaseClass
from docker.errors import DockerException


class SwarmJoinManager(DockerBaseClass):

    def __init__(self, client, results):

        super(SwarmJoinManager, self).__init__()

        self.client = client
        self.results = results
        self.check_mode = self.client.check_mode
        parameters = self.client.module.params

        self.role = parameters.get("role")
        self.remote_addrs = parameters.get("remote_addrs")
        self.join_token = parameters.get("join_token")
        self.listen_addr = parameters.get("listen_addr")
        self.advertise_addr = parameters.get("advertise_addr")

        self.execute()

    def execute(self):
        try:
            self.results['changed'] = self.client.join_swarm(self.remote_addrs, self.join_token, self.listen_addr, self.advertise_addr)
        except DockerException as e:
            self.fail(str(e))

    def fail(self, msg):
        self.client.fail(msg)


def main():
    argument_spec = dict(
        remote_addrs=dict(type='list'),
        join_token=dict(type='str'),
        listen_addr=dict(type='str', default='0.0.0.0:2377'),
        advertise_addr=dict(type='str', default=None)
    )

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=False
    )

    results = dict(
        changed=False
    )

    SwarmJoinManager(client, results)
    client.module.exit_json(**results)

if __name__ == '__main__':
    main()
