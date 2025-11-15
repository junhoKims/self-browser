# Base Request Resource

python으로 구현한 URL을 받아 헤더 정보를 출력하는 스크립트

## 기능

- URL을 받아 scheme, host, path등을 분리하여 사용
- socket을 통해 host와 연결 및 리소스 요청
- 암호화된 연결을 통해 https 스킴 URL도 지원

## 실행

```
python base-request-resource.py https://www.example.org/
```

## 참고

- http://www.example.org/
- http://browser.engineering/http.html
- https://blog.google/products/search/web-guide-labs/