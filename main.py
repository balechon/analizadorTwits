import numpy as np
import re
from unicodedata import normalize
import pandas as pd
p_positivas =["excelente","gran","positivo","quiero","bueno","inteligente"]
p_neutras = ["aprender","estudio","platzi","ocurre","saludo","asesora"]
p_negativas = ["muerte","luto","ignorante","perdida"]

palabras=p_positivas+p_neutras+p_negativas

def clean_twit(twit):   
    twit = re.sub(
    	r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
    	normalize( "NFD", twit), 0, re.I
    )
    return twit.replace("!","").replace(",","").lower().split(" ")

def calc_w(twit_limpio):
    w=np.zeros(len(palabras))
    for palabra in twit_limpio:
        for pal in palabras:
            if palabra==pal:
               w[palabras.index(pal)]+=1   
    return w
    
def calc_s(twit_limpio):
    positiva =0
    negativa=0
    neutra=0
    for palabra in twit_limpio:
        for posi in p_positivas:
            if palabra==posi:
                positiva+=1
        for nega in p_negativas:
            if palabra== nega:
                negativa+=1
        for neu in p_neutras:
            if palabra==neu:
                neutra+=1
    s=[positiva,neutra, negativa]
    return np.array(s)

def avg_w(twit_limpio):
    w=calc_w(twit_limpio)
    calidad = (np.ones(len(palabras))/len(palabras))
    return  np.dot(w,calidad)

def avg_s(twit_limpio):
    w=calc_w(twit_limpio)
    c_posi = (np.ones(len(p_positivas))/len(p_positivas))
    c_neu =  (np.ones(len(p_neutras))/len(p_neutras))
    c_nega = (np.ones(len(p_negativas))/len(p_negativas))
    s0=np.dot( c_posi, w[:len(p_positivas)]  ) 
    s1=np.dot( c_neu, w[len(p_positivas):len(p_neutras)+len(p_positivas)] )
    s2=np.dot (c_nega, w[len(p_neutras)+len(p_positivas):] )
    return np.array([s0,s1,s2])

def score(twit_limpio):
    s= calc_s(twit_limpio)
    aux =  np.array([1,0,-1])
    return np.dot(aux,s.transpose())


def run(twetts):
    resut=[]
    for i in twetts:
        twet=clean_twit(i)
        aux=[f't{twetts.index(i)+1}',avg_w(twet),avg_s(twet)[0],avg_s(twet)[1],avg_s(twet)[2],score(twet)]
        resut.append(aux)
    df = pd.DataFrame(resut, columns=["Tweet","Calidad","Calidad Positiva","Calidad Neutra","Calidad Negativa","Score"])
    print(df)

if __name__=="__main__":
    t1 = "Gran mexicano y excelente en su área, su muerte es una enorme perdida y debería ser luto nacional!!!"
    t2 = "Vaya señora que bueno que se asesora por alguien inteligente no por el ignorante del Gatt"
    t3 = "Se me ocurre y sin ver todos los videos de Plazti que me informéis por dónde empiezo. Entiendo que os tendría que decir quién soy y que quiero, vamos conocerme para asesorarme bien. Un saludo"
    t4 = "Soy docente universitario, estoy intentando preparar mis clases en modo platzi bien didáctico, (le llamo modo noticiero), descargue una plataforma gratuita de grabación y transmisión de vídeo, se llama Obs estudio!bueno la sigo remando con sus funciones pero sé que saldrá algo!"
    t5 = "Cómo easter egg dejo mi propio mensaje que malo fue tener una perdida economica al menos platzi me ayuda"
    twetts=[t1,t2,t3,t4,t5]
    run(twetts)
    