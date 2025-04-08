from dataclasses import dataclass

@dataclass(frozen=True)
class Address:
    postal_code: str
    prefecture: str
    city: str
    street: str

    def __eq__(self, other):
        if isinstance(other, Address):
            return (self.postal_code == other.postal_code and
                    self.prefecture == other.prefecture and
                    self.city == other.city and
                    self.street == other.street)
        return False 