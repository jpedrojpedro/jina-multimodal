from jina import Flow

if __name__ == '__main__':
    f = (
        Flow(port=8080, protocol='http')
        .add(name='encoder', uses='jinahub+docker://CLIPImageEncoder', replicas=2)
        .add(
            name='indexer',
            uses='jinahub+docker://PQLiteIndexer',
            uses_with={'dim': 512},
            shards=2,
        )
    )

    f.to_docker_compose_yaml('docker-compose.yml')
