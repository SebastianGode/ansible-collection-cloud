#!/usr/bin/python
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

DOCUMENTATION = '''
---
module: lb_listener
short_description: Add/Delete listener for load balancer from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Add or Remove listener for Enhanced Load Balancer from the OTC load-balancer
    service(ELB).
options:
  name:
    description:
      - Name that has to be given to the listener
    type: str
  state:
    description:
      - Should the resource be present or absent.
    choices: [present, absent]
    default: present
    type: str
  description:
    description:
      - Provides supplementary information about the listener.
    type: str
  protocol:
    description:
      - Specifies the load balancer protocol.
    choices: [TCP, HTTP, UDP, TERMINATED_HTTPS]
    required: true
    type: str
  protocol_port:
    description:
      - Specifies the port used by the load balancer.
    required: true
    type: int
  loadbalancer:
    description:
      - Specifies the associated load balancer.
    required: true
    type: str
  connection_limit:
    description:
      - Specifies the maximum number of connections (from -1 to 2147483647).
    default: -1
    type: int
  admin_state_up:
    description:
      - Specifies the administrative status of the listener.
    type: bool
  http2_enable:
    description:
      - Specifies whether to use HTTP/2 (valid only for TERMINATED_HTTPS).
    default: false
    type: bool
  default_pool_id:
    description:
      - Specifies the ID of the associated backend server group.
    type: str
  default_tls_container_ref:
    description:
      - Specifies the ID of the server certificate used by the listener
       (only for TERMINATED_HTTPS).
    default: null
    type: str
  client_ca_tls_container_ref:
    description:
      - Specifies the ID of the CA certificate used by the listener
       (only for TERMINATED_HTTPS).
    default: null
    type: str
  sni_container_refs:
    description:
      - Lists the IDs of SNI certificates
       (server certificates with a domain name) used by the listener
        (only for TERMINATED_HTTPS).
    default: []
    type: list
    elements: str
  tls_ciphers_policy:
    description:
      - Specifies the security policy used by the listener (only for TERMINATED_HTTPS).
       (server certificates with a domain name) used by the listener.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
lb_listener:
  description: Specifies the listener.
  type: complex
  returned: On Success.
  contains:
    id:
      description: Specifies the listener ID.
      type: str
      sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
    name:
      description: Specifies the listener name.
      type: str
      sample: "elb_test"
    description:
      description: Provides supplementary information about the listener.
      type: str
    protocol:
      description: Specifies the load balancer protocol.
      type: str
      sample: "TCP"
    protocol_port:
      description: Specifies the port used by the load balancer.
      type: int
      sample: "80"
    loadbalancers:
      description: Specifies the ID of the associated load balancer.
      type: list
    connection_limit:
      description: Specifies the maximum number of connections.
      type: int
    admin_state_up:
      description: Specifies the administrative status of the listener.
      type: bool
    default_pool_id:
      description: Specifies the ID of the associated backend server group.
      type: str
    tags:
      description: Tags the listener.
      type: str
    created_at:
      description: Specifies the time when the listener was created.
      type: str
    updated_at:
      description: Specifies the time when the listener was updated.
      type: str
'''

EXAMPLES = '''
# Create a lb listener.
- lb_listener:
    state: present
    protocol_port: 80
    protocol: TCP
    loadbalancer_id: "0416b6f1-877f-4a51-987e-978b3f084253"
    name: listener-test
    admin_state_up: true

# Create a HTTPS lb listener.
- lb_listener:
    state: present
    protocol_port: 443
    protocol: TERMINATED_HTTPS
    default_tls_container_ref: "02dcd56799e045bf8b131533cc911dd6"
    loadbalancer_id: "0416b6f1-877f-4a51-987e-978b3f084253"
    name: listener-test
    admin_state_up: true

# Create a HTTPS lb listener with the SNI feature.
- lb_listener:
    state: present
    protocol_port: 443
    protocol: TERMINATED_HTTPS
    default_tls_container_ref: "02dcd56799e045bf8b131533cc911dd6"
    loadbalancer_id: "0416b6f1-877f-4a51-987e-978b3f084253"
    name: listener-test
    admin_state_up: true
    sni_container_refs: ["e15d1b5000474adca383c3cd9ddc06d4", "5882325fd6dd4b95a88d33238d293a0f"]
    
# Delete a load balancer(and all its related resources)
- lb_listener:
    state: absent
    name: listener-test
'''

import time

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LoadBalancerListenerModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
        state=dict(default='present', choices=['absent', 'present']),
        description=dict(required=False),
        protocol=dict(required=True, choices=['TCP', 'HTTP', 'UDP', 'TERMINATED_HTTPS']),
        protocol_port=dict(required=True, type='int'),
        loadbalancer=dict(required=True, type='str'),
        connection_limit=dict(required=False, default=-1, type='int'),
        admin_state_up=dict(required=False, type='int'),
        http2_enable=dict(required=False, default=False, type='bool'),
        default_pool_id=dict(required=False, type='str'),
        default_tls_container_ref=dict(required=False, type='str'),
        client_ca_tls_container_ref=dict(required=False, type='str'),
        sni_container_refs=dict(required=False, type='list', elements='str'),
        tls_ciphers_policy=dict(required=False, type='str'),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        changed = False
        self.exit_json(changed=changed)


def main():
    module = LoadBalancerListenerModule()
    module()


if __name__ == '__main__':
    main()