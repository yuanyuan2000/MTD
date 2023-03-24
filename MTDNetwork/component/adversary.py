import logging
from MTDNetwork.statistic.attack_statistics import AttackStatistics
from MTDNetwork.data.constants import HACKER_ATTACK_ATTEMPT_MULTIPLER


class Adversary:
    def __init__(self, network, attack_threshold):
        self.network = network
        self._compromised_users = []
        self._compromised_hosts = []
        self._host_stack = []
        self._attack_counter = [0 for n in range(self.network.get_total_nodes())]
        self._stop_attack = []
        self._attack_threshold = attack_threshold
        self._pivot_host_id = -1
        self._curr_host_id = -1
        self.curr_host = None
        self._curr_ports = []
        self._curr_vulns = []
        self._max_attack_attempts = HACKER_ATTACK_ATTEMPT_MULTIPLER * network.get_total_nodes()
        self._curr_attempts = 0
        self.target_compromised = False
        self.observed_changes = {}

        self._attack_stats = AttackStatistics()
        self._curr_process = 'SCAN_HOST'

    def swap_hosts_in_compromised_hosts(self, host_id, other_host_id):
        """
        update compromised host ids for host topology shuffle
        """
        new_compromised_hosts = []

        for i in self._compromised_hosts:
            if i == host_id:
                new_compromised_hosts.append(other_host_id)
            elif i == other_host_id:
                new_compromised_hosts.append(host_id)
            else:
                new_compromised_hosts.append(i)

        self._compromised_hosts = new_compromised_hosts

    def update_compromise_progress(self, now, proceed_time):
        """
        Updates the Hackers progress state when it compromises a host.
        """
        self._pivot_host_id = self._curr_host_id
        if self._curr_host_id not in self._compromised_hosts:
            self._compromised_hosts.append(self._curr_host_id)
            self._attack_stats.update_compromise_host(self.curr_host)
            logging.info(
                "Adversary: Host %i has been compromised at %.1fs!" % (self._curr_host_id, now + proceed_time))
            self.network.update_reachable_compromise(self._curr_host_id, self._compromised_hosts)

            for user in self.curr_host.get_compromised_users():
                if user not in self._compromised_users:
                    self._attack_stats.update_compromise_user(user)
            self._compromised_users = list(set(self._compromised_users + self.curr_host.get_compromised_users()))
            if self.network.is_compromised(self._compromised_hosts):
                # terminate the whole process
                return

            # If target network, set adversary as done once adversary has compromised target node
            # if self.network.get_target_node() == self._curr_host_id:
            # if self.network.get_network_type() == 0:
            #      # terminate the whole process
            #     self.target_compromised = True
            #     self.end_event.succeed()
            #     return
            #

    def get_compromised_hosts(self):
        return self._compromised_hosts

    def get_statistics(self):
        return self._attack_stats.get_record()

    # private
    def get_attack_stats(self):
        return self._attack_stats

    def get_host_stack(self):
        return self._host_stack

    def get_curr_host_id(self):
        return self._curr_host_id

    def get_curr_ports(self):
        return self._curr_ports

    def get_curr_attempts(self):
        return self._curr_attempts

    def get_stop_attack(self):
        return self._stop_attack

    def get_attack_threshold(self):
        return self._attack_threshold

    def get_curr_vulns(self):
        return self._curr_vulns

    def get_max_attack_attempts(self):
        return self._max_attack_attempts

    def get_curr_process(self):
        return self._curr_process

    def get_attack_counter(self):
        return self._attack_counter

    def get_pivot_host_id(self):
        return self._pivot_host_id

    def get_compromised_users(self):
        return self._compromised_users

    # public
    def get_curr_host(self):
        return self.curr_host

    def get_network(self):
        return self.network

    # setter
    def set_curr_host_id(self, host_id):
        self._curr_host_id = host_id

    def set_curr_host(self, host):
        self.curr_host = host

    def set_pivot_host_id(self, host_id):
        self._pivot_host_id = host_id

    def set_curr_ports(self, ports):
        self._curr_ports = ports

    def set_curr_vulns(self, vulns):
        self._curr_vulns = vulns

    def set_curr_attempts(self, curr_attempts):
        self._curr_attempts = curr_attempts

    def set_host_stack(self, host_stack):
        self._host_stack = host_stack

    def set_curr_process(self, curr_process):
        self._curr_process = curr_process
