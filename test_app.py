# 숙제 도우미 챗봇의 테스트 (맥에서는 python3 test_app.py, Actions에서는 pytest)
# 모델 설정 (model.json)과 앱의 /healthz 응답을 봅니다
import json
import os
import threading
import unittest
import urllib.request

import app

HERE = os.path.dirname(os.path.abspath(__file__))

# 팀이 쓰기로 한 모델
MODELS = ["qwen2.5:0.5b", "qwen2.5:1.5b", "qwen2.5:3b"]


class ChatbotTest(unittest.TestCase):
    def read_settings(self):
        try:
            with open(os.path.join(HERE, "model.json"), encoding="utf-8") as f:
                return json.load(f)
        except ValueError as e:
            problem = e
        self.fail("model.json의 JSON 꼴이 깨졌습니다 (쉼표, 따옴표): %s" % problem)

    def test_model_name(self):
        name = self.read_settings().get("model")
        if name not in MODELS:
            self.fail("모델 이름이 목록에 없습니다: %r" % name)

    def test_max_answer(self):
        n = self.read_settings().get("max_answer")
        if not isinstance(n, int) or not 1 <= n <= 1000:
            self.fail("max_answer는 1 ~ 1000 사이의 숫자여야 합니다: %r" % n)

    def test_healthz(self):
        settings = self.read_settings()
        server = app.make_server("127.0.0.1", 0)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        port = server.server_address[1]
        try:
            url = "http://127.0.0.1:%d/healthz" % port
            with urllib.request.urlopen(url, timeout=5) as r:
                body = json.loads(r.read().decode("utf-8"))
        finally:
            server.shutdown()
            server.server_close()
        self.assertEqual(body, {"status": "ok", "model": settings.get("model")})


if __name__ == "__main__":
    unittest.main(verbosity=2)
