import json
from multiprocessing import Process, Manager

import requests


def split_list_n_list(origin_list, n):
    if len(origin_list) % n == 0:
        cnt = len(origin_list) // n
    else:
        cnt = len(origin_list) // n + 1

    for i in range(0, n):
        yield origin_list[i * cnt:(i + 1) * cnt]


def get_info(issues: list, pu_number, sort_type, rows_per_page, paper_infos, year_issues):
    cookies = {
        'JSESSIONID': 'vHwxa2Ckp9igWv29X9jxa2tpxTeQRNpi-KGv5gMUJVnJWfZvq4cW!1915905931',
        'ipCheck': '59.64.129.50',
        'ERIGHTS': 'czMaGMwAeGF0DstVKfxxhbooAKzZ6SPsQ*PXfDpDBBmkEUI9BcNY0KYAx3Dx3D-18x2dx2F6nFo4pR4JwBkFFDWWEycQx3Dx3DR2A3Pj5yBobd4hsFZ8HcEAx3Dx3D-gdpPDF74rjhVhbSezWo23Ax3Dx3D-hAF6CbSbyWBiTg9Gw04M9Ax3Dx3D',
        'WLSESSION': '203580044.20480.0000',
        'TS01b03060': '012f3506235d4edc6f6e1d59b84636a664c59adaa6730f807db38e7a94dbb4efb0912f2c2b3b66c8a04e1b3d7e24cb7e9e9b2d57bc',
        'fp': '3f8d64e2059bbc4a4783f33297176995',
        'ipList': '59.64.129.50',
        '__gads': 'ID=8959bc003e82ba46:T=1675866369:S=ALNI_MZ40-S03YhoFPiW8ZKXbqLox-MKeA',
        '__gpi': 'UID=00000bbe5fd75412:T=1675866369:RT=1675866369:S=ALNI_Mb6PQj8ukgwGYPtcuDAjDIaGgzq_A',
        'AMCVS_8E929CC25A1FB2B30A495C97%40AdobeOrg': '1',
        's_ecid': 'MCMID%7C07450342967836011380554529742981763782',
        's_cc': 'true',
        'AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg': '1687686476%7CMCIDTS%7C19397%7CMCMID%7C07450342967836011380554529742981763782%7CMCAAMLH-1676471176%7C11%7CMCAAMB-1676471176%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1675873576s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-19404%7CvVersion%7C3.0.0',
        'cookieconsent_status': 'dismiss',
        'utag_main': 'v_id:0186316b84e300029a7bea2a6aa805075008306d009dc$_sn:1$_se:2$_ss:0$_st:1675868210454$ses_id:1675866375396%3Bexp-session$_pn:2%3Bexp-session$vapi_domain:ieee.org',
        'xpluserinfo': 'eyJpc0luc3QiOiJ0cnVlIiwiaW5zdE5hbWUiOiJCRUlKSU5HIFVOSVZFUlNJVFkgT0YgUE9TVCBBTkQgVEVMRUNPTSIsInByb2R1Y3RzIjoiTUNTWU5USDF8TUNTWU5USDN8TUNTWU5USDZ8TUNTWU5USDJ8TUNTWU5USDV8TUNTWU5USDR8TUNTWU5USDd8TUNTWU5USDl8Tk9XOjIwMDQ6MjAxOXxXSUxFWVRFTEVDT006MjAwNToyMDE5fElCTToxODcyOjIwMjB8TUNTWU5USDh8SUVMfFZERXxOT0tJQSBCRUxMIExBQlN8In0=',
        'seqId': '7864',
        'TSaeeec342027': '080f8ceb8aab20002fd3bf313fd3e977d44bce0c7cbe7a43cdb707a2c1682ed267dba391d99ef59f089206780d11300056b7763d4defa78594a3e96c37eba39364296e624fd024d0ae65cc806893f0fe9be286cd0e3ffaaacd209a80fc74a598',
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://ieeexplore.ieee.org',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    base_url = 'https://ieeexplore.ieee.org'
    for issue in issues:
        is_number = issue['issue_number']
        current_year = issue['year']
        print('Begin is_number {}, year is {}'.format(is_number, current_year))
        json_data = {
            'isnumber': is_number,
            'punumber': pu_number,
            'sortType': sort_type,
            'rowsPerPage': str(rows_per_page),
            'pageNumber': '1',
        }
        response = requests.post(
            f'https://ieeexplore.ieee.org/rest/search/pub/{pu_number}/issue/{is_number}/toc',
            cookies=cookies,
            headers=headers,
            json=json_data,
        ).json()
        total_pages = response['totalPages']
        for i in range(total_pages):
            json_data['pageNumber'] = str(i + 1)
            response = requests.post(
                f'https://ieeexplore.ieee.org/rest/search/pub/{pu_number}/issue/{is_number}/toc',
                cookies=cookies,
                headers=headers,
                json=json_data,
            ).json()
            records = response['records']
            for record in records:
                article_title = record['articleTitle']
                download_count = record['downloadCount']
                paper_link = '{}{}'.format(base_url, record['htmlLink'])
                pdf_link = '{}{}'.format(base_url, record['pdfLink'])
                publication_title = record['publicationTitle']
                start_page = record['startPage']
                end_page = record['endPage']
                pages = f'{start_page}_{end_page}'
                article_content_type = record['articleContentType']
                authors = []
                volume = record['volume']
                this_issue = record['issue']
                # author_base_url = "https://ieeexplore.ieee.org/rest/author/{}"
                if 'authors' not in record:
                    # print(f'Skip {article_title}')
                    continue
                # for author in record['authors']:
                #     author_info = requests.get(author_base_url.format(author['id']), cookies=cookies,
                #                                headers=headers).json()[0]
                #     author_affiliation = 'Known'
                #     if 'currentAffiliation' in author_info:
                #         author_affiliation = author_info['currentAffiliation']
                #     authors.append({'name': author['searchablePreferredName'],
                #                     'author_links': 'https://ieeexplore.ieee.org/author/{}'.format(author['id']),
                #                     'author_affiliation': author_affiliation})

                doi = record['doi']
                publication_date = record['publicationDate']
                text = requests.get('https://ieeexplore.ieee.org/document/{}'.format(record['articleNumber']),
                                    cookies=cookies, headers=headers).text
                begin = 'xplGlobal.document.metadata='
                end = '};'
                begin_idx = text.find(begin) + len(begin)
                text = text[begin_idx:]
                end_idx = text.find(end)
                metadata = text[:end_idx + 1].strip()
                metadata_json = json.loads(metadata)
                abstract = ''
                author_keyword = ''
                if metadata_json['sections']['abstract'] == 'true':
                    abstract = metadata_json['abstract']
                if metadata_json['sections']['keywords'] == 'true':
                    for j in range(len(metadata_json['keywords'])):
                        if metadata_json['keywords'][j]['type'].strip() == 'Author Keywords':
                            author_keyword = metadata_json['keywords'][j]['kwd']
                            break
                if metadata_json['sections']['authors'] == 'true':
                    for author in metadata_json['authors']:
                        author_affiliation = 'Known'
                        if 'affiliation' in author and len(author['affiliation']) > 0:
                            author_affiliation = author['affiliation'][0]
                        authors.append({'name': author['name'],
                                        'author_links': 'https://ieeexplore.ieee.org/author/{}'.format(author['id']),
                                        'author_affiliation': author_affiliation})
                paper_infos.append({
                    'article_title': article_title,
                    'doi': doi,
                    'publication_date': publication_date,
                    'abstract': abstract,
                    'start_page': start_page,
                    'end_page': end_page,
                    'pages': pages,
                    'download_count': download_count,
                    'article_content_type': article_content_type,
                    'publication_title': publication_title,
                    'paper_link': paper_link,
                    'pdf_link': pdf_link,
                    'volume': volume,
                    'issue': this_issue,
                    'authors': authors,
                    'author_keyword': author_keyword
                })
        year_issues[current_year] = year_issues[current_year] - 1
        print('Finish is_number{}, year is {}, last{}'.format(is_number, current_year, year_issues[current_year]))


if __name__ == '__main__':
    pu_number = '7274857'
    rows_per_page = 100
    sort_type = 'vol-only-seq'
    cookies = {
        'JSESSIONID': 'vHwxa2Ckp9igWv29X9jxa2tpxTeQRNpi-KGv5gMUJVnJWfZvq4cW!1915905931',
        'ipCheck': '59.64.129.50',
        'ERIGHTS': 'czMaGMwAeGF0DstVKfxxhbooAKzZ6SPsQ*PXfDpDBBmkEUI9BcNY0KYAx3Dx3D-18x2dx2F6nFo4pR4JwBkFFDWWEycQx3Dx3DR2A3Pj5yBobd4hsFZ8HcEAx3Dx3D-gdpPDF74rjhVhbSezWo23Ax3Dx3D-hAF6CbSbyWBiTg9Gw04M9Ax3Dx3D',
        'WLSESSION': '203580044.20480.0000',
        'TS01b03060': '012f3506235d4edc6f6e1d59b84636a664c59adaa6730f807db38e7a94dbb4efb0912f2c2b3b66c8a04e1b3d7e24cb7e9e9b2d57bc',
        'fp': '3f8d64e2059bbc4a4783f33297176995',
        'ipList': '59.64.129.50',
        '__gads': 'ID=8959bc003e82ba46:T=1675866369:S=ALNI_MZ40-S03YhoFPiW8ZKXbqLox-MKeA',
        '__gpi': 'UID=00000bbe5fd75412:T=1675866369:RT=1675866369:S=ALNI_Mb6PQj8ukgwGYPtcuDAjDIaGgzq_A',
        'AMCVS_8E929CC25A1FB2B30A495C97%40AdobeOrg': '1',
        's_ecid': 'MCMID%7C07450342967836011380554529742981763782',
        's_cc': 'true',
        'AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg': '1687686476%7CMCIDTS%7C19397%7CMCMID%7C07450342967836011380554529742981763782%7CMCAAMLH-1676471176%7C11%7CMCAAMB-1676471176%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1675873576s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-19404%7CvVersion%7C3.0.0',
        'cookieconsent_status': 'dismiss',
        'utag_main': 'v_id:0186316b84e300029a7bea2a6aa805075008306d009dc$_sn:1$_se:2$_ss:0$_st:1675868210454$ses_id:1675866375396%3Bexp-session$_pn:2%3Bexp-session$vapi_domain:ieee.org',
        'xpluserinfo': 'eyJpc0luc3QiOiJ0cnVlIiwiaW5zdE5hbWUiOiJCRUlKSU5HIFVOSVZFUlNJVFkgT0YgUE9TVCBBTkQgVEVMRUNPTSIsInByb2R1Y3RzIjoiTUNTWU5USDF8TUNTWU5USDN8TUNTWU5USDZ8TUNTWU5USDJ8TUNTWU5USDV8TUNTWU5USDR8TUNTWU5USDd8TUNTWU5USDl8Tk9XOjIwMDQ6MjAxOXxXSUxFWVRFTEVDT006MjAwNToyMDE5fElCTToxODcyOjIwMjB8TUNTWU5USDh8SUVMfFZERXxOT0tJQSBCRUxMIExBQlN8In0=',
        'seqId': '7864',
        'TSaeeec342027': '080f8ceb8aab20002fd3bf313fd3e977d44bce0c7cbe7a43cdb707a2c1682ed267dba391d99ef59f089206780d11300056b7763d4defa78594a3e96c37eba39364296e624fd024d0ae65cc806893f0fe9be286cd0e3ffaaacd209a80fc74a598',
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://ieeexplore.ieee.org',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    issues_base_url = f'https://ieeexplore.ieee.org/rest/publication/{pu_number}/regular-issues'
    all_issues = requests.get(issues_base_url, cookies=cookies, headers=headers).json()
    all_issue = []
    all_years = []
    year_issues = Manager().dict()
    paper_infos = Manager().list()
    for decade in all_issues['issuelist']:
        for year in decade['years']:
            all_years.append(year['year'])
            year_issues[year['year']] = len(year['issues'])
            for issue in year['issues']:
                all_issue.append({'issue_number': issue['issueNumber'],
                                  'year': year['year']})
    print(f'Begin acquire the all papers info. Min year is {min(all_years)}, max year is {max(all_years)}')
    thread_num = 16
    issue_list = split_list_n_list(all_issue, thread_num)
    threads = []
    for iss in issue_list:
        thread = Process(target=get_info,
                         args=(iss, pu_number, sort_type, rows_per_page, paper_infos, year_issues))
        threads.append(thread)
        thread.start()
    for current_thread in threads:
        current_thread.join()
    with open(f'{pu_number}.json', 'w', encoding='utf8') as f2:
        json.dump(list(paper_infos), f2, ensure_ascii=False, indent=2)
