from .base_node import BaseNode


class DepositUsNode(BaseNode):
    """Represents a SYNAPSE-US node."""

    @classmethod
    def payload_for_create(cls, nickname, **kwargs):
        """Build the API 'create node' payload specific to SYNAPSE-US."""
        payload = super().payload_for_create('DEPOSIT-US',
                                             nickname=nickname,
                                             **kwargs)
        return payload
