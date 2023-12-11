from config import DATA_PATH
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt



class MemberCountModel(Model):
    __path = DATA_PATH['member_count']
    __columns = ['join_date', 'category', 'count']
    
    def __init__(self, units: int, length: int, input_dim: int):
        super(MemberCountModel, self).__init__()
        self.data = None
        self.sequences = None
        self.units = units
        self.length = length
        self.input_dim = input_dim
        self.lstm_layer = LSTM()
        self.dense = Dense()
        
    
    def read_data(self):
        self.data = pd.read_parquet(DATA_PATH['member_count'])
        return self
    
    def create_sequences(self):
        sequences = []
        for i in range(len(self.data) - self.length):
            sequences.append(self.data[i:i + self.length])
        self.sequences = np.array(sequences)
        return self
    
    def process_data(self):
        X = self.data[:, :-1]
        X = X.reshape(-1, self.length - 1, 1)
        y = self.data[:, -1]
        return X, y
    
    def lstm_model(self):
        pass
    
    def predict_future(self):
        X, y = self.process_data()
        future_seq = X[-1].copy()
        predictions = []
        
        for _ in range(10):
            prediction = model.predict(future_seq.reshape(1, seq_length - 1, 1), verbose=False)
            predictions.append(prediction[0, 0])
            future_seq = np.roll(future_seq, -1)
            future_seq[-1] = prediction[0, 0]
        
        return predictions











# 데이터를 pandas DataFrame으로 불러오기
data = pd.DataFrame({
    'order': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38],
    'join_number': [13126, 5768, 4473, 3060, 2291, 8790, 4797, 1960, 1890, 2983, 2853, 2704, 4714, 9104, 8791, 7141, 10384, 11183, 8773, 8736, 8336, 9877, 9425, 9997, 9523, 6847, 15090, 17016, 16064, 16563, 16563, 16563, 18444, 18521, 16777, 17072, 17491, 16666]
})

# 데이터 정규화 (옵션)
# data['join_number'] = (data['join_number'] - data['join_number'].mean()) / data['join_number'].std()

# 시계열 데이터를 시퀀스로 변환
def create_sequences(data, seq_length):
    sequences = []
    for i in range(len(data) - seq_length):
        sequences.append(data[i:i + seq_length])
    return np.array(sequences)

# 시퀀스 길이 설정
seq_length = 12

# 데이터를 시퀀스로 변환
sequences = create_sequences(data['join_number'].values, seq_length)

# 입력 데이터(X)와 타깃 데이터(y) 분리
X = sequences[:, :-1]
y = sequences[:, -1]

# 데이터 형태 변환 (샘플 수, 시퀀스 길이, 1)
X = X.reshape(-1, seq_length - 1, 1)

# 모델 정의
model = Sequential()
model.add(LSTM(units=48, activation='relu', input_shape=(seq_length - 1, 1)))
model.add(Dense(24, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# 모델 훈련
model.fit(X, y, epochs=100, batch_size=16, verbose=False)

# 미래 예측
future_seq = X[-1].copy()
predictions = []
for i in range(10):
    prediction = model.predict(future_seq.reshape(1, seq_length - 1, 1), verbose=False)
    predictions.append(prediction[0, 0])
    future_seq = np.roll(future_seq, -1)
    future_seq[-1] = prediction[0, 0]

# 예측 결과 그래프
plt.plot(data['order'], data['join_number'], label='True Data')
plt.plot(np.arange(len(data['join_number']), len(data['join_number']) + len(predictions)), predictions, label='Predictions')
plt.legend()
plt.show()


model2 = tf.keras.models.load_model(r'result\예측치.keras')