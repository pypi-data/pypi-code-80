"""Internet Control Message Protocol for IPv4."""
import logging

from pypacker import pypacker, checksum
from pypacker.pypacker import FIELD_FLAG_AUTOUPDATE

logger = logging.getLogger("pypacker")


# Types (icmp_type) and codes (icmp_code) -
# http://www.iana.org/assignments/icmp-parameters

ICMP_CODE_NONE			= 0		# for types without codes
ICMP_ECHOREPLY			= 0		# echo reply
ICMP_UNREACH			= 3		# dest unreachable, codes:
ICMP_UNREACH_NET		= 0		# bad net
ICMP_UNREACH_HOST		= 1		# bad host
ICMP_UNREACH_PROTO		= 2		# bad protocol
ICMP_UNREACH_PORT		= 3		# bad port
ICMP_UNREACH_NEEDFRAG		= 4		# IP_DF caused drop
ICMP_UNREACH_SRCFAIL		= 5		# src route failed
ICMP_UNREACH_NET_UNKNOWN	= 6		# unknown net
ICMP_UNREACH_HOST_UNKNOWN	= 7		# unknown host
ICMP_UNREACH_ISOLATED		= 8		# src host isolated
ICMP_UNREACH_NET_PROHIB		= 9		# for crypto devs
ICMP_UNREACH_HOST_PROHIB	= 10		# ditto
ICMP_UNREACH_TOSNET		= 11		# bad tos for net
ICMP_UNREACH_TOSHOST		= 12		# bad tos for host
ICMP_UNREACH_FILTER_PROHIB	= 13		# prohibited access
ICMP_UNREACH_HOST_PRECEDENCE	= 14		# precedence error
ICMP_UNREACH_PRECEDENCE_CUTOFF	= 15		# precedence cutoff
ICMP_SRCQUENCH			= 4		# packet lost, slow down
ICMP_REDIRECT			= 5		# shorter route, codes:
ICMP_REDIRECT_NET		= 0		# for network
ICMP_REDIRECT_HOST		= 1		# for host
ICMP_REDIRECT_TOSNET		= 2		# for tos and net
ICMP_REDIRECT_TOSHOST		= 3		# for tos and host
ICMP_ALTHOSTADDR		= 6		# alternate host address
ICMP_ECHO			= 8		# echo service
ICMP_RTRADVERT			= 9		# router advertise, codes:
ICMP_RTRADVERT_NORMAL		= 0		# normal
ICMP_RTRADVERT_NOROUTE_COMMON	= 16		# selective routing
ICMP_RTRSOLICIT			= 10		# router solicitation
ICMP_TIMEXCEED			= 11		# time exceeded, code:
ICMP_TIMEXCEED_INTRANS		= 0		# ttl==0 in transit
ICMP_TIMEXCEED_REASS		= 1		# ttl==0 in reass
ICMP_PARAMPROB			= 12		# ip header bad
ICMP_PARAMPROB_ERRATPTR		= 0		# req. opt. absent
ICMP_PARAMPROB_OPTABSENT	= 1		# req. opt. absent
ICMP_PARAMPROB_LENGTH		= 2		# bad length
ICMP_TSTAMP			= 13		# timestamp request
ICMP_TSTAMPREPLY		= 14		# timestamp reply
ICMP_INFO			= 15		# information request
ICMP_INFOREPLY			= 16		# information reply
ICMP_MASK			= 17		# address mask request
ICMP_MASKREPLY			= 18		# address mask reply
ICMP_TRACEROUTE			= 30		# traceroute
ICMP_DATACONVERR		= 31		# data conversion error
ICMP_MOBILE_REDIRECT		= 32		# mobile host redirect
ICMP_IP6_WHEREAREYOU		= 33		# IPv6 where-are-you
ICMP_IP6_IAMHERE		= 34		# IPv6 i-am-here
ICMP_MOBILE_REG			= 35		# mobile registration req
ICMP_MOBILE_REGREPLY		= 36		# mobile registration reply
ICMP_DNS			= 37		# domain name request
ICMP_DNSREPLY			= 38		# domain name reply
ICMP_SKIP			= 39		# SKIP
ICMP_PHOTURIS			= 40		# Photuris
ICMP_PHOTURIS_UNKNOWN_INDEX	= 0		# unknown sec index
ICMP_PHOTURIS_AUTH_FAILED	= 1		# auth failed
ICMP_PHOTURIS_DECOMPRESS_FAILED	= 2		# decompress failed
ICMP_PHOTURIS_DECRYPT_FAILED	= 3		# decrypt failed
ICMP_PHOTURIS_NEED_AUTHN	= 4		# no authentication
ICMP_PHOTURIS_NEED_AUTHZ	= 5		# no authorization
ICMP_TYPE_MAX			= 40


ICMP_TYPE_ECHO_REQ	= 0
ICMP_TYPE_UNREACH	= 3
ICMP_TYPE_QUENCH	= 4
ICMP_TYPE_ECHO_RESP	= 8
ICMP_TYPE_ECHO		= (ICMP_TYPE_ECHO_REQ, ICMP_TYPE_ECHO_RESP)
ICMP_TYPE_REDIRECT	= 5
ICMP_TYPE_TIMEEXCEED	= 11


class ICMP(pypacker.Packet):
	__hdr__ = (
		("type", "B", ICMP_ECHO),
		("code", "B", 0),
		("sum", "H", 0, FIELD_FLAG_AUTOUPDATE)
	)

	def _update_fields(self):
		# logger.debug("sum is: %d" % self.sum)
		if self.sum_au_active and self._changed():
			# logger.debug("sum is: %d" % self.sum)
			# logger.debug("header: %r", self.header_bytes)
			# logger.debug("body: %r", self.body_bytes)
			self.sum = 0
			self.sum = checksum.in_cksum(self.header_bytes + self.body_bytes)
			# logger.debug("sum is: %d" % self.sum)

	def _dissect(self, buf):
		# logger.debug("ICMP: adding fields for type: %d" % buf[0])
		self._init_handler(buf[0], buf[4:])
		return 4

	class Echo(pypacker.Packet):
		__hdr__ = (
			("id", "H", 0),
			("seq", "H", 1),
			("ts", "Q", 0)
		)

		def _dissect(self, buf):
			hlen = 12

			if len(buf) < 12:
				# not enough bytes for ts
				self.ts = None
				hlen = 4
			return hlen

	class Unreach(pypacker.Packet):
		__hdr__ = (
			("pad", "H", 0),
			("mtu", "H", 0)
		)

	class Quench(pypacker.Packet):
		__hdr__ = (
			("pad", "I", 0),
		)

	class Redirect(pypacker.Packet):
		__hdr__ = (
			("gw", "I", 0),
		)

	class TimeExceed(pypacker.Packet):
		__hdr__ = (
			("pad", "I", 0),
		)

	__handler__ = {
		ICMP_TYPE_ECHO: Echo,
		ICMP_TYPE_UNREACH: Unreach,
		ICMP_TYPE_QUENCH: Quench,
		ICMP_TYPE_REDIRECT: Redirect,
		ICMP_TYPE_TIMEEXCEED: TimeExceed
	}
