import streamlit as st
import time

st.title('Streamlit 超入門')

st.write('ProgressBar の表示')
'Start'

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iteration {i}')
    bar.progress(i)
    time.sleep(0.01)
'Done!!!'

left_column, right_column = st.beta_columns(2)

button = left_column.button('右カラムに文字を表示')
if button:
    right_column.write('ここは右カラムです')

expander = st.beta_expander('問い合わせ')
expander.write('問い合わせ内容を書く')

# text = st.text_input('あなたの趣味を教えてください。')
# condition = st.slider('あなたの今の調子は？', 0, 100, 50, 10)

# 'あなたの趣味：', text
# 'コンディション', condition

# if st.checkbox('Show Image'):
#     img = Image.open('./streamlitSample/sample.jpg')
#     st.image(img, caption='Houl', use_column_width=True)


