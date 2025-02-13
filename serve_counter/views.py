from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from datetime import datetime

from django import forms
from .forms import LoginForm, GameForm, GameResultForm, TermForm, ServeForm
from .models import Player, Game


from .comps import Comps
#from django.views.decorators.csrf import csrf_exempt

#---index
def index(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect(to = '/serve_counter/select')
    else:
        form=LoginForm(initial={'username':'guest'})
    params={
        'form':form,
    }
    return render(request, 'serve_counter/index.html', params)

#---logout
def logoutv(request):
    #logout(request)
    return render(request, 'serve_counter/logoutv.html')

#---select
@login_required(login_url='/serve_counter/')
def select(request):
    # logout(request)
    return render(request, 'serve_counter/select.html')

#---today
@login_required(login_url='/serve_counter/')
def today(request):
    now = timezone.localtime(timezone.now())
    n = Comps.str_date(now)
    #s0 = now.strftime('%Y/%m/%d')
    #v = Comps.str_date(now) datetime.strptime(s0 + "/00/00/00", '%Y/%m/%d/%H/%M/%S')
    #v2 = Comps.date_end(now)  datetime.strptime(s0 + "/23/59/59", '%Y/%m/%d/%H/%M/%S')
    gs = Game.objects.filter(Q(end=False)|Q(datestr=n))
    g_data = []
    for g in gs:
        g_data.append(
            {
                'hoshi': Comps.scoreHoshi(g.results),
                'score': Comps.scoreStr(g.results), 
                'game': g,
            },)
    
    params = {
        'now': n,
        'g_data': g_data,
    }
    return render(request, 'serve_counter/today.html',params)

#---opponent
@login_required(login_url='/serve_counter/')
def opponent(request):
    now = timezone.localtime(timezone.now())
    n = Comps.str_date(now)
    params={
        'now': n,
        'form':GameForm(),
    }

    if (request.method == 'POST'):
        opp_date = now
        opp_datestr = Comps.str_date(now)
        opp_name = request.POST['opp_name']
        players = Player.objects.all()    
        opp_players = ""
        opp_serves = ""
        for p in players:
            opp_players += p.name + ","  + str(p.grade) + "/"
            opp_serves += "0,0,0,0,0,0/"
        opp_players = opp_players[0:len(opp_players) - 1]
        opp_serves = opp_serves[0:len(opp_serves) - 1]
        opp_results = "0,0/0,0"
        game = Game(date=opp_date, \
                    datestr = opp_datestr, \
                    opponent=opp_name, \
                    end=False, \
                    players=opp_players, \
                    serves=opp_serves, \
                    results=opp_results)
        game.save()
        return redirect(to='/serve_counter/today')
    
    
    return render(request, 'serve_counter/opponent.html', params)

#---input_t (today)
@login_required(login_url='/serve_counter/')
def input_t(request, num):
    obj = Game.objects.get(id=num)
    if request.method == 'POST':
        if 'submit-End' in request.POST:
            request.session.pop('undo','')
            obj.end = True
            obj.save()
            return redirect(to='/serve_counter/today')
        if 'submit-Input' in request.POST:
            return redirect(to='/serve_counter/input_r/' + str(obj.id))
        if 'submit-Back' in request.POST:
            request.session.pop('undo','')
            return redirect(to='/serve_counter/today')
        if 'submit-Undo' in request.POST:
            k = request.session.pop('undo', '')
            if k == '':
                messages.error(request, '元に戻せません。')
                return redirect(to='/serve_counter/input_t/' + str(obj.id))
            else:
                obj.serves = Comps.serve_minus(obj.serves, k[1], k[2])
                obj.save()
                messages.success(request, 'ひとつ元に戻しました。')
                return redirect(to='/serve_counter/input_t/' + str(obj.id))
    
    pss = Comps.player_serves_1(obj.players, obj.serves)
    s = Comps.scoreStr(obj.results)
    ss = Comps.scores(obj.results)
    params={
        'game': obj,
        'players': pss,
        'score': s,
        'scores': ss,
    }
    return render(request, 'serve_counter/input_t.html', params)

#---input_r (results)
@login_required(login_url='/serve_counter/')
def input_r(request, num):
    game = Game.objects.get(id=num)
    alls = Comps.allscoreNums(game.results)
    f = GameResultForm()
    if request.method == 'POST':
        if "submit_Entry" in request.POST:
            s = Comps.strScore(request.POST)
            game.results = s
            game.save()
        return redirect(to = '/serve_counter/input_t/' + str(game.id))

    initial_dict = {}
    for i, s in enumerate(alls):
            initial_dict['score' + str(i) + '_0'] = alls[i][0]
            initial_dict['score' + str(i) + '_1'] = alls[i][1]
    f = GameResultForm(initial=initial_dict)        
    params={
        'game': game,
        'scores': alls,
        'form': f,
    }
    return render(request, 'serve_counter/input_r.html', params)

#---input_p (player)
@login_required(login_url='/serve_counter/')
def input_p(request, g_num, p_num):
    game = Game.objects.get(id=g_num)
    pname = Comps.player_name(game.players, p_num)
    serve = Comps.serve(game.serves, p_num)
    if request.method == 'POST':
        for i in range(6):
            k = 'serve_' + str(i)
            if k in request.POST.keys() :
                s = Comps.serve_plus(game.serves, p_num, i)
                game.serves = s
                game.save()
                request.session['undo'] = [g_num, p_num, i]
                return redirect(to='/serve_counter/input_t/' + str(g_num) ) 
    params = {
        'game': game,
        'player':pname,
        'serve':serve,
        'p_id':p_num,
    }
    return render(request, 'serve_counter/input_p.html', params)

#---look
@login_required(login_url='/serve_counter/')
def look(request):
    now = timezone.localtime(timezone.now())
    d = Comps.dateformstr_date(now)
    #form 初期化
    idict = {
        'from_date':d,
        'to_date':d,
    }
    #検索範囲　初期化
    from_date = datetime.strptime('2000/01/01','%Y/%m/%d')
    to_date = datetime.strptime('9999/12/31', '%Y/%m/%d')
    status = '全期間'
    if request.method == 'POST':
        if "submit-filter" in request.POST:
            fd = Comps.datedate_formstr(request.POST['from_date'])#0000-00-00 -> date
            td = Comps.datedate_formstr(request.POST['to_date'])
            from_date = Comps.date_start(fd)
            to_date = Comps.date_end(td)
            idict = {
                'from_date':request.POST['from_date'],
                'to_date':request.POST['to_date'],
            }
            status = '検索結果'
            #return redirect(to='/serve_counter/look')
        if "submit-clear" in request.POST:
            status = '全期間'
            #return redirect(to='/serve_counter/look')
        if "submit-view" in request.POST:
            gstr1 = Comps.dategetstr_formstr(request.POST['from_date'])
            gstr2 = Comps.dategetstr_formstr(request.POST['to_date'])
            
            return redirect(to='/serve_counter/look_summary/' + gstr1 + '/' + gstr2 + '/-3/')
        
    form = TermForm(initial=idict)
    games = Game.objects.filter(date__gte=from_date, date__lt=to_date, end=True)
    data_dict = {}
    for g in games:
        dstr = g.datestr
        filtered_games = Game.objects.filter(datestr=dstr, end=True)
        g_count = len(filtered_games)
        data_dict[dstr] = g_count
    
    data_dicts_rev = sorted(data_dict.items(), key=lambda x:x[0] , reverse=True)
    data = []
    for dd in data_dicts_rev:
        temp = {}
        temp['datestr'] = dd[0]
        temp['game_num'] = dd[1]
        temp['getstr'] = Comps.dategetstr_datestr(dd[0])
        data.append(temp)
    
    params={
        'form':form,
        'data':data,
        'status':status,
    }
    return render(request, 'serve_counter/look.html', params)

#---look_day
@login_required(login_url='/serve_counter/')
def look_day(request, gstr):
    dstr = Comps.datedatestr_getstr(gstr)
    games = Game.objects.filter(datestr=dstr, end=True)
    g_data = []
    wlds = [0, 0, 0]

    for g in games:
        temp = {
            'hoshi': Comps.scoreHoshi(g.results),
            'score': Comps.scoreStr(g.results), 
            'game': g,

        }
        g_data.append(temp)
        if temp['hoshi'] == "〇" :
            wlds[0] = wlds[0] + 1
        elif temp['hoshi'] == "×" :
            wlds[1] = wlds[1] + 1
        elif temp['hoshi'] == "△":
            wlds[2] = wlds[2] + 1
    
        
    params = {
        'gstrs':[gstr, gstr],
        'dstr': dstr,
        'wlds': wlds,
        #'games': games,
        'g_data': g_data,
    }
    return render(request, 'serve_counter/look_day.html',params)

#---look_summary
@login_required(login_url='/serve_counter/')
def look_summary(request, gstr1, gstr2, gnumstr):
    ps_data_1 = []
    gnum = int(gnumstr)
    s=[]
    ss=[]
    if gnum > 0:
        g = Game.objects.get(id=gnum)
        ps_data_1 = Comps.player_serves_1(g.players, g.serves)
        opp = g.opponent
        datestr = g.datestr
        s = Comps.scoreStr(g.results)
        ss = Comps.scores(g.results)
    else: # gnum=-1,-2
        from_date = Comps.date_start(Comps.datedate_getstr(gstr1))
        to_date = Comps.date_end(Comps.datedate_getstr(gstr2))
        games = Game.objects.filter(date__gte=from_date, date__lt=to_date)
        ps_data_2 = []
        if gnum == -1 or gnum == -2:
            datestr = Comps.str_date(from_date)
            opp = "全試合"
        else:
            datestr = Comps.str_date(from_date) + " ~ " + Comps.str_date(Comps.date_minussecond(to_date))
            opp = ""
        
        for i, g in enumerate(games):
            if i == 0:
                ps_data_2 = Comps.player_serves_2(g.players, g.serves) 
            else:
                ps_d2 = Comps.player_serves_2(g.players, g.serves)
                for j in range(len(ps_d2)):
                    for k in range(2,8):
                        ps_data_2[j][k] = ps_data_2[j][k] + ps_d2[j][k]
        for ps in ps_data_2:
            temp = []
            temp.append(ps[0])
            temp.append(ps[1])
            suc = int(ps[2])+int(ps[3])+int(ps[4])
            fai = int(ps[5])+int(ps[6])+int(ps[7])
            tot = suc + fai
            temp.append(suc)
            temp.append(fai)
            temp.append(tot)
            if tot > 0 :
                temp.append(100.0*suc/tot)
                temp.append(100.0*(int(ps[2])+int(ps[3]))/tot)  
            else:
                temp.append(0.0)
                temp.append(0.0)
            ps_data_1.append(temp)
    params={
        'gstrs': [gstr1, gstr2],
        'gnum': gnum,
        'ps_data': ps_data_1,
        'datestr': datestr,
        'opponent': opp,
        'score': s,
        'scores' : ss,
    }
    return render(request, 'serve_counter/look_summary.html', params)

#---look_detail
@login_required(login_url='/serve_counter/')
def look_detail(request, gstr1, gstr2, gnumstr):
    ps_data_2 = []
    gnum = int(gnumstr)
    gstrs = [gstr1, gstr2]
    s=[]
    ss=[]
    if gnum > 0:
        g = Game.objects.get(id=gnum)
        ps_data_2 = Comps.player_serves_2(g.players, g.serves)
        opp = g.opponent
        datestr = g.datestr
        s = Comps.scoreStr(g.results)
        ss = Comps.scores(g.results)
    else: # gnum=-1,-2
        from_date = Comps.date_start(Comps.datedate_getstr(gstr1))
        to_date = Comps.date_end(Comps.datedate_getstr(gstr2))
        games = Game.objects.filter(date__gte=from_date, date__lt=to_date)
        if gnum == -1 or gnum == -2:
            datestr = Comps.str_date(from_date)
            opp = "全試合"
        else:
            datestr = Comps.str_date(from_date) + " ~ " + Comps.str_date(Comps.date_minussecond(to_date))
            opp = ""
        
        for i, g in enumerate(games):
            if i == 0:
                ps_data_2 = Comps.player_serves_2(g.players, g.serves) 
            else:
                ps_d2 = Comps.player_serves_2(g.players, g.serves)
                for j in range(len(ps_d2)):
                    for k in range(2,8):
                        ps_data_2[j][k] = ps_data_2[j][k] + ps_d2[j][k] 
    
    params={
        'gstrs': gstrs,
        'gnum': gnum,
        'ps_data': ps_data_2,
        'datestr': datestr,
        'opponent': opp,
        'score': s,
        'scores' : ss,
    }
    return render(request, 'serve_counter/look_detail.html', params)

#---look_detail
@login_required(login_url='/serve_counter/')
def look_fix(request, gstr1, gstr2, gnumstr):
    gnum = int(gnumstr)
    g = Game.objects.get(id=gnum)
    ps_data_2 = Comps.player_serves_2(g.players, g.serves)
    if request.method == 'POST':
        if 'save_and_back' in request.POST:
            g.results = Comps.strScore(request.POST)
            g.serves = Comps.str_serves(request.POST)
            g.save()
            return redirect(to='/serve_counter/look_detail/' + gstr1 + "/" + gstr2 + "/" + gnumstr + "/")
    
        if 'submit-deldone' in request.POST:
            Game.objects.get(id=gnum).delete()    
            return redirect(to='/serve_counter/look_day/' + gstr1 + "/")
        
        if 'submit-delete' in request.POST:
            messages.error(request, g.opponent + ':削除しますがよろしいですか。')
            return redirect(to='/serve_counter/look_fix/' + gstr1 + "/" + gstr2 + "/" + gnumstr + "/")
        
    opp = g.opponent
    datestr = g.datestr
    alls = Comps.allscoreNums(g.results)
    initial_dict = {}
    for i, s in enumerate(alls):
        initial_dict['score' + str(i) + '_0'] = alls[i][0]
        initial_dict['score' + str(i) + '_1'] = alls[i][1]
    score_form = GameResultForm(initial=initial_dict)
    
    #initial_dicts = []
    #for ps in ps_data_2:
    #    temp={}
    #    for i in range(6):
    #        temp['serve_' + str(i)] = ps[i + 2]
    #    temp['serve_label'] = ps[1]
    #    initial_dicts.append(temp)

    serve_form = []
    for i, ps in enumerate(ps_data_2):
        tempform = {}
        tempform['serve_label'] = ps[1]
        for j in range(6):
            tempform['serve_' + str(j)] = {
                's_key':"form-" + str(i) + "-serve_" + str(j),
                's_value': ps[2+j]
            }
        serve_form.append(tempform)
            
    # formset = forms.formset_factory(form = ServeForm, extra=0)
    # serve_form = formset(initial=initial_dicts)

    players = Comps.players(g.players)
    params={
        'gstrs': [gstr1, gstr2],
        'gnum': gnum,
        'ps_data': ps_data_2,
        'datestr': datestr,
        'opponent': opp,
        'score_form': score_form,
        'serve_form': serve_form,
        'serve_player' :players
    }
    return render(request, 'serve_counter/look_fix.html', params)

