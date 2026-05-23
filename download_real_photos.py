#!/usr/bin/env python3
"""批量获取名人真实照片，替换AI生成的照片。

来源优先级：百度百科 -> 待定
"""
import os
import re
import subprocess
import time
import sys

SKIP_EXISTING = True       # 跳过已有真实照片的（非173K的标准化AI图）
TIMEOUT = 15               # 单次请求超时秒数
SLEEP = 1.5                # 请求间隔


def is_ai_photo(path: str) -> bool:
    """判断是否是AI生成的标准化照片（173KB左右，1832x1832）"""
    if not os.path.exists(path):
        return False
    size = os.path.getsize(path)
    # AI照片典型特征: ~173KB, 1832x1832
    return 150000 < size < 200000


def get_celebrity_name(filepath: str) -> str:
    """从markdown文件中提取中文姓名"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'^# (.+)$', content, re.MULTILINE)
    if m:
        name = m.group(1)
        # 清理姓名中的括号注释，如 "方济各（Pope Francis）" -> "方济各"
        name = re.sub(r'[（(].*[）)]', '', name).strip()
        return name
    return ''


def download_baidu_baike_photo(name: str, output_path: str) -> bool:
    """从百度百科获取人物照片"""
    import urllib.parse
    encoded = urllib.parse.quote(name)
    html_file = f'/tmp/bk_{name[:4]}.html'

    # 下载百度百科页面
    try:
        result = subprocess.run(
            ['wget', '-q', '-O', html_file,
             f'https://baike.baidu.com/item/{encoded}',
             '--timeout', str(TIMEOUT),
             '-U', 'Mozilla/5.0 (X11; Linux x86_64)'],
            capture_output=True, text=True, timeout=TIMEOUT + 5
        )
        if result.returncode != 0:
            return False
    except Exception:
        return False

    if os.path.getsize(html_file) < 5000:
        return False

    # 提取boje CDN图片URL
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    urls = re.findall(r'https?://bkimg\.cdn\.bcebos\.com/pic/[a-f0-9]+', html)
    if not urls:
        # 尝试smart格式
        urls = re.findall(
            r'https?://bkimg\.cdn\.bcebos\.com/smart/[a-f0-9]+',
            html
        )

    if not urls:
        return False

    # 下载第一张（通常是肖像）
    img_url = urls[0]
    try:
        result = subprocess.run(
            ['wget', '-q', '-O', output_path, img_url,
             '--timeout', str(TIMEOUT)],
            capture_output=True, text=True, timeout=TIMEOUT + 5
        )
        if result.returncode != 0:
            return False
    except Exception:
        return False

    # 验证下载结果
    if not os.path.exists(output_path):
        return False
    size = os.path.getsize(output_path)
    if size < 2000:  # 太小，不是有效图片
        os.remove(output_path)
        return False

    return True


def download_wikipedia_photo(name_en: str, output_path: str) -> bool:
    """从Wikipedia获取照片（备用方案）"""
    import urllib.parse
    encoded = urllib.parse.quote(name_en.replace(' ', '_'))
    api_url = (
        f'https://en.wikipedia.org/w/api.php?action=query&titles='
        f'{encoded}&prop=pageimages&format=json&pithumbsize=800'
    )
    try:
        result = subprocess.run(
            ['wget', '-q', '-O', '-', api_url,
             '--timeout', str(TIMEOUT)],
            capture_output=True, text=True, timeout=TIMEOUT + 5
        )
        if result.returncode != 0:
            return False
        import json
        data = json.loads(result.stdout)
        pages = data.get('query', {}).get('pages', {})
        for pid, page in pages.items():
            thumb = page.get('thumbnail', {}).get('source')
            if thumb:
                result2 = subprocess.run(
                    ['wget', '-q', '-O', output_path, thumb,
                     '--timeout', str(TIMEOUT)],
                    capture_output=True, text=True, timeout=TIMEOUT + 5
                )
                if result2.returncode == 0 and os.path.getsize(output_path) > 2000:
                    return True
    except Exception:
        return False
    return False


def main():
    people_dir = 'celebrity'
    pics_dir = 'pics'
    if not os.path.exists(pics_dir):
        os.makedirs(pics_dir)

    files = sorted([f for f in os.listdir(people_dir) if f.endswith('.md')])

    success = 0
    skipped = 0
    failed = 0

    # 外国人姓名映射（中文名 -> 英文Wikipedia名）
    foreign_map = {
        '史蒂芬·霍金': 'Stephen_Hawking',
        '史蒂夫·乔布斯': 'Steve_Jobs',
        '迈克尔·杰克逊': 'Michael_Jackson',
        '斯坦·李': 'Stan_Lee',
        '丹尼斯·里奇': 'Dennis_Ritchie',
        '彼得·德鲁克': 'Peter_Drucker',
        '戈登·摩尔': 'Gordon_Moore',
        '查理·芒格': 'Charlie_Munger',
        '戈登·贝尔': 'Gordon_Bell',
        '伊丽莎白·泰勒': 'Elizabeth_Taylor',
        '肖恩·康纳利': 'Sean_Connery',
        '艾伦·里克曼': 'Alan_Rickman',
        '伊丽莎白二世': 'Elizabeth_II',
        '戴安娜王妃': 'Diana,_Princess_of_Wales',
        '菲德尔·卡斯特罗': 'Fidel_Castro',
        '乔治·布什': 'George_H._W._Bush',
        '理查德·尼克松': 'Richard_Nixon',
        '伊扎克·拉宾': 'Yitzhak_Rabin',
        '穆罕默德·阿里': 'Muhammad_Ali',
        '科比·布莱恩特': 'Kobe_Bryant',
        '迭戈·马拉多纳': 'Diego_Maradona',
        '贝利': 'Pelé',
        '吉米·卡特': 'Jimmy_Carter',
        '曼莫汉·辛格': 'Manmohan_Singh',
        '胡安·萨马兰奇': 'Juan_Antonio_Samaranch',
        'J.D.塞林格': 'J._D._Salinger',
        '米兰·昆德拉': 'Milan_Kundera',
        '加西亚·马尔克斯': 'Gabriel_García_Márquez',
        '玛丽·弗雷德里克森': 'Marie_Fredriksson',
        '玛吉·史密斯': 'Maggie_Smith',
        '迈克尔·甘本': 'Michael_Gambon',
        '马修·派瑞': 'Matthew_Perry',
        '莱斯利·尼尔森': 'Leslie_Nielsen',
        '秀兰·邓波儿': 'Shirley_Temple',
        '皮尔·卡丹': 'Pierre_Cardin',
        '奥利维亚·德哈维兰': 'Olivia_de_Havilland',
        '乔治·阿玛尼': 'Giorgio_Armani',
        '弗雷德·史密斯': 'Frederick_W._Smith',
        '珍·古道尔': 'Jane_Goodall',
        '方济各': 'Pope_Francis',
    }

    for filename in files:
        key = filename.replace('.md', '')
        filepath = os.path.join(people_dir, filename)
        pic_path = os.path.join(pics_dir, f'{key}.jpg')

        name = get_celebrity_name(filepath)
        if not name:
            print(f'SKIP  {key}: no name found')
            skipped += 1
            continue

        # 跳过非AI照片
        if SKIP_EXISTING and not is_ai_photo(pic_path):
            print(f'SKIP  {key} ({name}): already has real photo')
            skipped += 1
            continue

        print(f'FETCH {key} ({name})... ', end='', flush=True)

        # 尝试百度百科
        if download_baidu_baike_photo(name, pic_path):
            size_kb = os.path.getsize(pic_path) // 1024
            print(f'OK (baike, {size_kb}KB)')
            success += 1
            time.sleep(SLEEP)
            continue

        # 外国人尝试Wikipedia
        eng = foreign_map.get(name)
        if eng and download_wikipedia_photo(eng, pic_path):
            size_kb = os.path.getsize(pic_path) // 1024
            print(f'OK (wiki, {size_kb}KB)')
            success += 1
            time.sleep(SLEEP)
            continue

        print('FAIL')
        failed += 1
        time.sleep(SLEEP)

    print(f'\n=== Done ===')
    print(f'Success: {success}')
    print(f'Skipped: {skipped}')
    print(f'Failed:  {failed}')


if __name__ == '__main__':
    main()
