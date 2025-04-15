import time
import threading

timeout = 3 # 超时的阈值是3秒
is_running = True

def check_timeout():
    global is_running
    start_time = time.time()
    while is_running:
        if time.time() - start_time >= timeout:
            is_running = False
            raise TimeoutError("Loop timeout")
    time.sleep(0.1)

def main():
    global is_running

    t = threading.Thread(target=check_timeout) 
    t.daemon = True
    t.start()

    for i in range(10):
        try:
            is_running = True
            # loop body
            if i == 6:
                time.sleep(6) # 更新is_running
                print(i)
            else:
                time.sleep(1)
                print(i)
        except TimeoutError:
            print(f"round {i} timeout")
            continue

    t.join()


if __name__ == "__main__":
    main()