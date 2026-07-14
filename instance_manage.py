import subprocess, sys
counter = int(sys.argv[1]) - 1

while True:
    with open('logfile.txt', 'w') as log_file:
        log_file.write("")

    def print_s(text):
        print(text)
        with open('logfile.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(text)

    with open('status.txt', 'w') as f:
        f.write('')

    with open('comments_bool.txt', 'w') as f:
        f.write('false')
    while True:
        subprocess.Popen(['python.exe', "auto_reply_chrome.py", str(counter)])
        while True:
            with open('comments_bool.txt', 'r') as f:
                comments_bool = f.read()

            if 'true' in comments_bool:
                with open('comments_bool.txt', 'w') as f:
                    f.write('false')
                break
   
        if counter == 4:
            break
        else:
            counter += 1
    counter = 0

    print_s('\n[+] Cycle Done')
