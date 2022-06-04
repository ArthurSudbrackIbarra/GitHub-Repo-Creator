from os import path
import base64


class TokenManager:
    def __init__(self) -> None:
        self.tokenPath = path.abspath(
            path.join(path.dirname(__file__), '../config/TOKEN'))

    def readToken(self) -> str:
        with open(self.tokenPath, 'r') as tokenFile:
            base64Token = tokenFile.readline()
            base64Bytes = base64Token.encode("ascii")
            tokenBytes = base64.b64decode(base64Bytes)
            return tokenBytes.decode("ascii")

    def writeToken(self, accessToken: str) -> None:
        with open(self.tokenPath, 'w') as tokenFile:
            tokenBytes = accessToken.encode("ascii")
            base64Bytes = base64.b64encode(tokenBytes)
            base64Token = base64Bytes.decode("ascii")
            tokenFile.write(base64Token)
