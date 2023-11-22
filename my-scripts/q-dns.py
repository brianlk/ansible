
import socket
import sys
import time
import dns.resolver

fqdn="www.emsd.gov.hk"
servers=[socket.gethostbyname("NS7.EMSD.GOV.HK"), socket.gethostbyname("NS8.EMSD.GOV.HK")]

count = 0

while True:
    print(f"Time: {str(time.time())}")
    resolver = dns.resolver.Resolver(configure=False)
    try:
        if count/2 == 0:
            resolver.nameservers = [servers[0]]
        else:
            resolver.nameservers = [servers[1]]
        answer = resolver.resolve(fqdn, "CNAME")
        print(answer.response)
        print("\n")
        time.sleep(10)
        count += 1 
    except Exception as e:
        print(f"Time: {str(time.time())}: {str(e)}")
    finally:
        sys.stdout.flush()
        


