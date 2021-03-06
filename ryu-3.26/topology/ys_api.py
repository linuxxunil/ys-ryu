# Copyright (C) 2013 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.topology import ys_event as event


def get_switch(app, dpid=None):
    rep = app.send_request(event.EventSwitchRequest(dpid))
    return rep.switches


def get_all_switch(app):
    return get_switch(app)


def get_link(app, dpid=None):
    rep = app.send_request(event.EventLinkRequest(dpid))
    return rep.links


def get_all_link(app):
    return get_link(app)

# by jesse : clink request
def get_clink(app, dpid=None):
	rep = app.send_request(event.EventCLinkRequest(dpid))
	return rep.links

# by jesse : slink request
def get_slink(app, dpid=None):
	rep = app.send_request(event.EventSLinkRequest(dpid))
	return rep.links


# by jesse : lldp interval
def get_lldp_interval(app, method):
	rep = app.send_request(event.EventLLDPRequest(method))
	return rep.interval 

def set_lldp_interval(app, method, interval):
	rep = app.send_request(event.EventLLDPRequest(method, interval))
	return rep.interval


app_manager.require_app('ryu.topology.ys_switches', api_style=True)
