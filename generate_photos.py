#!/usr/bin/env python3
import os
import sys
import time
import subprocess

# 名人提示词映射
celebrity_prompts = {
    'cai-lan': 'Chua Lam, Hong Kong writer, gourmet, one of the Four Talents of Hong Kong',
    'charlie-munger': 'Charlie Munger, Berkshire Hathaway vice chairman, investor',
    'chen-xiao-xu': 'Chen Xiaoxu, Chinese actress, played Lin Daiyu in Dream of the Red Chamber',
    'chen-yong-quan': 'Chen Yongquan, Chinese xiangsheng performer',
    'de-de-ma': 'Dedema, Mongolian Chinese mezzo-soprano singer',
    'deng-xiao-ping': 'Deng Xiaoping, Chinese leader, reform and opening up',
    'fang-da-tong': 'Khalil Fong, Chinese singer-songwriter',
    'fang-ji-ge': 'Pope Francis, 266th Pope of the Catholic Church',
    'fred-smith': 'Fred Smith, founder of FedEx',
    'giorgio-armani': 'Giorgio Armani, Italian fashion designer, founder of Armani',
    'gordon-moore': 'Gordon Moore, co-founder of Intel, Moore\'s Law',
    'he-qing': 'He Qing, Chinese actress, classical beauty',
    'huang-xu-hua': 'Huang Xuhua, father of Chinese nuclear submarines, Republic Medal',
    'huang-yong-yu': 'Huang Yongyu, Chinese painter, designer of monkey stamp',
    'inamori-kazuo': 'Kazuo Inamori, founder of Kyocera, Japanese business guru',
    'jane-goodall': 'Jane Goodall, British primatologist, UN Messenger of Peace',
    'ji-chun-hua': 'Ji Chunhua, Chinese actor, martial artist',
    'jimmy-carter': 'Jimmy Carter, 39th President of the United States',
    'kobe-bryant': 'Kobe Bryant, NBA basketball player, Los Angeles Lakers',
    'li-jing-fei': 'Li Jingfei, Chinese actor, played Zhang Fei in Romance of the Three Kingdoms',
    'li-min': 'Coco Lee, Chinese pop singer',
    'li-yi-ning': 'Li Yining, Chinese economist, advocate of shareholding reform',
    'li-yong': 'Li Yong, Chinese TV host',
    'li-zhao-ji': 'Lee Shau Kee, Hong Kong real estate tycoon, founder of Henderson Land',
    'li-zheng-dao': 'Tsung-Dao Lee, Nobel Prize in Physics, Chinese-American physicist',
    'liu-jia-chang': 'Liu Jiachang, Chinese music godfather',
    'lu-shu-ming': 'Lu Shuming, Chinese actor, played Guan Yu in Romance of the Three Kingdoms',
    'ma-shi-tu': 'Ma Shitu, Chinese writer and calligrapher',
    'maggie-smith': 'Maggie Smith, British actress, Oscar winner',
    'manmohan-singh': 'Manmohan Singh, former Prime Minister of India',
    'matthew-perry': 'Matthew Perry, actor, Chandler in Friends',
    'michael-gambon': 'Michael Gambon, British actor, Dumbledore in Harry Potter',
    'miho-nakayama': 'Miho Nakayama, Japanese actress and singer, starred in Love Letter',
    'milan-kundera': 'Milan Kundera, Czech writer, author of The Unbearable Lightness of Being',
    'min-ying-hua': 'Min Yinghua, researcher at Institute of Computing Technology, Chinese Academy of Sciences',
    'ni-kuang': 'Ni Kuang, one of Hong Kong Four Talents, author of Wisely series',
    'nian-guang-jiu': 'Nian Guangjiu, founder of Shazi Guazi, China\'s first peddler',
    'pele': 'Pele, Brazilian football king, player of the century',
    'qian-bai-hui': 'Qian Baihui, Taiwanese singer',
    'qiao-yu': 'Qiao Yu, Chinese lyricist, author of My Motherland',
    'qiong-yao': 'Chiung Yao, Taiwanese romance novelist',
    'ren-rong-rong': 'Ren Rongrong, Chinese children\'s writer and translator',
    'robbie-coltrane': 'Robbie Coltrane, British actor, Hagrid in Harry Potter',
    'ryuichi-sakamoto': 'Ryuichi Sakamoto, Japanese musician, composer of The Last Emperor',
    'seiji-ozawa': 'Seiji Ozawa, Japanese conductor',
    'shen-qing': 'Shen Qing, Chinese campus folk singer, author of Youth',
    'shen-xu-bang': 'Shen Xubang, CAS academician, computer expert',
    'shi-ban-yu': 'Shi Banyu, voice actor for Stephen Chow',
    'stephen-hawking': 'Stephen Hawking, British theoretical physicist, cosmologist',
    'steve-jobs': 'Steve Jobs, co-founder of Apple',
    'su-dong-zhuang': 'Su Dongzhuang, Chinese computer science master',
    'tang-xiao-ou': 'Tang Xiaoou, founder of SenseTime, AI scientist',
    'tanimura-shinji': 'Shinji Tanimura, Japanese national treasure singer',
    'tong-xiang-ling': 'Tong Xiangling, Peking opera performing artist',
    'vangelis': 'Vangelis, Greek musician, composer of Chariots of Fire',
    'wang-tie-cheng': 'Wang Tiecheng, performing artist',
    'wu-meng-da': 'Ng Man-tat, Hong Kong comedy actor',
    'xie-li-si': 'Xie Lisi, singer of China Film Orchestra',
    'xu-shao-qiang': 'Norman Chu, Hong Kong actor',
    'xu-xi-yuan': 'Barbie Hsu, Taiwanese actress and singer',
    'yang-shao-hua': 'Yang Shaohua, Chinese xiangsheng performer',
    'yang-shi-e': 'Yang Shi\'e, CAE academician, underwater acoustics expert',
    'yang-zhen-ning': 'Chen-Ning Yang, Nobel Prize in Physics, world-renowned physicist',
    'yao-bei-na': 'Yao Beina, Chinese young singer',
    'ye-jia-ying': 'Florence Chia-ying Yeh, Chinese classical literature scholar',
    'yu-meng-long': 'Alan Yu, Chinese actor and singer',
    'yuan-long-ping': 'Yuan Longping, father of hybrid rice, Republic Medal',
    'zhang-shao-hua': 'Zhang Shaohua, Chinese actress, starred in The Grand Mansion Gate',
    'zheng-hua-juan': 'Zheng Huajuan, Taiwanese songwriter',
    'zheng-pei-pei': 'Cheng Pei-pei, martial arts queen',
    'zhou-hai-mei': 'Kathy Chow, Hong Kong actress',
    'zong-qing-hou': 'Zong Qinghou, founder of Wahaha Group',
    'zuo-hui': 'Zuo Hui, founder of Ke Holdings, founder of Lianjia',
}

def generate_photo(filename, prompt):
    """为名人生成照片"""
    photo_name = filename.replace('.md', '.jpg')
    photo_path = os.path.join('pics', photo_name)
    
    # 检查照片是否已存在
    if os.path.exists(photo_path):
        print(f"Skip: {photo_name} (already exists)")
        return True
    
    # 使用text_to_image API
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={prompt}&image_size=square_hd"
    
    try:
        print(f"Generating: {photo_name}")
        result = subprocess.run(
            ['wget', '-q', '-O', photo_path, url],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"Success: {photo_name}")
            return True
        else:
            print(f"Failed: {photo_name}")
            if os.path.exists(photo_path):
                os.remove(photo_path)
            return False
    except Exception as e:
        print(f"Error: {photo_name} - {e}")
        if os.path.exists(photo_path):
            os.remove(photo_path)
        return False

def main():
    people_dir = 'people'
    pics_dir = 'pics'
    
    # 确保pics目录存在
    if not os.path.exists(pics_dir):
        os.makedirs(pics_dir)
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    # 获取所有名人文件
    for filename in os.listdir(people_dir):
        if not filename.endswith('.md'):
            continue
        
        photo_name = filename.replace('.md', '.jpg')
        photo_path = os.path.join(pics_dir, photo_name)
        
        # 检查照片是否已存在
        if os.path.exists(photo_path):
            print(f"Skip: {photo_name} (already exists)")
            skip_count += 1
            continue
        
        # 获取提示词
        name_key = filename.replace('.md', '')
        prompt = celebrity_prompts.get(name_key, name_key.replace('-', ' '))
        
        # 生成照片
        if generate_photo(filename, prompt):
            success_count += 1
        else:
            fail_count += 1
        
        # 避免请求过快
        time.sleep(2)
    
    print(f"\n=== Summary ===")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Skipped: {skip_count}")

if __name__ == '__main__':
    main()
