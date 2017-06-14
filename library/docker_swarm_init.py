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
module: docker_swarm_init
short_description:
    - A module for initialize a new Swarm using the current connected engine as the first node.
description:
    - A module for initialize a new Swarm using the current connected engine as the first node.
author: unitymind

options:
  advertise_addr:
    description:
      - Externally reachable address advertised to other nodes. This can either be an address/port combination in the form 192.168.1.1:4567, or an interface followed by a port number, like eth0:4567. If the port number is omitted, the port number from the listen address is used. If advertise_addr is not specified, it will be automatically detected when possible.
    required: false
    default: null
  listen_addr:
    description:
      - Listen address used for inter-manager communication, as well as determining the networking interface used for the VXLAN Tunnel Endpoint (VTEP). This can either be an address/port combination in the form 192.168.1.1:4567, or an interface followed by a port number, like eth0:4567. If the port number is omitted, the default swarm listening port is used.
    required: false
    default: '0.0.0.0:2377'
  force_new_cluster:
    description: Force creating a new Swarm, even if already part of one.
    required: false
    default: false
  

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
  docker_swarm_init:

- name: Force leave node from a cluster
  docker_swarm_init:
    force: True
"""


from ansible.module_utils.docker_common import AnsibleDockerClient, DockerBaseClass
from docker.errors import DockerException


class SwarmInitManager(DockerBaseClass):

    def __init__(self, client, results):

        super(SwarmInitManager, self).__init__()

        self.client = client
        self.results = results
        self.check_mode = self.client.check_mode
        parameters = self.client.module.params

        self.advertise_addr = parameters.get("advertise_addr", None)
        self.listen_addr = parameters.get("listen_addr")
        self.force_new_cluster = parameters.get("force_new_cluster")

        self.execute()

    def execute(self):
        try:
            self.results['changed'] = self.client.init_swarm(
                self.advertise_addr, self.listen_addr, self.force_new_cluster
            )
        except DockerException as e:
            self.fail(str(e))

    def fail(self, msg):
        self.client.fail(msg)


def main():
    argument_spec = dict(
        advertise_addr=dict(type='str', required=False),
        listen_addr=dict(type='str', required=False, default='0.0.0.0:2377'),
        force_new_cluster=dict(type='bool', required=False, default=False)
    )

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=False
    )

    results = dict(
        changed=False
    )

    SwarmInitManager(client, results)
    client.module.exit_json(**results)

if __name__ == '__main__':
    main()
