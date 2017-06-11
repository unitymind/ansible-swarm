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
module: docker_swarm_leave
short_description:
    - A module for leaving node from a cluster.
description:
    - A module for leaving node from a cluster.
author: unitymind

options:
  force:
    description:
      - Leave the swarm even if this node is a manager.
    required: False
    default: False
    
extends_documentation_fragment:
    - docker
requirements:
    - "python >= 2.7"
    - "docker >= 2.3.0"
    - "Docker API >= 1.24"
"""

EXAMPLES = """
- name: Leave node from a cluster
  docker_swarm_leave:
  
- name: Force leave node from a cluster
  docker_swarm_leave:
    force: True
"""


from ansible.module_utils.docker_common import AnsibleDockerClient, DockerBaseClass


class SwarmLeaveManager(DockerBaseClass):

    def __init__(self, client, results):

        super(SwarmLeaveManager, self).__init__()

        self.client = client
        self.results = results
        self.check_mode = self.client.check_mode
        parameters = self.client.module.params

        self.force = parameters.get("force")

        self.execute()

    def execute(self):
        try:
            if self.client.swarm.leave(self.force):
                self.results['changed'] = True
        except Exception as e:
            self.fail(e.message)

    def fail(self, msg):
        self.client.fail(msg)


def main():
    argument_spec = dict(
        force=dict(type='bool', default=False)
    )

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=False
    )

    results = dict(
        changed=False
    )

    SwarmLeaveManager(client, results)
    client.module.exit_json(**results)

if __name__ == '__main__':
    main()
