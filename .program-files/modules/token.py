from os import path
from base64 import b64encode, b64decode


class TokenManager:
    def __init__(self) -> None:
        self.tokenPath = path.abspath(
            path.join(path.dirname(__file__), '../configurations/token.txt'))

    def readToken(self) -> str:
        if not path.exists(self.tokenPath):
            return ""
        with open(self.tokenPath, 'r') as tokenFile:
            base64Token = tokenFile.readline()
            base64Bytes = base64Token.encode("ascii")
            tokenBytes = b64decode(base64Bytes)
            return tokenBytes.decode("ascii")

    def writeToken(self, accessToken: str) -> None:
        with open(self.tokenPath, 'w+') as tokenFile:
            tokenBytes = accessToken.encode("ascii")
            base64Bytes = b64encode(tokenBytes)
            base64Token = base64Bytes.decode("ascii")
            tokenFile.write(base64Token)
