class Artist:
    def __init__(
        self, 
        name: str | None,
        aliases: list[str] | None = None,
    ):
        self.name = name
        self.aliases = aliases if aliases is not None else []
    
    def __str__(self):
        return (f"{self.name} {self.aliases}")