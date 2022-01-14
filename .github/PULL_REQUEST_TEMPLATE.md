# Title: ex. [FR] 특정 속성에 대해 중요도 100%로 유사검색 결과 생성
## PR : File a bug report
- labels: ex. FR(New Feature), BUG(bug report)
- assignees:
  - pminhyung

### [AS-IS]
ex. 현재 모든 속성에 대하여 source와 target 간 모든 pair에 대해 distance 계산 후 유사 검색 결과 생성

### [TO-BE]
ex. text similarity 계산 후 유사 검색 결과에서, 특정 속성의 값이 상이할 때 결과에서 완전히 제외하도록 로직 추가