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
    'fang-ji-ge': 'Pope Francis, 266th Pope of the Catholic Church',
    'fred-smith': 'Fred Smith, founder of FedEx',
    'giorgio-armani': 'Giorgio Armani, Italian fashion designer, founder of Armani',
    'gordon-bell': 'Gordon Bell, American computer engineer, DEC PDP designer, computer architecture pioneer',
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
    'li-ze-hou': 'Li Zehou, Chinese philosopher and aesthetician, author of The Path of Beauty',
    'li-zhao-ji': 'Lee Shau Kee, Hong Kong real estate tycoon, founder of Henderson Land',
    'li-zheng-dao': 'Tsung-Dao Lee, Nobel Prize in Physics, Chinese-American physicist',
    'liu-jia-chang': 'Liu Jiachang, Chinese music godfather',
    'liu-wei-wei': 'Liu Weiwei, Chinese tenor, opera singer, spinto tenor, national first-class performer',
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
    'ren-changxia': 'Ren Changxia, Chinese female police officer, national hero, director of Dengfeng Public Security Bureau',
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
    'wu-zun-you': 'Wu Zunyou, Chinese epidemiologist, chief expert at China CDC',
    'xu-shao-qiang': 'Norman Chu, Hong Kong actor',
    'xu-xi-yuan': 'Barbie Hsu, Taiwanese actress and singer',
    'yang-shao-hua': 'Yang Shaohua, Chinese xiangsheng performer',
    'yang-shi-e': 'Yang Shi\'e, CAE academician, underwater acoustics expert',
    'yang-li-de': 'Yang Lide, Taiwanese lyricist and music producer, composer of Dear Child',
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
    'ai-qing': 'Ai Qing, Chinese poet, author of I Love This Land',
    'aixinjueluo-pujie': 'Aisin Gioro Pujie, brother of the last Qing emperor Puyi',
    'akira-kurosawa': 'Akira Kurosawa, Japanese film director, Seven Samurai',
    'alan-rickman': 'Alan Rickman, British actor, played Snape in Harry Potter',
    'anita-mui': 'Anita Mui, Hong Kong singer and actress',
    'bin-xin': 'Bing Xin, Chinese writer, representative of modern Chinese literature',
    'blacky-ko': 'Blacky Ko, Hong Kong stuntman and actor',
    'buren-bayir': 'Buren Bayir, Mongolian singer, member of Three Lucky Treasures',
    'charles-kao': 'Charles Kao, father of fiber optics, Nobel Prize winner',
    'chen-bide': 'Chen Bide, father of Taiwanese pop music',
    'cheng-kaijia': 'Cheng Kaijia, Chinese nuclear physicist, Two Bombs One Star',
    'chen-jingrun': 'Chen Jingrun, Chinese mathematician, Goldbach conjecture',
    'chen-xingshen': 'Chen Xingshen, Chinese-American mathematician, father of differential geometry',
    'chen-zhaodi': 'Chen Zhaodi, Chinese women\'s volleyball player, world champion',
    'chen-zhiyuan': 'Chen Zhiyuan, Taiwanese composer',
    'chen-zhongshi': 'Chen Zhongshi, Chinese writer, author of White Deer Plain',
    'dai-tielang': 'Dai Tielang, Chinese animation director, Black Cat Sheriff',
    'deng-lijun': 'Teresa Teng, Chinese singer',
    'dennis-ritchie': 'Dennis Ritchie, creator of C language and Unix',
    'diana-princess': 'Princess Diana, Princess of Wales',
    'diego-maradona': 'Diego Maradona, Argentine football legend',
    'ding-guangquan': 'Ding Guangquan, Chinese xiangsheng performer',
    'elizabeth-taylor': 'Elizabeth Taylor, American actress, two-time Oscar winner',
    'fidel-castro': 'Fidel Castro, Cuban revolutionary leader',
    'fong-fei-fei': 'Fong Fei Fei, Taiwanese singer',
    'fu-biao': 'Fu Biao, Chinese actor',
    'gao-xiumin': 'Gao Xiumin, Chinese sketch performer',
    'garcia-marquez': 'Gabriel Garcia Marquez, Colombian writer, magical realism',
    'ge-cunzhuang': 'Ge Cunzhuang, Chinese actor',
    'george-bush': 'George Bush, 41st President of the United States',
    'gu-yue': 'Gu Yue, Chinese special actor, Mao Zedong impersonator',
    'he-luting': 'He Luting, Chinese composer',
    'hou-yaowen': 'Hou Yaowen, Chinese xiangsheng performer',
    'huang-danian': 'Huang Danian, world-renowned Chinese geophysicist',
    'huang-renyu': 'Huang Renyu, Chinese historian, author of 1587 Year of No Significance',
    'huang-yi': 'Huang Yi, Chinese fantasy novel writer',
    'i-ming-pei': 'I. M. Pei, Chinese-American architect, Louvre Pyramid',
    'jd-salinger': 'J.D. Salinger, American writer, The Catcher in the Rye',
    'jin-yong': 'Jin Yong, Chinese wuxia novelist',
    'juan-samaranch': 'Juan Antonio Samaranch, former IOC president',
    'kenneth-tsang': 'Kenneth Tsang, Hong Kong actor',
    'lam-kit-ying': 'Lam Kit Ying, Hong Kong actress',
    'lan-tianye': 'Lan Tianye, Chinese stage actor',
    'leslie-cheung': 'Leslie Cheung, Hong Kong singer and actor',
    'leslie-nielsen': 'Leslie Nielsen, Canadian comedy actor',
    'liang-yusheng': 'Liang Yusheng, Chinese wuxia novelist',
    'li-ao': 'Li Ao, Taiwanese writer and political commentator',
    'li-peiyao': 'Li Peiyao, Chinese politician',
    'li-wanfen': 'Li Wanfen, Chinese performing artist',
    'li-wenhua': 'Li Wenhua, Chinese xiangsheng performer',
    'lou-gerstner': 'Lou Gerstner, former IBM CEO, led IBM turnaround',
    'luo-jing': 'Luo Jing, CCTV news anchor',
    'luosang-nyima': 'Luosang Nyima, Chinese xiangsheng performer from Tibet',
    'ma-ji': 'Ma Ji, Chinese xiangsheng master',
    'ma-sanli': 'Ma Sanli, Chinese xiangsheng grand master',
    'michael-jackson': 'Michael Jackson, King of Pop',
    'mike-wallace': 'Mike Wallace, American journalist for 60 Minutes',
    'muhammad-ali': 'Muhammad Ali, boxing legend',
    'mu-tiezhu': 'Mu Tiezhu, Chinese basketball player',
    'olivia-de-havilland': 'Olivia de Havilland, American actress, Gone with the Wind',
    'peter-drucker': 'Peter Drucker, father of modern management',
    'pierre-cardin': 'Pierre Cardin, French fashion designer',
    'qian-qichen': 'Qian Qichen, Chinese diplomat',
    'qian-xuesen': 'Qian Xuesen, father of Chinese aerospace',
    'qian-zhongshu': 'Qian Zhongshu, Chinese writer, Fortress Besieged',
    'qi-gong': 'Qi Gong, Chinese calligrapher and educator',
    'queen-elizabeth': 'Queen Elizabeth II, British monarch',
    'richard-nixon': 'Richard Nixon, 37th President of the United States',
    'run-run-shaw': 'Run Run Shaw, Hong Kong film mogul',
    'sakura-momoko': 'Momoko Sakura, Japanese manga artist, Chibi Maruko-chan',
    'sean-connery': 'Sean Connery, British actor, the first James Bond',
    'shan-tianfang': 'Shan Tianfang, Chinese pingshu performer',
    'shen-dianxia': 'Lydia Shum, Hong Kong actress',
    'sheng-zhong-guo': 'Sheng Zhongguo, Chinese violinist',
    'shirley-temple': 'Shirley Temple, American child star',
    'shi-shengjie': 'Shi Shengjie, Chinese xiangsheng performer',
    'song-meiling': 'Soong Mei-ling, wife of Chiang Kai-shek',
    'stan-lee': 'Stan Lee, father of Marvel Comics',
    'su-buqing': 'Su Buqing, Chinese mathematician',
    'takakura-ken': 'Ken Takakura, Japanese actor',
    'tang-jiezhong': 'Tang Jiezhong, Chinese xiangsheng performer',
    'tie-niu': 'Tie Niu, Chinese actor',
    'toriyama-akira': 'Akira Toriyama, Japanese manga artist, creator of Dragon Ball',
    'wang-jiangmin': 'Wang Jiangmin, father of Chinese antivirus software',
    'wang-luobin': 'Wang Luobin, Chinese folk song composer',
    'wang-xiaobo': 'Wang Xiaobo, Chinese writer',
    'wei-wei': 'Wei Wei, Chinese writer, Who Are the Most Adorable People',
    'xiao-lin': 'Xiao Lin, Chinese xiangsheng performer',
    'xie-jin': 'Xie Jin, Chinese film director',
    'xin-fengnian': 'Xin Fengnian, Chinese music critic',
    'xu-chi': 'Xu Chi, Chinese poet and essayist',
    'yang-dezhi': 'Yang Dezhi, Chinese PLA general',
    'yang-jiang': 'Yang Jiang, Chinese writer and translator',
    'yang-jie': 'Yang Jie, Chinese TV director, Journey to the West',
    'yan-huaili': 'Yan Huaili, Chinese actor, played Sha Wujing',
    'yan-su': 'Yan Su, Chinese lyricist',
    'yao-li': 'Yao Li, Chinese singer from the Republican era',
    'ye-maozhong': 'Ye Maozhong, Chinese marketing consultant',
    'ye-yonglie': 'Ye Yonglie, Chinese science writer',
    'yitzhak-rabin': 'Yitzhak Rabin, former Prime Minister of Israel',
    'yuan-kuocheng': 'Yuan Kuocheng, Chinese pingshu performer',
    'yuan-shihai': 'Yuan Shihai, Chinese Peking opera performer',
    'yu-guangzhong': 'Yu Guangzhong, Chinese poet, author of Homesickness',
    'yu-xunfa': 'Yu Xunfa, Chinese bamboo flute performer',
    'zang-tianshuo': 'Zang Tianshuo, Chinese rock singer',
    'zeng-shiqiang': 'Zeng Shiqiang, Chinese management scholar',
    'zhang-ailing': 'Zhang Ailing, Chinese writer',
    'zhang-qiang': 'Zhang Qiang, Chinese weightlifting athlete',
    'zhang-xueliang': 'Zhang Xueliang, Chinese general, Xian Incident',
    'zhang-zhen': 'Zhang Zhen, Chinese PLA general',
    'zhao-lirong': 'Zhao Lirong, Chinese sketch performer',
    'zhao-puchu': 'Zhao Puchu, Chinese religious leader and poet',
    'zhao-zhongxiang': 'Zhao Zhongxiang, CCTV host',
    'zhou-guangzhao': 'Zhou Guangzhao, Chinese physicist, CAS president',
    'zhou-youguang': 'Zhou Youguang, father of Chinese Pinyin',
    'zhuang-nu': 'Zhuang Nu, Chinese lyricist, author of Tian Mi Mi',
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
    people_dir = 'celebrity'
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
