#!/usr/bin/env python3
import os
import re

# 已知的百度百科链接（微信百科和百度百科）
baidu_links = {
    'yuan-long-ping': 'https://baike.weixin.qq.com/v88497.htm',
    'kobe-bryant': 'https://baike.weixin.qq.com/v226587.htm',
    'steve-jobs': 'https://baike.weixin.qq.com/v674008.htm',
    'pele': 'https://m.baike.com/wiki/%E8%B4%9D%E5%88%A9/20042878',
    'inamori-kazuo': 'https://m.baike.com/wiki/%E7%A8%BB%E7%9B%9B%E5%92%8C%E5%A4%AB/19370732',
    'qiong-yao': 'https://baike.weixin.qq.com/v64425208.htm',
    'jimmy-carter': 'https://baike.weixin.qq.com/v34464.htm',
    'gordon-moore': 'https://baike.weixin.qq.com/v722034.htm',
    'charlie-munger': 'https://baike.weixin.qq.com/v7480201.htm',
    'giorgio-armani': 'https://m.baike.com/wiki/%E4%B9%94%E6%B2%BB%C2%B7%E9%98%BF%E7%8E%9B%E5%B0%BC/447180',
    'fred-smith': 'https://m.baike.com/wiki/%E5%BC%97%E9%9B%B7%E5%BE%B7%C2%B7%E5%8F%B2%E5%AF%86%E6%96%AF/1139857',
    'li-zheng-dao': 'https://baike.weixin.qq.com/v140366.htm',
    'yang-zhen-ning': 'https://m.baike.com/wiki/%E6%9D%A8%E6%8C%AF%E5%AE%81/242586',
    'jane-goodall': 'https://m.baike.com/wiki/%E7%8F%8D%E5%A6%AE%C2%B7%E5%8F%A4%E9%81%93%E5%B0%94/930156',
    'stephen-hawking': 'https://m.baike.com/wiki/%E6%96%AF%E8%92%82%E8%8A%AC%C2%B7%E9%9C%8D%E9%87%91/447217',
    'milan-kundera': 'https://m.baike.com/wiki/%E7%B1%B3%E5%85%B0%C2%B7%E6%98%86%E5%BE%B7%E6%8B%89/265051',
    'ryuichi-sakamoto': 'https://m.baike.com/wiki/%E5%9D%82%E6%9C%AC%E9%BE%99%E4%B8%80/881868',
    'seiji-ozawa': 'https://m.baike.com/wiki/%E5%B0%8F%E6%B3%BD%E5%BE%81%E5%B0%94/305357',
    'maggie-smith': 'https://m.baike.com/wiki/%E7%8E%9B%E5%90%89%C2%B7%E5%8F%B2%E5%AF%86%E6%96%AF/857891',
    'matthew-perry': 'https://baike.weixin.qq.com/v742202.htm',
    'michael-gambon': 'https://m.baike.com/wiki/%E8%BF%88%E5%85%8B%E5%B0%94%C2%B7%E7%94%98%E6%9C%AC/21591210',
    'miho-nakayama': 'https://m.baike.com/wiki/%E4%B8%AD%E5%B2%9B%E7%BE%8E%E5%98%89/307886',
    'robbie-coltrane': 'https://m.baike.com/wiki/%E7%BD%97%E5%BD%BC%C2%B7%E8%80%83%E7%89%B9%E6%8B%89%E5%B0%BC/2286417',
    'ye-jia-ying': 'https://m.baike.com/wiki/%E5%8F%B6%E5%98%89%E8%8E%B9/340655',
    'chen-xiao-xu': 'https://m.baike.com/wiki/%E9%99%88%E6%99%93%E6%97%AD/19308977',
    'huang-xu-hua': 'https://m.baike.com/wiki/%E9%BB%84%E6%97%AD%E5%8D%8E/19716130',
    'tanimura-shinji': 'https://m.baike.com/wiki/%E8%B0%B7%E6%9D%91%E6%96%B0%E5%8F%B8/1003507',
}

def update_baidu_links():
    people_dir = 'people'
    updated_count = 0
    missing_links = []

    # 遍历所有markdown文件
    for filename in os.listdir(people_dir):
        if not filename.endswith('.md'):
            continue

        filepath = os.path.join(people_dir, filename)
        name_key = filename.replace('.md', '')

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 获取对应的链接
        baidu_link = baidu_links.get(name_key)

        if baidu_link:
            # 检查是否已经有百度百科链接（不是空的）
            if re.search(r'- 百度百科链接：https?://', content):
                continue

            # 替换空的百度百科链接
            new_content = re.sub(
                r'- 百度百科链接：\s*\n',
                f'- 百度百科链接：{baidu_link}\n',
                content
            )

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"Updated: {filename}")
            updated_count += 1
        else:
            missing_links.append(name_key)

    print(f"\n=== Summary ===")
    print(f"Updated: {updated_count}")
    print(f"Missing links: {len(missing_links)}")
    if missing_links:
        print("\nFiles without Baidu links:")
        for name in sorted(missing_links):
            print(f"  - {name}")

if __name__ == '__main__':
    update_baidu_links()
