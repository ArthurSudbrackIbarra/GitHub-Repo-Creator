from os import path
import base64

TOKEN_FILE_PATH = "config/TOKEN.txt"


class TokenManager:
    def __init__(self) -> None:
        self.absoluteFilePath = path.abspath(TOKEN_FILE_PATH)

    def readToken(self) -> str:
        with open(self.absoluteFilePath, 'r') as tokenFile:
            base64Token = tokenFile.readline()
            base64Bytes = base64Token.encode("ascii")
            tokenBytes = base64.b64decode(base64Bytes)
            return tokenBytes.decode("ascii")

    def writeToken(self, accessToken: str) -> None:
        with open(self.absoluteFilePath, 'w') as tokenFile:
            tokenBytes = accessToken.encode("ascii")
            base64Bytes = base64.b64encode(tokenBytes)
            base64Token = base64Bytes.decode("ascii")
            tokenFile.write(base64Token)
