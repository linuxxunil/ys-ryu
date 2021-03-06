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

import json
from webob import Response

from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from ryu.base import app_manager
from ryu.lib import dpid as dpid_lib
from ryu.topology.ys_api import get_switch, get_link, get_clink, \
                        get_lldp_interval, set_lldp_interval, get_slink, get_vlan, set_vlan

# REST API for switch configuration
#
# get all the switches
# GET /v1.0/topology/switches
#
# get the switch
# GET /v1.0/topology/switches/<dpid>
#
# get all the links
# GET /v1.0/topology/links
#
# get the links of a switch
# GET /v1.0/topology/links/<dpid>
#
# where
# <dpid>: datapath id in 16 hex
# 
# by jesse add
# get the links of switch of other controller
# GET /v1.0/topology/clinks
#
# by jesse add
# get the links of switch of same controller
# GET /v1.0/topology/slinks
#
# get interval value for lldp 
# GET /v1.0/topology/lldp
#
# set interval value for lldp 
# POST /v1.0/topology/lldp
#
# request body format:
#   {"interval": "<float>"}
# 
# get vlan for lldp 
# GET /v1.0/topology/vlan
#
# set vlan for lldp 
# POST /v1.0/topology/vlan
#
# request body format:
#   {"vlan_vid": "<int, untagged = 0>"}
# 


class TopologyAPI(app_manager.RyuApp):
    _CONTEXTS = {
        'wsgi': WSGIApplication
    }

    def __init__(self, *args, **kwargs):
        super(TopologyAPI, self).__init__(*args, **kwargs)

        wsgi = kwargs['wsgi']
        wsgi.register(TopologyController, {'topology_api_app': self})

class TopologyController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(TopologyController, self).__init__(req, link, data, **config)
        self.topology_api_app = data['topology_api_app']

    @route('topology', '/v1.0/topology/switches',
           methods=['GET'])
    def list_switches(self, req, **kwargs):
        return self._switches(req, **kwargs)

    @route('topology', '/v1.0/topology/switches/{dpid}',
           methods=['GET'], requirements={'dpid': dpid_lib.DPID_PATTERN})
    def get_switch(self, req, **kwargs):
        return self._switches(req, **kwargs)

    @route('topology', '/v1.0/topology/links',
           methods=['GET'])
    def list_links(self, req, **kwargs):
        return self._links(req, **kwargs)

    @route('topology', '/v1.0/topology/links/{dpid}',
           methods=['GET'], requirements={'dpid': dpid_lib.DPID_PATTERN})
    def get_links(self, req, **kwargs):
        return self._links(req, **kwargs)

    # by jesse
    @route('topology', '/v1.0/topology/clinks',
           methods=['GET'])
    def list_clinks(self, req, **kwargs):
        return self._clinks(req, **kwargs)

    # by jesse
    @route('topology', '/v1.0/topology/slinks',
           methods=['GET'])
    def list_slinks(self, req, **kwargs):
        return self._slinks(req, **kwargs)

    #@route('topology', '/v1.0/topology/clinks/{dpid}',
    #       methods=['GET'], requirements={'dpid': dpid_lib.DPID_PATTERN})
    #def get_clinks(self, req, **kwargs):
    #    return self._clinks(req, **kwargs)

    # by jesse 
    @route('topology', '/v1.0/topology/lldp',
           methods=['GET'])
    def get_lldp(self, req, **kwargs):
        return self._lldp(req, **kwargs)

    @route('topology', '/v1.0/topology/lldp',
           methods=['POST'])
    def set_lldp(self, req, **kwargs):
        return self._lldp(req, **kwargs)

    def _switches(self, req, **kwargs):
        dpid = None
        if 'dpid' in kwargs:
            dpid = dpid_lib.str_to_dpid(kwargs['dpid'])
        switches = get_switch(self.topology_api_app, dpid)
        body = json.dumps([switch.to_dict() for switch in switches])
        return Response(content_type='application/json', body=body)

    def _links(self, req, **kwargs):
        dpid = None
        if 'dpid' in kwargs:
            dpid = dpid_lib.str_to_dpid(kwargs['dpid'])
        links = get_link(self.topology_api_app, dpid)
        body = json.dumps([link.to_dict() for link in links])
        return Response(content_type='application/json', body=body)

    # by jesse
    def _clinks(self, req, **kwargs):
        dpid = None
        #if 'dpid' in kwargs:
        #   dpid = dpid_lib.str_to_dpid(kwargs['dpid'])
        links = get_clink(self.topology_api_app, dpid)
        body = json.dumps([link.to_dict() for link in links])
        return Response(content_type='application/json', body=body)


    # by jesse
    def _slinks(self, req, **kwargs):
        dpid = None
        #if 'dpid' in kwargs:
        #   dpid = dpid_lib.str_to_dpid(kwargs['dpid'])
        links = get_slink(self.topology_api_app, dpid)
        body = json.dumps([link.to_dict() for link in links])
        return Response(content_type='application/json', body=body)

    # by jesse
    def _lldp(self, req, **kwargs):
        if req.method == 'GET':
            req_interval = get_lldp_interval(self.topology_api_app, req.method)
        elif req.method == 'POST':
            
            try:
                param = json.loads(req.body) if req.body else {}
            except SyntaxError :
                return Response(status=400)
            interval = param['interval']
            print interval
            if interval is not None :
                req_interval = set_lldp_interval(self.topology_api_app, req.method, interval)
            else:
                req_interval = ""

        dict = { "interval":req_interval }
        body = json.dumps(dict)
        return Response(content_type='application/json', body=body)

    # by jesse 
    @route('topology', '/v1.0/topology/vlan',
           methods=['GET'])
    def get_vlan(self, req, **kwargs):
        return self._vlan(req, **kwargs)

    @route('topology', '/v1.0/topology/vlan',
           methods=['POST'])
    def set_vlan(self, req, **kwargs):
        return self._vlan(req, **kwargs)


    # by jesse
    def _vlan(self, req, **kwargs):
        if req.method == 'GET':
            req_vlan_vid = get_vlan(self.topology_api_app, req.method)
        elif req.method == 'POST':
            try:
                param = json.loads(req.body) if req.body else {}
            except SyntaxError :
                return Response(status=400)
            vlan_vid = param['vlan_vid']
            if vlan_vid is not None :
                req_vlan_vid = set_vlan(self.topology_api_app, req.method, vlan_vid)
            else:
                req_vlan_vid = -1

        dict = { "vlan_vid":req_vlan_vid }
        body = json.dumps(dict)
        return Response(content_type='application/json', body=body)
