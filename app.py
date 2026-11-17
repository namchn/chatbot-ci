# 숙제 도우미 챗봇의 작은 웹 앱 (표준 라이브러리만, 포트 8000)
# 어느 모델을 쓰고 답을 몇 글자까지 할지는 model.json에 있고, 이 설정이 이미지에 함께 들어갑니다
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))


def load_settings():
    with open(os.path.join(HERE, "model.json"), encoding="utf-8") as f:
        return json.load(f)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        settings = load_settings()
        if self.path == "/healthz":
            self.reply(200, {"status": "ok", "model": settings.get("model")})
        elif self.path == "/":
            self.reply(200, {"message": "숙제 도우미 챗봇입니다",
                             "model": settings.get("model"),
                             "max_answer": settings.get("max_answer")})
        else:
            self.reply(404, {"error": "not found"})

    def reply(self, code, body):
        data = (json.dumps(body, ensure_ascii=False) + "\n").encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass  # 요청마다 찍는 줄을 끔 (테스트 화면을 깨끗하게)


def make_server(host="0.0.0.0", port=8000):
    return ThreadingHTTPServer((host, port), Handler)


if __name__ == "__main__":
    print("chatbot-ci 앱을 켰습니다: 포트 8000 (끄려면 Ctrl+C)", flush=True)
    try:
        make_server().serve_forever()
    except KeyboardInterrupt:
        print("앱을 껐습니다")
