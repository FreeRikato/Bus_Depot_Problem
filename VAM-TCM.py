import timeit
start = timeit.default_timer()
import pandas as pd
import numpy as np
import random
from collections import defaultdict
randomlist = []
df_demand = {}
random.seed(12) # Use the same random seed
for i in range(0,20):   # 20 depots
    n = random.randint(100,150) # Depot Capacity
    randomlist.append(n)
for i in range(20):
    df_demand['D'+str(i+1)] = randomlist[i]
print(df_demand , "\n" , randomlist)
sum = 0
for (k,v) in df_demand.items():
    sum = sum + v
sum
df_supply = {}
for i in range(sum):
    df_supply[i] = 1.0
df_supply


# In[6]:


np.random.seed(12) # Use the same random seed
df_dkm = pd.DataFrame(np.random.uniform(0.5,40, size=(sum,20))).astype(float)


# In[7]:


random.seed(12) # Use the same random seed
age_b = []
for i in range(sum):
    n = random.randint(1,3) #Only to generate integer values inclusive of 1 & 3
    age_b.append(n)
    
age = {}
for i in range(len(age_b)):
    age[i] = age_b[i] 
    


# In[8]:


kpl = []
co2 = []
random.seed(12) # Use the same random seed
for (k,v) in age.items():
    if (v==1):
        n = random.uniform(5.1,6)
        m = round(random.uniform(515, 524), 2)
        kpl.append(n)
        co2.append(m)
    if (v==2):
        n = random.uniform(4.1,5)
        m = round(random.uniform(525, 534), 2)
        kpl.append(n)
        co2.append(m)
    if (v==3):
        n = random.uniform(3.1,4)
        m = round(random.uniform(535, 540), 2)
        kpl.append(n)
        co2.append(m)
        


# In[9]:


fc_kpl = {}
for i in range(sum):
    fc_kpl[i] =(111/ kpl[i])

co2_c = {}
for i in range(sum):
    co2_c[i] =(0.00118642*co2[i])
    


# In[10]:


random.seed(12) # Use the same random seed
doc = {}
for i in range(0,20):
    n = random.uniform(50,100)
    doc[i] = n
    
df_tdkom = pd.DataFrame(np.zeros(df_dkm.shape))
for i in range(len(df_dkm.columns)):
    for j in range(len(df_dkm.index)):
        df_tdkom[i][j] = df_dkm[i][j]*fc_kpl[j] + df_dkm[i][j]*co2_c[j] + doc[i]
#df_tdkom


# In[11]:


df_tdkom.columns = [("D"+str(i)) for i in range(1,21)]

df_tdkom.head()

dk = df_tdkom.transpose()


# In[14]:


costs_t = dk.to_dict()
colsn = sorted(df_demand.keys())
res = dict((k, defaultdict(int)) for k in costs_t)
g = {}
for x in df_supply:
    # print(x)
    # print(costs_t[x])
    g[x] = sorted(costs_t[x].keys(), key=lambda g: costs_t[x][g])
for x in df_demand:
    g[x] = sorted(costs_t.keys(), key=lambda g: costs_t[g][x])


while g:
    d = {}
    # print(df_supply,dic)
    for x in df_demand:
        d[x] = (costs_t[g[x][1]][x] - costs_t[g[x][0]][x]) if len(g[x]) > 1 else (costs_t[g[x][0]][x])
    s = {}
    for x in df_supply:
        s[x] = (costs_t[x][g[x][1]] - costs_t[x][g[x][0]])  if len(g[x]) > 1 else costs_t[x][g[x][0]]
    f = max(d, key=lambda n: d[n])
    t = max(s, key=lambda n: s[n])
    t, f = (f, g[f][0]) if d[f] >= s[t] else (g[t][0], t)
    v = min(df_supply[f], df_demand[t])
    # print(f,t)
    # print(v)
    res[f][t] += v
    df_demand[t] -= v

    if df_demand[t] == 0:
        for k, n in df_supply.items():
            if n != 0:
                g[k].remove(t)
        del g[t]
        del df_demand[t]
    df_supply[f] -= v
    if df_supply[f] == 0:
        for k, n in df_demand.items():
            if n != 0:
                g[k].remove(f)
        del g[f]
        del df_supply[f]

# print("G",g)
cost = 0
# cols = sorted(df_demand.keys())
# print(costs)
for g in sorted(costs_t):
    # print (g, " ",)
    # print("S")
    for n in colsn:
        y = res[g][n]
        # print("YESS",y)
        if y != 0:
            pass
            # print (y,)
        cost += y * costs_t[g][n]
stop = timeit.default_timer()
execution_time = stop - start

print("Program Executed in "+str(execution_time))