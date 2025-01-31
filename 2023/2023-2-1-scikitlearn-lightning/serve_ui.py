# !python -m pip install -U scikit-learn
import gradio as gr
import lightning as L
from joblib import load
from lightning.app.components.serve import ServeGradio
from lightning.app.storage import Drive
from PIL import Image

CLASS_NAMES = ["Setosa", "Versicolor", "Virginica"]
FLOWERS = ["setosa.jpeg", "versicolor.jpeg", "virginica.jpeg"]


class SKLearnServeUI(ServeGradio):
    inputs = [
        gr.Number(label="Sepal Width"),
        gr.Number(label="Sepal Length"),
        gr.Number(label="Petal Width"),
        gr.Number(label="Petal Length"),
    ]
    outputs = [gr.Text(), gr.Image(label="Predicted Iris")]
    examples = [[6.1, 3. , 4.6, 1.4], [4.6, 3.4, 1.4, 0.3], [6.3, 2.9, 5.6, 1.8]]

    def __init__(self):
        super().__init__(self)
        # cloud persistable storage for model checkpoint
        self.model_storage = Drive("lit://checkpoints")

    def build_model(self):
        self.model_storage.get("model.joblib")
        return load("model.joblib")

    def predict(self, sepal_width, sepal_length, petal_width, petal_length):
        class_idx = self.model.predict(
            [[sepal_width, sepal_length, petal_width, petal_length]]
        )[0]
        print(class_idx)
        return CLASS_NAMES[class_idx], Image.open("flowers/" + FLOWERS[class_idx])


component = SKLearnServeUI()
app = L.LightningApp(component)
