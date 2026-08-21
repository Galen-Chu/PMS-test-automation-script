from pathlib import Path
import pickle
import os
import numpy as np
import cv2
from tensorflow import keras  # pylint: disable=no-name-in-module,import-error
from tensorflow.keras import layers  # pylint: disable=no-name-in-module,import-error
from sklearn.model_selection import train_test_split


class CaptchaTrainer:
    def __init__(self, img_width=160, img_height=60, max_length=4):
        self.img_width = img_width
        self.img_height = img_height
        self.max_length = max_length
        self.characters = set()
        self.char_to_num = {}
        self.num_to_char = {}

    def load_data(self, data_path):  # 修復逗號位置
        """載入訓練資料"""
        images = []
        labels = []

        for filename in os.listdir(data_path):
            if filename.endswith((".png", ".jpg", ".jpeg")):
                # 檔名為標籤
                label = filename.split(".")[0]
                img_path = os.path.join(data_path, filename)

                # 讀取並預處理圖片
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                img = cv2.resize(img, (self.img_width, self.img_height))
                img = img.astype(np.float32) / 255.0

                images.append(img)
                labels.append(label)

                # 收集所有字符
                for char in label:
                    self.characters.add(char)

        return np.array(images), labels

    def create_char_mappings(self):
        """建立字符映射"""
        self.characters = sorted(list(self.characters))
        self.char_to_num = {char: idx for idx, char in enumerate(self.characters)}
        self.num_to_char = dict(enumerate(self.characters))

    def encode_labels(self, labels):
        """將標籤編碼為數字"""
        encoded_labels = []
        for label in labels:
            encoded_label = []
            for char in label:
                encoded_label.append(self.char_to_num[char])
            # 填充到固定長度
            while len(encoded_label) < self.max_length:
                encoded_label.append(len(self.characters))  # 使用特殊token填充
            encoded_labels.append(encoded_label)
        return np.array(encoded_labels)

    def build_model(self):
        """建立CNN模型"""
        input_img = layers.Input(shape=(self.img_height, self.img_width, 1))

        # CNN層
        x = layers.Conv2D(32, (3, 3), activation="relu")(input_img)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Conv2D(64, (3, 3), activation="relu")(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Conv2D(128, (3, 3), activation="relu")(x)
        x = layers.MaxPooling2D((2, 2))(x)

        # 展平
        x = layers.Flatten()(x)
        x = layers.Dropout(0.5)(x)

        # 為每個位置建立輸出層
        outputs = []
        for i in range(self.max_length):
            output = layers.Dense(len(self.characters) + 1, activation="softmax", name=f"char_{i}")(
                x
            )
            outputs.append(output)

        model = keras.Model(inputs=input_img, outputs=outputs)
        return model

    def _prepare_all_data(self, data_path, validation_split):
        """準備所有訓練資料和標籤字典"""
        # 載入和預處理資料
        images, labels = self.load_data(data_path)
        self.create_char_mappings()

        # 重新調整圖片維度 - 修復參數傳遞問題
        images = images.reshape((-1, self.img_height, self.img_width, 1))

        # 編碼標籤
        encoded_labels = self.encode_labels(labels)

        # 分割資料
        x_train, x_test, y_train_encoded, y_test_encoded = train_test_split(
            images, encoded_labels, test_size=validation_split, random_state=42
        )

        # 準備多輸出標籤字典
        y_train_dict = {f"char_{i}": y_train_encoded[:, i] for i in range(self.max_length)}
        y_test_dict = {f"char_{i}": y_test_encoded[:, i] for i in range(self.max_length)}

        return x_train, x_test, y_train_dict, y_test_dict

    def train_model(self, data_path, epochs=50, batch_size=32, validation_split=0.2):
        """訓練模型"""
        # 準備所有資料
        x_train, x_test, y_train_dict, y_test_dict = self._prepare_all_data(
            data_path, validation_split
        )

        # 建立和編譯模型
        model = self.build_model()

        loss_dict = {f"char_{i}": "sparse_categorical_crossentropy" for i in range(self.max_length)}
        metrics_dict = {f"char_{i}": ["accuracy"] for i in range(self.max_length)}

        model.compile(optimizer="adam", loss=loss_dict, metrics=metrics_dict)

        # 訓練
        history = model.fit(
            x_train,
            y_train_dict,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(x_test, y_test_dict),
            verbose=1,
        )

        # 儲存模型和映射
        model.save("captcha_model.keras")

        with open("char_mappings.pkl", "wb") as f:
            pickle.dump(
                {
                    "char_to_num": self.char_to_num,
                    "num_to_char": self.num_to_char,
                    "characters": self.characters,
                },
                f,
            )

        return model, history

    def predict_captcha(self, image_path):
        # 載入模型
        model_path = (
            Path(__file__).resolve().parent.parent.parent / "ml-models" / "captcha_model.keras"
        )
        model = keras.models.load_model(model_path)

        # 載入字符映射
        pickle_path = (
            Path(__file__).resolve().parent.parent.parent / "ml-models" / "char_mappings.pkl"
        )
        with open(pickle_path, "rb") as f:
            mappings = pickle.load(f)
            self.char_to_num = mappings["char_to_num"]
            self.num_to_char = mappings["num_to_char"]
            self.characters = mappings["characters"]

        # 預測驗證碼
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (self.img_width, self.img_height))
        img = img.astype(np.float32) / 255.0
        img = img.reshape((1, self.img_height, self.img_width, 1))  # 修復參數傳遞問題

        predictions = model.predict(img)

        predicted_text = ""
        for i in range(self.max_length):
            pred_char_idx = np.argmax(predictions[i])
            if pred_char_idx < len(self.characters):
                predicted_text += self.num_to_char[pred_char_idx]

        return predicted_text
