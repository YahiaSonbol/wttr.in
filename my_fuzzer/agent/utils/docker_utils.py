import os
import docker
from ..core.config import FuzzerConfig


def build_image(
    client: docker.DockerClient, 
    config: FuzzerConfig,
) -> None:
    print(f"[build] Building Docker image {config.image}")
    _, logs = client.images.build(path=str(config.repo_root), tag=config.image, rm=True)
    for event in logs:
        stream = event.get("stream")
        if stream:
            line = stream.strip()
            if line:
                print(f"[build] {line}")


def ensure_image(
    client: docker.DockerClient,
    config: FuzzerConfig,
) -> None:
    try:
        client.images.get(config.image)
        return
    except docker.errors.ImageNotFound:
        print(f"[build] Local image {config.image} was not found. Building it now.")
        build_image(client, config)


def start_container(
    client: docker.DockerClient,
    config: FuzzerConfig,
    iteration: int,
) -> docker.models.containers.Container:
    container_name = f"wttr-fuzzer-{os.getpid()}-{iteration}"
    print(f"[docker] Starting container {container_name}")
    ensure_image(client, config)

    return client.containers.run(
        config.image,
        name=container_name,
        detach=True,
        ports={f"{config.container_port}/tcp": ("127.0.0.1", config.host_port)},
        volumes={str(config.cache_dir.resolve()): {"bind": "/app/cache", "mode": "rw"}},
        environment={"COVERAGE_FILE": "/app/cache/.coverage"},
    )

def stop_and_collect_container(
    container: docker.models.containers.Container,
    timeout_seconds: int,
) -> tuple[int | None, str]:
    try:
        container.stop(timeout=timeout_seconds)
    finally:
        logs = container.logs(tail=400).decode("utf-8", errors="replace")
        container.reload()
        exit_code = container.attrs.get("State", {}).get("ExitCode")
        container.remove(force=True)

    return exit_code, logs
