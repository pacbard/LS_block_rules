import os
import time
import urllib2

def download_hosts(target_url, urls):
    count_urls = len(urls)
    try:
        print("Downloading and processing "+ str(target_url))
        count = 0
        f_host=urllib2.urlopen(target_url)
        fl =f_host.readlines()
        current_number=-1
        for line in fl:
            line=line.strip()
            line=line.replace("127.0.0.1", "0.0.0.0")
            #print(line)
            if line.startswith('0.0.0.0') and not (line.endswith('0.0.0.0')):
                domain=line.split('0.0.0.0')
                if "localhost" in str(domain[1].strip()) or str(domain[1].strip()) == "local":
                    # Skip all entries with localhost
                    continue
                elif '#' in str(domain[1].strip()):
                    urls[str(str(domain[1].strip()).split('#')[0]).strip()] = 1
                    count += 1
                else:
                    urls[str(str(domain[1]).strip()).strip()] = 1
                    count += 1
    except Exception as e:
        print(str(e))
    print(str(count) + " ("+ str(len(urls)-count_urls)  +" new) urls processed")
    print(str(len(urls)) +" unique urls in block list")
    return urls

def convert_to_lsrules(urls_to_block):
    output_script='LS_bLock_list'
    output_dir="Rules"
    description='My block list'
    name='LSRules'
    script_number=0
    rule_count=0

    # Open file
    global f
    file_name=output_script+'.lsrules'

    if os.path.exists(os.path.join(os.getcwd(),output_dir)) :
        dir_path=os.path.join(os.getcwd(),output_dir)
        f= open(os.path.join(dir_path,file_name),"w+")
    else:
        try:
            os.makedirs(os.path.join(os.getcwd(),output_dir))
        except OSError as obj:
            error = obj.strerror+os.path.join(os.getcwd(),output_dir)
            print("%d: %s" %(obj.errno,error))
            pass
        dir_path=os.path.join(os.getcwd(),output_dir)
        f= open(os.path.join(dir_path,file_name),"w+")

    begin='{\n'+'    "description" : "'+description+'",\n    "name" : "'+file_name+'",\n    "denied-remote-domains": [\n'
    f.write(begin)

    #Process all urls
    for url in urls_to_block[:-1]:
        #print(url)
        rule_remote_domain='        "'+str(url).strip()+'",\n'
        f.write(rule_remote_domain)

    rule_remote_domain='        "'+str(urls_to_block[-1]).strip()+'"\n'
    f.write(rule_remote_domain)

    end='   ]\n}'
    f.write(end)
    f.close()
    print('Completed, closing the file')
    #quit()

def main():
    hostfiles=[
                'https://block.energized.pro/spark/formats/hosts',
                'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts',
                'https://someonewhocares.org/hosts/',
                'https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0'
              ]
    urls = {}

    for url in hostfiles:
        urls = download_hosts(url, urls)

    urls = list(sorted(urls.keys()))
    convert_to_lsrules(urls)

if __name__== "__main__":
  main()
