import os
import webbrowser
from pathlib import Path
from docarray import DocumentArray
from jina import Flow
from jina.importer import ImportExtensions
from jina.logging.predefined import default_logger
# from jina.logging.profile import ProgressBar


multimodal_folder = Path.cwd()


def run(skip_indexing=True):
    """
    Execute the multimodal example.
    """
    with ImportExtensions(
        required=True,
        help_text='this multimodal demo requires Pytorch and Transformers to be installed, '
        'if you haven\'t, please do `pip install jina[torch,transformers]`',
    ):
        import torch
        import torchvision
        import transformers

        assert [
            torch,
            transformers,
            torchvision,
        ]

    # this envs are referred in index and query flow YAMLs
    os.environ['HW_WORKDIR'] = str(Path.cwd().absolute())
    os.environ['PY_MODULE'] = str((Path.cwd() / "my_executors.py").absolute())

    if not skip_indexing:
        # index it!
        f = Flow.load_config('flow-index.yml')

        with f, open(multimodal_folder / "input" / "electronics_20220615.csv", newline='') as fp:
            f.index(inputs=DocumentArray.from_csv(fp), request_size=10, show_progress=True)
            f.post(on='/dump', target_executor='textIndexer')
            f.post(on='/dump', target_executor='imageIndexer')
            f.post(on='/dump', target_executor='keyValueIndexer')

    # search it!
    f = Flow.load_config('flow-search.yml')
    # switch to HTTP gateway
    f.protocol = 'http'
    f.port = 8080

    url_html_path = 'file://' + str((Path.cwd() / "static" / "index.html").absolute())
    with f:
        try:
            webbrowser.open(url_html_path, new=2)
        except:
            pass  # intentional pass, browser support isn't cross-platform
        finally:
            default_logger.info(
                f'You should see a demo page opened in your browser, '
                f'if not, you may open {url_html_path} manually'
            )
        # this block() is necessary to keep the system up
        f.block()


if __name__ == '__main__':
    run()
