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
module: docker_facts
short_description:
    - A module for injecting Docker info as facts.
description:
    - A module for injecting Docker info as facts.
author: nextrevision, unitymind
"""

EXAMPLES = """
- name: load docker facts
  docker_facts:
"""


from ansible.module_utils.docker_common import AnsibleDockerClient, DockerBaseClass
from docker.errors import DockerException


class InfoManager(DockerBaseClass):

    def __init__(self, client, results):

        super(InfoManager, self).__init__()

        self.client = client
        self.results = results
        self.check_mode = self.client.check_mode
        self.info = self.client.info
        self.swarm = self.client.inspect_swarm

        self.execute()

    def execute(self):
        # collect common info
        try:
            info = self.info()
            self.results['changed'] = True
            if not self.check_mode:
                self.results['ansible_facts'] = {'docker': {'info': info}}
            else:
                self.results['docker'] = {'info': info}
        except DockerException as e:
            self.fail(str(e))

        # collect swarm inspect (if node is part of swarm and has manager role)
        try:
            swarm_info = self.swarm()
            if not self.check_mode:
                self.results['ansible_facts']['docker']['swarm'] = {'info': swarm_info}
            else:
                self.results['docker']['swarm'] = {'info': swarm_info}
        except DockerException:
            pass

    def fail(self, msg):
        self.client.fail(msg)


def main():
    argument_spec = dict()

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    results = dict(
        changed=False
    )

    InfoManager(client, results)
    client.module.exit_json(**results)

if __name__ == '__main__':
    main()
