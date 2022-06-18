from jina import Flow
from pathlib import Path


if __name__ == '__main__':
    multimodal_folder = Path.cwd()
    indexing_pipeline = multimodal_folder / "flow-index.yml"
    f = Flow.load_config(str(indexing_pipeline.absolute()))
    f.plot("index-flow.jpeg")
