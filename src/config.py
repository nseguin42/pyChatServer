import orjson as json


class Config:
    model: str
    model_config: dict
    use_gpu_if_available: bool
    websocket_ip: str
    websocket_port: int

    def __init__(self, config_dict: dict):
        self.model = config_dict["model"]
        self.model_config = config_dict["model_config"]
        self.use_gpu_if_available = config_dict["use_gpu_if_available"]
        self.websocket_ip = config_dict["websocket_ip"] or "localhost"
        self.websocket_port = config_dict["websocket_port"] or 8765

    @staticmethod
    def load(path: str) -> "Config":
        with open(path) as f:
            data = json.loads(f.read())
            return Config(data)
