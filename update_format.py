#!/usr/bin/env python3
import os
import re

def parse_current_format(content):
    """解析当前格式文件"""
    data = {}
    lines = content.split('\n')
    
    # 提取标题
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            data['标题'] = line[2:].strip()
            break
    
    # 提取各个字段
    field_map = {
        '姓名': '姓名',
        '性别': '性别',
        '国籍': '国籍',
        '出生日期': '出生日期',
        '去世日期': '去世日期',
        '生平事迹': '生平事迹',
        '主要贡献': '主要贡献',
        '百度百科': '百度百科',
        '维基百科': '维基百科'
    }
    
    for line in lines:
        line = line.strip()
        for key in field_map:
            if line.startswith(f'{key}：'):
                data[field_map[key]] = line[len(key)+1:].strip()
                break
    
    return data

def format_to_spec(data, filename):
    """格式化为spec.md要求的格式"""
    name = data.get('姓名', data.get('标题', ''))
    photo_name = filename.replace('.md', '.jpg')
    
    return f"""# {name}

![](pics/{photo_name})

- 姓名：{data.get('姓名', '')}
- 性别：{data.get('性别', '')}
- 国籍：{data.get('国籍', '')}
- 出生日期：{data.get('出生日期', '')}
- 去世日期：{data.get('去世日期', '')}

# 生平事迹

{data.get('生平事迹', '')}

# 主要贡献

{data.get('主要贡献', '')}

# 参考资料

- 百度百科链接：{data.get('百度百科', '')}
"""

def update_files():
    people_dir = 'people'
    count = 0
    errors = []

    for filename in os.listdir(people_dir):
        if not filename.endswith('.md'):
            continue

        filepath = os.path.join(people_dir, filename)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否已经是spec格式
        if '![](pics/' in content and '- 姓名：' in content:
            continue

        # 解析当前格式
        data = parse_current_format(content)

        if not data:
            errors.append(filename)
            continue

        # 生成spec格式
        new_content = format_to_spec(data, filename)

        # 写回文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        count += 1
        print(f"Updated: {filename}")

    print(f"\nTotal updated: {count}")
    if errors:
        print(f"Errors: {errors}")

if __name__ == '__main__':
    update_files()
