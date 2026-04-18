from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr, EthAddr
import logging

log = core.getLogger()

FIREWALL_RULES = [
    {'src': '10.0.0.1', 'dst': '10.0.0.2', 'action': 'allow'},
    {'src': '10.0.0.2', 'dst': '10.0.0.1', 'action': 'allow'},
    {'src': '10.0.0.3', 'dst': None, 'action': 'block'},
    {'src': None, 'dst': '10.0.0.3', 'action': 'block'},
    {'src': None, 'dst': '10.0.0.4', 'port': 80, 'action': 'block'},
]

class Firewall(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)
        log.info("Firewall controller connected to switch: %s" % connection)

    def _match_rule(self, src_ip, dst_ip, dst_port=None):
        for rule in FIREWALL_RULES:
            src_match = rule['src'] is None or rule['src'] == str(src_ip)
            dst_match = rule['dst'] is None or rule['dst'] == str(dst_ip)
            port_match = 'port' not in rule or rule['port'] == dst_port
            if src_match and dst_match and port_match:
                return rule['action']
        return 'allow'

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            return

        ip_packet = packet.find('ipv4')
        if not ip_packet:
            self._forward(event, packet)
            return

        src_ip = ip_packet.srcip
        dst_ip = ip_packet.dstip

        tcp_packet = packet.find('tcp')
        udp_packet = packet.find('udp')
        dst_port = None
        if tcp_packet:
            dst_port = tcp_packet.dstport
        elif udp_packet:
            dst_port = udp_packet.dstport

        action = self._match_rule(src_ip, dst_ip, dst_port)

        if action == 'block':
            log.warning("BLOCKED: %s -> %s (port: %s)" % (src_ip, dst_ip, dst_port))
            self._install_drop_rule(event, ip_packet, dst_port)
        else:
            log.info("ALLOWED: %s -> %s" % (src_ip, dst_ip))
            self._forward(event, packet)

    def _install_drop_rule(self, event, ip_packet, dst_port=None):
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800
        msg.match.nw_src = ip_packet.srcip
        msg.match.nw_dst = ip_packet.dstip
        if dst_port:
            msg.match.tp_dst = dst_port
        msg.priority = 100
        msg.hard_timeout = 30
        self.connection.send(msg)
        log.warning("DROP rule installed: %s -> %s" % (ip_packet.srcip, ip_packet.dstip))

    def _forward(self, event, packet):
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, event.port)
        msg.priority = 10
        msg.hard_timeout = 30
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        self.connection.send(msg)

class FirewallController(object):
    def __init__(self):
        core.openflow.addListeners(self)
        log.info("Firewall Controller starting...")

    def _handle_ConnectionUp(self, event):
        Firewall(event.connection)

def launch():
    core.registerNew(FirewallController)
    log.info("SDN Firewall launched!")
