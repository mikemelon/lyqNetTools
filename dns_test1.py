import dns.resolver

def dns_query(domain, type):
    print(type + "记录：")
    try:
        dnsquery = dns.resolver.resolve(domain, type)
        for i in dnsquery.response.answer:
            for j in i:
                print(j)
    except dns.resolver.NoAnswer:
        print(domain+" DNS未响应！")
        print('-' * 20)


domain = "baidu.com"
domain_A = "mail." + domain
dns_query(domain, "MX")
dns_query(domain_A, 'A')
dns_query(domain, 'TXT')
dns_query(domain, 'NS')