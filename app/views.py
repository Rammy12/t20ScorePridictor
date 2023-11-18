from django.shortcuts import render
import pickle
import numpy as np
import pandas as pd



model_path_t20='model/pipet20men.pkl'
pipe_t20=pickle.load(open(model_path_t20,'rb'))
def t20_pridict(request):
    if request.method=='POST':
       batting_team=request.POST['batting_team']
       bowling_team=request.POST['bowling_team']
       city=request.POST['city']
       current_score=request.POST['current_score']
       overs=request.POST['overs']
       wickets=request.POST['wickets']
       last_five=request.POST['last_five']
       fields=[batting_team,bowling_team,city,current_score,overs,wickets,last_five]
       if batting_team==bowling_team:
           return render(request,'index.html',{'Error':'Batting Team And Bowling Team Can not Be same'})
       if not None in fields:
            overs=float(overs)
            if overs>=5 and overs<=19:
                wickets=float(wickets)
                current_score=float(current_score)
                last_five=float(last_five)
                balls_left=120-(overs*6)
                wickets_left=10-wickets
                crr=current_score/overs
                input=pd.DataFrame([[batting_team,bowling_team,city,current_score,balls_left,wickets_left,crr,last_five]],columns=['batting_team','bowling_team','city','current_score','balls_left','wickets_left','crr','last_five'])
                result=pipe_t20.predict(input)[0]
                result=np.round(result,0)
                result_dict={'Batting_team':batting_team,
                             'Bowling_team':bowling_team,
                             'Current_Runs':current_score,
                             'overs':overs,
                             'wickets':wickets,
                             'result':result}
                return render(request,'index.html',{'dict':result_dict})
            else:
                return render(request,'index.html',{'Error':'Overs Must be Between 5 and 19'}) 
       return render(request,'index.html',{'Error':'Please Type Correct Input'})          
    return render(request,'index.html')

