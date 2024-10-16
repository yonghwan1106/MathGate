import streamlit as st
import random
import math

# 세션 상태 초기화
if 'user' not in st.session_state:
    st.session_state.user = {
        'name': '',
        'level': '초급',
        'score': 0,
        'total_questions': 0,
        'points': 0,
        'progress': {'초급': 0, '중급': 0, '고급': 0}
    }

def generate_question(level):
    if level == "초급":
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        operator = random.choice(['+', '-'])
        question = f"{a} {operator} {b} = ?"
        answer = eval(f"{a} {operator} {b}")
        explanation = f"{a} {operator} {b} = {answer}"
    elif level == "중급":
        a = random.randint(10, 50)
        b = random.randint(10, 50)
        operator = random.choice(['+', '-', '*'])
        question = f"{a} {operator} {b} = ?"
        answer = eval(f"{a} {operator} {b}")
        explanation = f"{a} {operator} {b} = {answer}"
    else:  # 고급
        operation = random.choice(['square_root', 'power', 'equation'])
        if operation == 'square_root':
            a = random.randint(1, 100)
            question = f"√{a} = ?"
            answer = math.sqrt(a)
            explanation = f"√{a} = {answer:.2f}"
        elif operation == 'power':
            a = random.randint(1, 10)
            b = random.randint(2, 3)
            question = f"{a}^{b} = ?"
            answer = a ** b
            explanation = f"{a}^{b} = {answer}"
        else:
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            c = a * b + random.randint(-5, 5)
            question = f"{a}x + {b} = {c}. x = ?"
            answer = (c - b) / a
            explanation = f"x = ({c} - {b}) / {a} = {answer}"
    return question, answer, explanation

def update_progress(level):
    st.session_state.user['progress'][level] += 1
    if st.session_state.user['progress'][level] >= 10:
        if level == '초급':
            st.session_state.user['level'] = '중급'
        elif level == '중급':
            st.session_state.user['level'] = '고급'

def level_problems_page():
    st.title("레벨별 수학 문제")
    level = st.selectbox("난이도를 선택하세요:", ["초급", "중급", "고급"])
    if st.button("새로운 문제 생성"):
        st.session_state.question, st.session_state.answer, st.session_state.explanation = generate_question(level)
        st.session_state.user['total_questions'] += 1
    
    if 'question' in st.session_state:
        st.write(f"문제: {st.session_state.question}")
        user_answer = st.number_input("답을 입력하세요:", step=0.1)
        if st.button("제출"):
            if abs(user_answer - st.session_state.answer) < 0.1:
                st.success("정답입니다!")
                st.session_state.user['score'] += 1
                st.session_state.user['points'] += 10
                update_progress(level)
            else:
                st.error(f"틀렸습니다. 정답은 {st.session_state.answer:.2f}입니다.")
                st.session_state.user['points'] -= 5

def learning_system_page():
    st.title("단계별 학습 시스템")
    st.write(f"현재 레벨: {st.session_state.user['level']}")
    for level, progress in st.session_state.user['progress'].items():
        st.write(f"{level} 진행도: {progress * 10}%")
        st.progress(progress / 10)
    st.write("각 레벨에서 10문제를 맞추면 다음 레벨로 올라갑니다.")
    
    st.subheader("레벨별 특징")
    st.write("초급: 간단한 덧셈, 뺄셈")
    st.write("중급: 곱셈 추가")
    st.write("고급: 제곱근, 지수, 간단한 방정식")

def point_system_page():
    st.title("포인트 시스템")
    st.write(f"현재 포인트: {st.session_state.user['points']}")
    st.subheader("포인트 획득 방법")
    st.write("- 정답: +10 포인트")
    st.write("- 오답: -5 포인트")
    
    st.subheader("포인트 사용")
    st.write("1. 힌트 구매: 50 포인트")
    st.write("2. 레벨 테스트 응시: 100 포인트")
    
    if st.button("힌트 구매 (50 포인트)"):
        if st.session_state.user['points'] >= 50:
            st.session_state.user['points'] -= 50
            st.success("힌트를 구매했습니다!")
        else:
            st.error("포인트가 부족합니다.")

def feedback_page():
    st.title("실시간 피드백 및 설명")
    if 'explanation' in st.session_state:
        st.write(f"최근 문제 설명: {st.session_state.explanation}")
    else:
        st.write("문제를 풀면 여기에 설명이 표시됩니다.")
    
    st.subheader("일반적인 팁")
    st.write("1. 문제를 천천히 읽고 이해하세요.")
    st.write("2. 필요한 정보를 모두 파악했는지 확인하세요.")
    st.write("3. 풀이 과정을 단계별로 나누어 접근하세요.")
    st.write("4. 답을 구한 후 문제와 비교하여 검토하세요.")

def progress_tracking_page():
    st.title("진도 추적 및 분석")
    st.write(f"총 문제 수: {st.session_state.user['total_questions']}")
    st.write(f"맞은 문제 수: {st.session_state.user['score']}")
    if st.session_state.user['total_questions'] > 0:
        accuracy = (st.session_state.user['score'] / st.session_state.user['total_questions']) * 100
        st.write(f"정확도: {accuracy:.2f}%")
    
    st.subheader("레벨별 진행도")
    for level, progress in st.session_state.user['progress'].items():
        st.write(f"{level}: {progress * 10}%")
        st.progress(progress / 10)
    
    st.subheader("학습 분석")
    st.write("1. 가장 많이 틀린 유형의 문제를 더 연습하세요.")
    st.write("2. 정확도가 80% 이상이면 다음 레벨에 도전해보세요.")
    st.write("3. 꾸준한 학습이 중요합니다. 매일 조금씩 풀어보세요.")

def main():
    st.sidebar.title("MathGate - 수학 학습 플랫폼")

    # 사용자 이름 입력
    if not st.session_state.user['name']:
        st.session_state.user['name'] = st.sidebar.text_input("이름을 입력하세요:")

    if st.session_state.user['name']:
        st.sidebar.write(f"안녕하세요, {st.session_state.user['name']}님!")
        
        # 메인 메뉴
        menu = st.sidebar.radio(
            "메뉴를 선택하세요",
            ["홈", "레벨별 문제", "학습 시스템", "포인트", "피드백 및 설명", "진도 추적"]
        )

        if menu == "홈":
            st.title("MathGate에 오신 것을 환영합니다!")
            st.write("왼쪽 사이드바에서 원하는 메뉴를 선택하세요.")
            st.write(f"현재 레벨: {st.session_state.user['level']}")
            st.write(f"총 점수: {st.session_state.user['score']}")
            st.write(f"포인트: {st.session_state.user['points']}")

        elif menu == "레벨별 문제":
            level_problems_page()

        elif menu == "학습 시스템":
            learning_system_page()

        elif menu == "포인트":
            point_system_page()

        elif menu == "피드백 및 설명":
            feedback_page()

        elif menu == "진도 추적":
            progress_tracking_page()

if __name__ == "__main__":
    main()
