# -*- coding: utf-8 -*-
# Triparty v1.14.0: אטרקציות (c="fun") לכל הערים. נבנה לפי Playbook סעיף 2א.
def F(ak,h,e,la,ln,dt,d,ho,co,ti,s,iq,story,more,facts,kd=None,ag=None,kids=None):
    return {"c":"fun","ak":ak,"h":h,"e":e,"la":la,"ln":ln,"d":d,"ho":ho,"co":co,"ti":ti,"s":s,"iq":iq,
            "th":None,"pv":None,"pvs":None,"st":"מדריך כתוב ביד","ag":ag,"kd":kd,"ko":0,"dt":dt,
            "x":{"level":"compact","story":story+"\nעוד על המקום\n"+more,"do":None,"tips":None,"reviews":None,
                 "verdict":None,"kids":kids,"facts":facts,"quiz":None,"timeline":None}}
def EV(h,e,k,rep,when,m,where,d,co,ti,la=None,ln=None,wd=None,kd=None,ag=None,ko=0):
    o={"h":h,"e":e,"k":k,"rep":rep,"when":when,"m":m,"wd":wd,"where":where,"d":d,"co":co,"ti":ti,"kd":kd,"ag":ag,"chk":1}
    if la is not None: o["la"]=la; o["ln"]=ln
    if ko: o["ko"]=1
    return o
