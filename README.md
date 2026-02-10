# Seoul Bakery Map (서울 빵집 지도) 🥐

네이버 지도에서 '서울 빵집'을 검색하여 리뷰 수가 많은 인기 베이커리를 시각화한 프로젝트입니다.

## 지도 보기
[👉 서울 빵집 지도 보러가기](https://your-username.github.io/bread-map/)
*(GitHub Pages 설정 후 위 링크가 활성화됩니다)*

## 데이터 출처
- **Source**: 네이버 지도 (Naver Maps)
- **Criteria**: 방문자 리뷰 50개 이상인 인기 빵집 상위 20곳
- **Date**: 2026-02-10

## 기술 스택
- **Crawler**: Python, Playwright
- **Visualizer**: Folium (Leaflet.js)

## 실행 방법
1. 의존성 설치
```bash
pip install -r requirements.txt
playwright install chromium
```

2. 데이터 수집
```bash
python3 bakery_crawler.py
```

3. 지도 생성
```bash
python3 visualize_map.py
```
