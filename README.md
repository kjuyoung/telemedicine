# 원격진료 프로젝트

---
## 1. 프로젝트 세팅 방법
### 1.1. 개발 환경
 - Python : 3.11
 - Django : 5.0.1
 - Django REST Framework : 3.14.0
 - MySQL : 8.2
### 1.2. 프로젝트 세팅
- Git clone을 이용하여 telemedicine repo 다운로드
> git clone https://github.com/kjuyoung/telemedicine.git

- requirements.txt를 이용하여 패키지 설치
> pip install -r requirements.txt

- DB 생성 후 아래 명령어 통해 스키마 적용
> python manage.py makemigrations
> 
> python manage.py migrate

***
## 2. 데이터 입력 방법
- _telemedicine.postman_collection.json_ 파일을 이용하여 아래 환자, 의사 데이터를 미리 DB에 입력
1. **환자 등록 API** (name)
2. **의사 등록 API** (name, hospital_name, diagnosis_department, uninsured_services_department, business_hours)

- 참고로 postman 설정파일 안에 예시 json 데이터를 만들어 두었습니다. 

***
## 3. 각 로직 실행 방법
### 3.1. 의사 조회
- postman 설정파일의 의사 조회 API를 이용하여 로직 실행
- 예시) 127.0.0.1:8000/doctor/?hospital_name=서울병원&name=김의사 

### 3.2. 진료 요청
- 진료 요청 API를 이용하여 진료 요청 생성 로직 실행
- 예시) 127.0.0.1:8000/diagnosis/

### 3.3. 진료 요청 검색
- 진료 요청 검색 API를 이용하여 진료 요청 생성 로직 실행
- 예시) 127.0.0.1:8000/diagnosis/?doctor_id=1

### 3.4. 진료 요청 수락
- 진료 요청 수락 API를 이용하여 진료 요청 생성 로직 실행
- 예시) 127.0.0.1:8000/diagnosis/{진료요청id}/accept/

***
## 4. 프로젝트 구조
- 구조

- ERD
![img.png](img.png)

***
## 5. 기능
### 5.1. 의사 조회

### 5.2. 진료 요청

### 5.3. 진료 요청 검색


### 5.4. 진료 요청 수락
