import simpy
import logging
from MTDNetwork.component.time_network import TimeNetwork
from MTDNetwork.operation.mtd_operation import MTDOperation
from MTDNetwork.data.constants import ATTACKER_THRESHOLD
from MTDNetwork.component.adversary import Adversary
from MTDNetwork.operation.attack_operation import AttackOperation
from MTDNetwork.snapshot.snapshot_checkpoint import SnapshotCheckpoint
from MTDNetwork.statistic.metrics import Metrics
from MTDNetwork.component import game

logging.basicConfig(format='%(message)s', level=logging.INFO)


def main(start_time=0, finish_time=1000, scheme='randomly', checkpoints=None):
    # start the game
    new_game = game.Game()
    new_game.init(start_time, finish_time, scheme, checkpoints)
    new_game.run()


if __name__ == "__main__":
    main()
