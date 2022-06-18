import json
import random
import base64
import pandas as pd
from pathlib import Path


input_path = Path.cwd() / "input"
images_path = Path.cwd() / "images"


def transform_image(caption, image_name):
    with open(f"{images_path}/{image_name}", "rb") as open_file:
        byte_content = open_file.read()
        base64_bytes = base64.b64encode(byte_content)
        base64_string = base64_bytes.decode('ascii')
        header = "data:image/jpeg;base64"
        uri = f"{header},{str(base64_string)}"
        return {"uri": uri, "text": caption}


def main(filename="electronics_20220615.csv", k=50):
    result = []
    df = pd.read_csv(input_path / filename)
    print(f"dataframe: {df.shape}")
    positions = [random.randint(0, df.shape[0]) for _ in range(k)]
    for pos in positions:
        row = df.iloc[pos]
        aux = transform_image(row["caption"], row["image"])
        result.append(aux)
    return json.dump(result, open(f"{input_path}/sample.json", "w"))


if __name__ == '__main__':
    main()
