import numpy as np
import matplotlib.pyplot as plt

moldata = np.loadtxt('sirius_data.dat')

for i in range(len(moldata)):
    pKa = moldata[i,1]
    logp0 = moldata[i,2]
    logp1 = moldata[i,3]

    p0 = 10**(+logp0)
    p1 = 10**(+logp1)
    ka = 10**(-pKa)

    pHexp = [1.0,1.2,2.0,3.0,4.0,5.0,6.0,6.5,7.0,7.4,8.0,9.0,10.0,11.0,12.0]
    pH = np.array(pHexp)
    cH = 10**(pH)
#print(-np.log10(cH))
    logD = np.log10((p0 + p1*cH*ka)/(1.0 + cH*ka))
#logD = logp1 - 10**(pH-pKa*np.ones(len(pH)))

#logDref = np.loadtxt('sirius_data_SM41.dat')
    
    logDexp = np.loadtxt('logD_sirius_SM%d.dat'%moldata[i,0])
    plt.figure()
    plt.plot(pHexp,logDexp,label='Experimental')
    plt.plot(pH,logD,label='Predicted from Eqn')
   # plt.plot(logDref[:,0],logDref[:,1],label='Sirius data')
   # plt.ylim(-6,1)
    plt.legend(fontsize=14)
    plt.xlabel('pH',fontsize=16)
    plt.ylabel('logD',fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
   # plt.show()
    plt.savefig('lipophilicity_SM%d.png'%moldata[i,0],dpi=120,bbox_inches='tight')
