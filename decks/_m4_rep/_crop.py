import os
from PIL import Image, ImageFilter, ImageChops
A=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','_m4_assets')
C=os.path.join(os.path.dirname(os.path.abspath(__file__)),'crops')
def crop(src,name,box,f=12,ell=False):
    im=Image.open(os.path.join(A,src+'.webp')).convert('RGBA').crop(box)
    w,h=im.size
    m=Image.new('L',(w,h),0)
    from PIL import ImageDraw
    d=ImageDraw.Draw(m)
    if ell: d.ellipse((f,f,w-f,h-f),fill=255)
    else: d.rectangle((f,f,w-f-1,h-f-1),fill=255)
    m=m.filter(ImageFilter.GaussianBlur(f/2.2))
    im.putalpha(m)
    im.save(os.path.join(C,name+'.png'))
if __name__=='__main__':
    L=[
    ('i_optimal1','o1_router',(300,520,460,635)),
    ('i_optimal1','o1_router_s',(1390,470,1515,560)),
    ('i_optimal1','o1_cloud',(1540,452,1665,555)),
    ('i_optimal1','o1_bgp',(25,355,130,452),True),
    ('i_optimal1','o1_ospf',(25,462,130,558),True),
    ('i_optimal1','o1_rip',(25,566,130,662),True),
    ('i_optimal1','o1_isis',(25,668,130,765),True),
    ('i_optimal1','o1_search',(942,648,1036,735),True),
    ('i_optimal2','o2_router',(212,148,330,228)),
    ('i_optimal2','o2_cloud',(1285,240,1525,380),False),
    ('i_mech','m_copper',(8,285,200,435)),
    ('i_mech','m_sfp',(1005,300,1200,435)),
    ('i_mech','m_device',(625,520,1050,645)),
    ('i_mech','m_chip',(432,748,570,845)),
    ('i_mech','m_port',(698,748,885,845)),
    ('i_mech','m_c1',(1070,722,1182,838),True),
    ('i_mech','m_c2',(1250,722,1372,838),True),
    ('i_mech','m_c3',(1440,722,1572,838),True),
    ('i_table_b','t_router',(350,452,500,562)),
    ('i_principles','p_router',(364,722,466,795)),
    ('i_principles','p_trophy',(1012,270,1114,372),True),
    ('i_principles','p_db',(1012,386,1114,488),True),
    ('i_principles','p_shield',(1012,502,1114,604),True),
    ('i_principles','p_bolt',(1012,618,1114,722),True),
    ('i_principles','p_gear',(1012,738,1114,842),True),
    ]
    for t in L: crop(*t[:3],ell=(len(t)>3 and t[3]))
