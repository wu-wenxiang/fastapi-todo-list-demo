import logging
import random
import threading
import time

logging.basicConfig(
    format="%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def listen_service(namespace, lock):
    while True:
        logging.info(f"listen_service: begin listen {namespace}")
        time.sleep(random.randint(1, 5))


def main():
    namespaces = ["1", "2"]
    lock = threading.Lock()
    for namespace in namespaces:
        thread = threading.Thread(
            target=listen_service,
            name="listen_service",
            kwargs={"namespace": namespace, "lock": lock},
            daemon=True,
        )
        thread.start()

    while True:
        time.sleep(1)


# 不能使用异步io，因为stream会阻塞
if __name__ == "__main__":
    main()
