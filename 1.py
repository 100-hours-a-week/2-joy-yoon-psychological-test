import openai

openai.api_key = 'API_KEY'

#줄바꿈
def line_change(text):
  sentences = text.split('. ')
  formatted_text = '\n'.join([sentences.strip() for sentences in sentences])
  return formatted_text

#프롬포트
def set_inrto (topic):

  prompt = f''' "{topic}" 라는 주제를 바탕으로 심리테스트에 대한 소개 작성. '''


  response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo-0125',
    messages = [
        {"role": "system", "content": '너는 스토리텔링 형식 심리테스트를 제공해야해.'},
        {"role": "user", "content": prompt}],
        max_tokens=250
    )
  return response.choices[0].message['content']


#질문
def set_question (topic, previous_choice=None):

  prompt = f''' "{topic}" 라는 주제를 바탕으로 스토리텔링 형식으로 심리테스트에 대한 질문 작성. 스토리는 사용자의 이전 선택 : "{previous_choice}"를 기반으로 전개되어야함. 항목은 4개로 이루어져 있는 객관식이어야함.
  1 [항목 1]
  2 [항목 2]
  3 [항목 3]
  4 [항목 4]'''


  response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo-0125',
    messages = [
        {"role": "system", "content": '너는 스토리텔링 형식 심리테스트를 제공해야해.'},
        {"role": "user", "content": prompt}],
        max_tokens=350
    )
  return response.choices[0].message['content']


#최종 테스트 결과
def set_final_result(choices, topic):

  prompt = f''' "{topic}" 에 대한 심리 테스트에서 "{choices}"에 있는 사용자가 선택한 항목을 기반으로 최종 테스트 결과를 세 줄로 제공'''
  response = openai.ChatCompletion.create(
  model = 'gpt-3.5-turbo-0125',
  messages = [
      {"role": "system", "content": '너는 스토리텔링 형식 심리테스트를 제공해야해.'},
      {"role": "user", "content": prompt}],
      max_tokens=400
  )
  return response.choices[0].message['content']



#실행
def run_test():
  print("심리테스트 시작합니다.")
  topic = input('테스트 주제를 입력하세요(ex. 연애, 진로, 성격):')

  print('START')

  #도입부 생성
  intro = set_inrto(topic)
  #줄바꿈
  formatted_response = line_change(intro)
  print(formatted_response)

  num_questions = 4
  choices = []

  for i in range(1, num_questions+1):
    #이전 선택 기반 질문 생성
    previous_choice = choices[-1] if choices else None
    question = set_question(topic, previous_choice)
    #줄바꿈
    formatted_response = line_change(question)
    print(f'\nQ{i}: {formatted_response}\n')

    # 답변
    while True:
      try:
        answer = int(input(f'\nQ{i}에 대한 답변을 선택하세요 (1~4): '))
        if 1 <= answer <= 4:
          break
        else:
          print('잘못된 답변입니다. 다시 시도하세요.')
      except ValueError:
        print('잘못된 답변입니다. 숫자를 입력하세요.')

    #저장
    import time
    choices.append(answer)
    time.sleep(1)

  #최종 결과 생성
  final_result = set_final_result(choices, topic)
  #줄바꿈
  formatted_response = line_change(final_result)

  print("-----------테스트 결과-----------")
  print(formatted_response)
  print("테스트가 종료되었습니다. 감사합니다.")


#최종 실행
if __name__ == '__main__':
  run_test()