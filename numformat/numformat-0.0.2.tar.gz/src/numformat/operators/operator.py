from abc import ABC, abstractmethod


class Operator(ABC):

    @abstractmethod
    def is_zero(self):
        pass

    @abstractmethod
    def get_order(self):
        pass

    @abstractmethod
    def get_sigfigs(self):
        pass

    @abstractmethod
    def set_sigfigs(self, desired_sig_figs):
        pass

    @abstractmethod
    def to_standard_notation(self):
        pass

    @abstractmethod
    def to_scientific_notation(self):
        pass

    @abstractmethod
    def to_engineering_notation(self):
        pass
