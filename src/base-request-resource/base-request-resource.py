import socket
import ssl



class URL:
    # URL 클래스의 생성자
    # url을 인자로 받아서 이를 분리해 scheme, host, path 셋업
    def __init__(self, url):
        # scheme 인자 추출
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https"]

        # url에서 host와 path 추출
        if "/" not in url: url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url

        # https는 일반적으로 443 포트번호를 사용한다
        # http는 일반적으로 80 포트번호를 사용한다
        if self.scheme == "http": self.port = 80
        elif self.scheme == "https": self.port = 443

    # URL을 가지고 리소스를 요청하는 함수
    # socket을 통해 웹서버에 연결하고 인자를 통해 리소스 호출
    def request(self):
        # socket을 생성하고 host와 연결한다
        # 다른 컴퓨터을 어떻게 찾을지(family), 어떻게 데이터를 전달할지(type), 패킷 전송 방법(proto) 등을 설정
        s = socket.socket(
            family = socket.AF_INET,
            type = socket.SOCK_STREAM,
            proto = socket.IPPROTO_TCP,
        )

        # socket을 python에서 제공하는 ssl을 통해 TLS 보안을 통해 암호화된 연결로 만들어줄 수 있다
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname = self.host)
            s.connect((self.host, self.port))
        elif self.scheme == "http":
            s.connect((self.host, self.port))

        # 인스턴스에 기록한 host, path를 통해서 리소스 요청 문자열을 작성
        # 반드시 엔터 두번(\r\n) 작성 필요
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"
        s.send(request.encode("utf8"))

        # 소켓을 통해 응답을 읽을 수 있는 객체로 만들고 첫줄(HTTP/1.0 200 OK)을 split으로 분리
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statuslines = response.readline()
        version, status, explanation = statuslines.split(" ", 2)

        # 헤더 데이터를 기록한다.
        # \r\n 나오기 전까지는 모두 헤더 데이터이므로 이를 반복하여 기록한다
        # casefold(소문자로 치환), strip(값 양쪽 공백, 개행을 제거)를 사용한다
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break

            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        # content type과 같은 헤더는 반드시 필요하다
        # 없으면 에러를 발생시킨다
        assert "transfer-encoding" not in response_headers
        assert "content-type" in response_headers

        body = response.read()
        s.close()

        return body

# body 태그에서 순수 텍스트만 print하는 함수
# body의 한글자 한글자 읽어가면서 처리
# <p>hello</p>, '<'로 시작했으니 in_tag true, '>' 나올때까지 스킵
def show(body):
    in_tag = False

    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url):
    body = url.request()
    show(body)


if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))
