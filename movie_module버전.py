con, cur = None, None
DB_dic={}
movie_num=0

def insertData() :
    con = sqlite3.connect("D:/sqlite/Test")##개인설정으로 바꿔야함.
    cur = con.cursor()
    data1 = DB_dic['name']
    data2 = str(DB_dic['score'])
    data3 = str(DB_dic['number'])
    print(type(data1), type(data2), type(data3))
    sql = "INSERT INTO t4 VALUES('"+data1+"','"+data2+"','"+data3+"');"
    cur.execute(sql)
    con.commit()
    con.close()

def printData() :
    con = sqlite3.connect("D:/sqlite/Test")##개인설정으로 바꿔야함.
    cur = con.cursor()
    sql = "SELECT * FROM t4 ORDER BY score DESC;"
    cur.execute(sql)
    result = cur.fetchall()
    i=0
    for data in result:
        da_li = str(data).split(', ')
        print("%s %s" % (str(da_li[0])[1:], da_li[1]))
        i+=1
        if i>5: break

    con.close()

def searching_movie():
    global movie_num
    movie = input("어떤 영화를 검색하시겠습니까? ")
    url = f'https://movie.naver.com/movie/search/result.naver?query={movie}&section=all&ie=utf8'
    if movie == '0' :
        printData()
        exit()
    user_dic = {}
    point_dic = []
    name_list = ['', ]
    score_list = ['', ]
    res = requests.get(url)
    index = 1


    if res.status_code == 200:  #HTTP status code가 OK일 때
        soup=BeautifulSoup(res.text,'lxml')
    
    
        for href in soup.find("ul", class_="search_list_1").find_all("li"):
            print(f"=============={index}번 영화===============")
            print(href.dl.text[:-2])    #영화 정보 출력

            name_list.append(href.dl.text.split('\n')[1])
            try :
                score_list.append(float(href.dl.text.split('\n')[3][:4]))
            except :
                ##0으로 할지, 뭐 NULL로 할지는 보류
                score_list.append(0.0)
            # 영화 평점

            user_dic[index] = int(href.dl.dt.a['href'][30:])    #index에 따른 영화 고유 코드 dictionary에 저장
            index = index+1

    num = int(input("몇 번 영화를 선택하시겠습니까? (숫자만 입력) "))
    movie_num = user_dic[num]   #영화 고유 숫자
    DB_dic['name'] = name_list[num]
    DB_dic['number'] = movie_num
    DB_dic['score'] = score_list[num]
    #print(DB_dic)
    base_url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code={num}&type=after&onlyActualPointYn=N&onlySpoilerPointYn=N&order=sympathyScore&page='

    crawling()


def allthing():
    global movie_num
    searching_movie()
    crawling()
    frequency(str(movie_num))
    print_senti("%s" % str(movie_num))
    cloud(str(movie_num))

    insertData()
    printData()
    

#개봉안한영화 -> 예외처리
