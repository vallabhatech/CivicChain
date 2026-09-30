"""Small hash-chain primitive used to record vote integrity metadata."""
from __future__ import annotations

import hashlib
from collections.abc import Iterable


class HashDataBlock:
    """Create a deterministic SHA-256 link from data and the previous hash."""

    def __init__(self, previous_block_hash: str, data_list: Iterable[str]) -> None:
        self.previous_block_hash = str(previous_block_hash)
        self.data_list = [str(item) for item in data_list]
        self.block_data = "-".join(self.data_list) + "-" + self.previous_block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode("utf-8")).hexdigest()
