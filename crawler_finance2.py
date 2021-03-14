import urllib

import urllib.request
import time

 

service_root = 'http://quotes.money.163.com/service/'

# 'zcfzb', 'lrb', 'xjllb',
table_type_names = ['zycwzb']

code_prefixes = ['600', '601', '603', '000', '001', '002', '300']

for table_name in table_type_names:

    for prefix in code_prefixes:

        for i in range(0, 1000):
            time.sleep(1)

            code = str(i).zfill(3)

            service_url = service_root + table_name + "_" + prefix + code + ".html"
            path = "C:/Users/cesarlu/Desktop/Cesar/temp/hackthon/" + table_name + "_" + prefix + code + ".csv"

            try:

                urllib.request.urlretrieve(service_url, path, None)
                print('successfully retrieved url:' + service_url)

            except Exception as e:

                print('failed to retrieve url:' + service_url)
