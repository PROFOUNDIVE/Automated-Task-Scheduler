import datetime

# Task 클래스 정의
class Task:
    def __init__(self, title, description, priority, estimated_time):
        """
        :param title: 업무 제목
        :param description: 상세 설명
        :param priority: 우선순위 ("High", "Medium", "Low")
        :param estimated_time: 예상 소요시간 (분 단위)
        """
        self.title = title
        self.description = description
        self.priority = priority
        self.estimated_time = estimated_time
        self.scheduled_start = None
        self.scheduled_end = None

    def __repr__(self):
        return f"Task({self.title}, {self.priority}, {self.estimated_time} min)"

# 우선순위 매핑: High=3, Medium=2, Low=1
priority_mapping = {"High": 3, "Medium": 2, "Low": 1}

def schedule_tasks(tasks):
    """
    주어진 Task 리스트를 우선순위(높은 순)와 예상 소요시간(짧은 순)으로 정렬하고,
    현재 시간부터 순차적으로 스케줄을 배정합니다.
    """
    # 우선순위 내림차순, 예상 소요시간 오름차순 정렬
    sorted_tasks = sorted(tasks, key=lambda t: (-priority_mapping[t.priority], t.estimated_time))
    
    current_time = datetime.datetime.now()  # 현재 시간을 시작점으로 사용
    print(f"current time: {current_time}")
    for task in sorted_tasks:
        task.scheduled_start = current_time
        task.scheduled_end = current_time + datetime.timedelta(minutes=task.estimated_time)
        current_time = task.scheduled_end  # 다음 Task의 시작 시간 업데이트
    return sorted_tasks

def main():
    # 데모용 Task 생성
    tasks = [
        Task("보고서 작성", "분기 보고서 초안 작성", "High", 60),
        Task("고객 이메일 회신", "이메일 답변", "Medium", 30),
        Task("팀 회의", "프로젝트 업데이트 논의", "High", 45),
        Task("코드 리뷰", "PR 리뷰", "Low", 20),
        Task("UI 디자인", "신규 기능 UI 목업 제작", "Medium", 90)
    ]

    # 스케줄링 실행
    scheduled_tasks = schedule_tasks(tasks)
    
    # 스케줄링 결과 출력
    print("=== 스케줄링 결과 ===")
    for task in scheduled_tasks:
        start_str = task.scheduled_start.strftime('%H:%M')
        end_str = task.scheduled_end.strftime('%H:%M')
        print(f"{task.title} ({task.priority}) - 시작: {start_str}, 종료: {end_str}")

    # [선택사항] Google Calendar 연동 (예: Zapier 연동 시 이 부분을 Webhook으로 호출)
    # 아래 코드는 Google Calendar API를 이용해 이벤트를 생성하는 기본 틀의 예시입니다.
    # 실제 사용 시 구글 API 클라이언트 라이브러리와 OAuth 2.0 인증 절차를 추가해야 합니다.
    #
    # from googleapiclient.discovery import build
    # from google.oauth2.credentials import Credentials
    #
    # def create_google_calendar_event(task):
    #     event = {
    #         'summary': task.title,
    #         'description': task.description,
    #         'start': {
    #             'dateTime': task.scheduled_start.isoformat(),
    #             'timeZone': 'Asia/Seoul',
    #         },
    #         'end': {
    #             'dateTime': task.scheduled_end.isoformat(),
    #             'timeZone': 'Asia/Seoul',
    #         },
    #         'colorId': '11' if task.priority == "High" else '7'
    #     }
    #     # 인증 후 서비스 객체 생성
    #     # service = build('calendar', 'v3', credentials=creds)
    #     # event_result = service.events().insert(calendarId='primary', body=event).execute()
    #     # print(f"Event created: {event_result.get('htmlLink')}")
    #     pass
    #
    # # Google Calendar에 모든 스케줄 등록
    # for task in scheduled_tasks:
    #     create_google_calendar_event(task)

if __name__ == '__main__':
    main()
