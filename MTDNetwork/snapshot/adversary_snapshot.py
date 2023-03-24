import pickle
from MTDNetwork.component.adversary import Adversary
from MTDNetwork.snapshot import Snapshot


class AdversarySnapshot(Snapshot):
    def __init__(self):
        super().__init__()

    def save_adversary(self, adversary: Adversary, timestamp: float):
        """
        saving adversary snapshot
        """
        file_name = self.get_file_by_time('adversary', timestamp)
        with open(file_name, 'wb') as f:
            pickle.dump(adversary, f, pickle.HIGHEST_PROTOCOL)

    def load_adversary(self, timestamp: float):
        """
        loading adversary based on saved snapshot
        """
        if timestamp == 0:
            return
        file_name = self.get_file_by_time('adversary', timestamp)
        with open(file_name, 'rb') as f:
            adversary = pickle.load(f)
            return adversary
