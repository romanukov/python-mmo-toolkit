from dataclasses import dataclass


@dataclass
class RPCMethod:
    func: callable
    argument_model: type
