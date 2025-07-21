from PIL import Image
from pipeline import run_inference

if __name__ == "__main__":
    file_path = "/sources/test_data/ml_cv_example.jpg"
    question = "Give me the key experience and skill set of my resume."

    with open(file_path, "rb") as f:

        class DummyFile:
            async def read(self):
                return f.read()

        dummy_file = DummyFile()

        import asyncio

        result = asyncio.run(run_inference(dummy_file, question))

        print("\n🧾 결과:")
        print(result)
