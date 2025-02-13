import datetime as dt
from datetime import datetime
class Comps():
    # date
    def date_minussecond(d: datetime):
        return d + dt.timedelta(seconds=-1)
    def str_date(d: datetime): # date -> %y/%m/%d(%a)
        return d.strftime('%y/%m/%d(%a)')
    def date_start(d: datetime): # date -> start_date
        s = d.strftime('%Y/%m/%d')
        return datetime.strptime(s + "/00/00/00", '%Y/%m/%d/%H/%M/%S')
    def date_end(d: datetime): # date -> end_date
        d = d + dt.timedelta(days=1)
        s = d.strftime('%Y/%m/%d')
        return datetime.strptime(s + "/00/00/00", '%Y/%m/%d/%H/%M/%S')
    def dateformstr_date(d: datetime): # date -> %Y-%m-%d
        return d.strftime('%Y-%m-%d')
    def datedate_formstr(s: str): # %Y-%m-%d -> date  datedate_formstr
        return datetime.strptime(s, '%Y-%m-%d')
    def dategetstr_datestr(s: str): # %y/%m/%d(%a) -> %y%m%d
        s0 = datetime.strptime(s, '%y/%m/%d(%a)')
        return s0.strftime('%y%m%d')
    def datedatestr_getstr(s: str): # %y%m%d -> %y/%m/%d(%a)
        s0 = datetime.strptime(s, '%y%m%d')
        return s0.strftime('%y/%m/%d(%a)')
    def dateformstr_getstr(s: str): # %Y%m%d -> %Y-%m-%d
        s0 = datetime.strptime(s, '%y%m%d')
        return s0.strftime('%Y-%m-%d')        
    def dategetstr_formstr(s: str): # %Y-%m-%d -> %y%m%d
        s0 = datetime.strptime(s, '%Y-%m-%d')
        return s0.strftime('%y%m%d')
    def datedate_getstr(s: str): # %y%m%d -> date
        return datetime.strptime(s, '%y%m%d')

    # players
    def players(s: str):
        c1 = s.split("/")
        temp = []
        for p in c1:
            c2 = p.split(",")
            temp.append(c2[0] + " (" + c2[1] + ")")
        return temp
    def player_name(s: str, n: int):
        c1 = s.split("/")
        c2 = c1[n].split(",")
        return c2[0] + " (" + str(c2[1]) + ")"
    # serves
    def serve_plus(s:str, p_n:int, s_n:int):
        s1 = s.split("/")
        s2 = s1[p_n].split(",")
        s2[s_n] = str(min(99, int(s2[s_n]) + 1))
        s3 = ""
        for i in range(6):
            s3 = s3 + s2[i] + ","
        s3 = s3[0:-1]
        s1[p_n] = s3
        s4 = ""
        for i in range(len(s1)):
            s4 = s4 + s1[i] + "/"
        s4 = s4[0:-1] 
        return s4
    
    def serve_minus(s:str, p_n:int, s_n:int):
        s1 = s.split("/")
        s2 = s1[p_n].split(",")
        s2[s_n] = str(max(0, int(s2[s_n]) - 1))
        s3 = ""
        for i in range(6):
            s3 = s3 + s2[i] + ","
        s3 = s3[0:-1]
        s1[p_n] = s3
        s4 = ""
        for i in range(len(s1)):
            s4 = s4 + s1[i] + "/"
        s4 = s4[0:-1] 
        return s4
    def player_serves_1(p: str, s:str):
        temp = []
        ps1 = p.split("/")
        ss1 = s.split("/")
        for i in range(len(ps1)):
            ps2 = ps1[i].split(",")
            ss2 = ss1[i].split(",")
            success = int(ss2[0]) + int(ss2[1]) + int(ss2[2])
            failed = int(ss2[3]) + int(ss2[4]) + int(ss2[5])
            total = success + failed
            if total > 0 :
                percent = 100.0 * success / total 
                percent2 = 100.0 * (int(ss2[0]) + int(ss2[1]))/ total
            else:
                percent = 0.0
                percent2 = 0.0
            temp.append([i, ps2[0] + " (" + ps2[1] + ")", success, failed, total, percent, percent2])
        return temp
    def player_serves_2(p: str, s: str):
        temp = []
        ps1 = p.split("/")
        ss1 = s.split("/")
        for i in range(len(ps1)):
            ps2 = ps1[i].split(",")
            ss2 = ss1[i].split(",")
            temp.append([i, ps2[0] + " (" + ps2[1] + ")", int(ss2[0]), int(ss2[1]), int(ss2[2]), int(ss2[3]), int(ss2[4]), int(ss2[5])])
        return temp
    
    def serve(s:str, n: int):
        ss1 = s.split("/")
        ss2 = ss1[n].split(",")
        return ss2
    
    def str_serves(d: dict): # 'form-0-serve_0':[0]
        s = ""
        i = 0
        while True:
            j = 0
            v = d.get('form-' + str(i) + '-serve_' + str(j), "")
            if  v == "": 
                break
            for j in range(6):
                s = s + str(d['form-' + str(i) + '-serve_' + str(j)]) + ','
            s = s + '/'
            i = i + 1
        s = s[0:-1]
        return s
            

        #for i in range(len(d['serve_0'])):
        #    for j in range(6):
        #        s = s + str(d['serve_' + str(j)][i]) + "/"
        #s = s[0:-1]
        #return s
    
        
    # results
    def strScore(d:dict):
        s = ""
        for i in range(6):
            k0 = 'score' + str(i) + '_0'
            k1 = 'score' + str(i) + '_1'
            if str(d[k0]) != '' and str(d[k1]) != '':
                s = s + d[k0] + "," + d[k1] + "/"
        s = s[0:-1]
        return s
    
    def scoreStr(s:str):
        c1 = s.split("/")
        c2 = str(c1[0]).split(",")

        return str(c2[0]) + " - " + str(c2[1])
    
    def scoreHoshi(s: str):
        c1 = s.split("/")
        c2 = str(c1[0]).split(",")
        if c2[0] > c2[1]:
            hoshi = "〇"
        elif c2[0] < c2[1]:
            hoshi = "×"
        else:
            hoshi = "△"

        return hoshi
        

    def scores(s: str):
        c1 = s.split("/")
        temp = []
        for index, c in enumerate(c1):
            if index > 0:
                c2 = c.split(',')
                temp.append(str(c2[0]) + " - " + str(c2[1]))
        return temp
    
    def allscoreNums(s: str):
        c1 = s.split("/")
        temp = []
        for c in c1:
            c2 = c.split(',')
            temp.append(c2)
        return temp