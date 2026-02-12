import requests
import json
import threading
import time
from byte import Encrypt_ID, encrypt_api

# Owner: @senkucodex
# modified By : @BLACK666FF

def load_accounts():
    try:
       
        with open("account_IND.json", "r") as file:
            accounts = json.load(file)
        return accounts
    except Exception as e:
        print(f"Error loading accounts: {e}")
        return []

def get_token(uid, password):
    try:
        url = f"https://kallu-access-to-jwt.vercel.app/token?uid={uid}&password={password}"
        response = requests.get(url, timeout=15)
        data = response.json()
        token = data.get('token')
        return token
    except Exception as e:
        print(f"Error getting token for UID {uid}: {e}")
        return get_token(uid, password)

def send_friend_request(target_uid, token, results, account_uid):
    try:
        encrypted_id = Encrypt_ID(target_uid)
        payload = f"08a7c4839f1e10{encrypted_id}1801"
        encrypted_payload = encrypt_api(payload)

        url = "https://client.ind.freefiremobile.com/RequestAddingFriend"
        headers = {
            "Expect": "100-continue",
            "Authorization": f"Bearer {token}",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB52",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "16",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-N975F Build/PI)",
            "Host": "clientbp.ggblueshark.com",
            "Connection": "close",
            "Accept-Encoding": "gzip, deflate, br"
        }

        response = requests.post(url, headers=headers, data=bytes.fromhex(encrypted_payload))

        if response.status_code == 200:
            print(f"✓ Success from UID: {account_uid}")
            results["success"] += 1
        else:
            print(f"✗ Failed from UID: {account_uid} - Status: {response.status_code} : {response.content}")
            results["failed"] += 1
            
    except Exception as e:
        print(f"✗ Error from UID: {account_uid} - {e}")
        results["failed"] += 1

def process_account(account, target_uid, results, delay=0):
  
    if delay > 0:
        time.sleep(delay)
    
    uid = account["uid"]
    password = account["password"]
    
    print(f"Processing account UID: {uid}")
    
    
    token = get_token(uid, password)
    
    if token:
       
        send_friend_request(target_uid, token, results, uid)
    else:
        print(f"✗ Failed to get token for UID: {uid}")
        results["failed"] += 1

def main():
   
    accounts = load_accounts()
    
    if not accounts:
        print("No accounts found in account_IND.json")
        return
    
    print(f"Loaded {len(accounts)} accounts")
    
  
    target_uid = input("Enter UID To Spam Friend Request: ")
    
   
    results = {"success": 0, "failed": 0}
    
    
   
    choice = "2"
    
    if choice == "2":
        
        threads = []
        thread_delay = 0.1  
        
        for i, account in enumerate(accounts):
         
            thread = threading.Thread(
                target=process_account,
                args=(account, target_uid, results, i * thread_delay)
            )
            threads.append(thread)
            thread.start()
        
    
        for thread in threads:
            thread.join()
            
    else:
     
        for account in accounts:
            process_account(account, target_uid, results)
         
            time.sleep(0.5)
    
  
    print("\n" + "="*50)
    print("FRIEND REQUEST SENDING COMPLETED")
    print("="*50)
    print(f"Total Accounts: {len(accounts)}")
    print(f"Successful Requests: {results['success']}")
    print(f"Failed Requests: {results['failed']}")
    print("="*50)

if __name__ == "__main__":
    
    main()