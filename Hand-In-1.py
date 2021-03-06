import numpy as np
import matplotlib.pyplot as plt

def factorial(k):
   h = 1
   k = k
   while k>1:
      h = h*k
      k -= 1
   return h

def Poisson(labda, k):
   labda = np.float64(labda)
   k = np.float64(k)
   return (labda**k)*np.exp(-labda)/(factorial(k))

def LCG(x):
   a = 3202034522624059733
   c = 4354685564936845319
   m = 2**64
   return (a*x+c)%m

def XOR_shift(x):
   a1, a2, a3 = np.uint64(21), np.uint64(35), np.uint64(4)
   x = np.uint64(x)
   x = x ^ (x >> a1)
   x = x ^ (x << a2)
   x = x ^ (x >> a3)
   return x

def RNG(length, norm = True):
   global seed

   randomnumbers = []
   state = seed
   
   for i in range(length):
      state = LCG(state)
      randomnumbers.append(XOR_shift(state))

   randomnumbers = np.array(randomnumbers)

   if norm == True:
      randomnumbers = np.array(randomnumbers)/(2**64)

   seed = state
   if length == 1:
      return randomnumbers[0]
   else:
      return randomnumbers.tolist()

def densityprofileint(x, N_sat=1):
   return N_sat*((x/b)**(a-3))*np.exp(-(x/b)**c)*x**2

def densityprofile(x, N_sat=1):
   return N_sat*((x/b)**(a-3))*np.exp(-(x/b)**c)

def ndprofile(x, N_sat=1):
   return 4*np.pi*A*densityprofileint(x, N_sat)

def rootfunction(x, N_sat=100):
   return ndprofile(x, N_sat)-1.33/2

def extmidpoint(func, edges, n):
   h = (edges[1]-edges[0])/n
   integration = 0

   for i in range(n):
       integration += func(edges[0]+(i+0.5)*h)
   integration = h*integration

   return integration

def extmidpointromberg(func, edges, n, N):
   s = [[] for i in range(N)]
   s[0].append(extmidpoint(func, edges, n))

   for i in range (1,N):
      n = 2*n
      s[0].append(extmidpoint(func, edges, n))
   
   for j in range(N-1):
      for i in range(N-(j+1)):
         s[j+1].append(s[j][i+1]+(s[j][i+1]-s[j][i])/(-1+4**(j+1)))

   return s[-1][0]

def Linearinterpolation(interpolatedrange,numbers,values):
   interpolatedvalues = []
   linslope = []

   for i in range(len(numbers)-1):
      linslope.append((values[i+1]-values[i])/(numbers[i+1]-numbers[i]))

   def linearinterpolation(x,i):
      if i<6:
         return (linslope[i]*(x-numbers[i])+values[i])
      else:
         return (linslope[5]*(x-numbers[5])+values[5])

   for interpolatednumber in interpolatedrange:
      rangefound = False
      indexrange = 0
      while rangefound!=True:
         if interpolatednumber >= numbers[-1]:
            indexrange = len(numbers)-2
            rangefound = True
            interpolatedvalues.append(linearinterpolation(interpolatednumber,indexrange))
         elif numbers[indexrange] <= interpolatednumber < numbers[indexrange+1]:
            rangefound = True
            interpolatedvalues.append(linearinterpolation(interpolatednumber,indexrange))
         else:
            indexrange+=1

   return interpolatedvalues

def nevi(x,i,j,numbers,p):
   return ((x-numbers[j])*p[i][j+1]-(x-numbers[j+1+i])*p[i][j])/(numbers[j+1+i]-numbers[j])

def Nevillesinterpolation(interpolationrange,numbers,values):
   interpolatedvalues = []

   for interpolatednumber in interpolatedrange:
      M=len(numbers)
      p=[[] for i in range(7)]
      p[0]=values
      while M>1:
         for j in range(M-1):
            order = 1+len(numbers)-M
            p[order].append(nevi(interpolatednumber,order-1,j,numbers,p))
         M-=1
      interpolatedvalues.append(p[len(numbers)-1][0])

   return interpolatedvalues

def centraldifference(func,x,h):
   return (func(x+h)-func(x-h))/(2*h)

def riddler(func,x,h,d,m):
   D=[[] for i in range(m)]
   D[0].append(centraldifference(func,x,h))
   if m>1:
      for i in range(m-1):
         D[0].append(centraldifference(func,x,h/(d**(i+1))))
   for j in range(m-1):
      riddlercombine(D,j,d,m)
   return D[-1][-1]

def riddlercombine(D,j,d,m):
   for i in range(m-j-1):
      D[j+1].append((d**(2*(j+1))*D[j][i+1]-D[j][i])/(d**(2*(j+1))-1))

def analyticaldrvdensityprofile(x):
   return densityprofile(x)*((1/x)*(a-3-c*(x/b)**c))

def argsort(x):
   if type(x) is np.ndarray:
      xd = x[:].tolist() #Create a copy of the array so the actual array doesn't get sorted
   else:
      xd = x[:]
   y = [i for i in range(len(x))]
   argsortinner(xd,y)
   return y

def argsortinner(xd, y, start=0, end=None): #When sorting the array, also keeps track of how the indices swap around
   if end == None:
      end = len(xd)-1
   if start < end:
      index = argpivotsort(xd,y,start,end)
      argsortinner(xd,y,start,index-1)
      argsortinner(xd,y,index+1,end)

def argpivotsort(xd,y,start,end):
   pivot = xd[end]
   i = start-1
   for j in range(start,end):
      if xd[j] <= pivot:
         i += 1
         xd[i], xd[j] = xd[j], xd[i]
         y[i], y[j] = y[j], y[i]
   xd[i+1], xd[end] = xd[end], xd[i+1]
   y[i+1], y[end] = y[end], y[i+1]
   return i+1

def pivotsort(x,start,end):
   pivot = x[end]
   i = start-1
   for j in range(start,end):
      if x[j] <= pivot:
         i += 1
         x[i], x[j] = x[j], x[i]
   x[i+1], x[end] = x[end], x[i+1]
   return i+1

def Quicksort(x, start=0, end=None):
   if end == None:
      end = len(x)-1
   if start < end:
      index = pivotsort(x,start,end)
      Quicksort(x,start,index-1)
      Quicksort(x,index+1,end)

def secant(func, interval, criterium, maxiter):
   x_0 = interval[0]
   x_1 = interval[1]
   if func(x_0)*func(x_1)>=0:
      return None
   for i in range(maxiter):
      x_2 = (1+func(x_0)/(func(x_1)-func(x_0)))*x_1-(func(x_0)/(func(x_1)-func(x_0)))*x_0
      if abs(func(x_2)) <= criterium:
         return x_2      
      elif func(x_0)*func(x_2)<0:
         x_0 = x_0
         x_1 = x_2
      elif func(x_1)*func(x_2)<0:
         x_0 = x_1
         x_1 = x_2
      else:
         return None
   return None

def Linear3dinterpolator(A,a,b,c):
   #Find indices of small cube surrounding the point
   i = int((a-1.1)//0.1)
   j = int((b-0.5)//0.1)
   k = int((c-1.5)//0.1)
   
   #Combine 4 known points into intermediate values
   p1 = Linearinterpolation([c],[1.5+0.1*k,1.5+0.1*(k+1)],[A[i,j,k],A[i,j,k+1]])[0]
   p2 = Linearinterpolation([c],[1.5+0.1*k,1.5+0.1*(k+1)],[A[i,j+1,k],A[i,j+1,k+1]])[0]
   p3 = Linearinterpolation([c],[1.5+0.1*k,1.5+0.1*(k+1)],[A[i+1,j,k],A[i+1,j,k+1]])[0]
   p4 = Linearinterpolation([c],[1.5+0.1*k,1.5+0.1*(k+1)],[A[i+1,j+1,k],A[i+1,j+1,k+1]])[0]

   #Combine the 4 intermediate values into two closer intermediate values
   p5 = Linearinterpolation([a],[1.1+0.1*i,1.5+0.1*(i+1)],[p1,p3])[0]
   p6 = Linearinterpolation([a],[1.1+0.1*i,1.5+0.1*(i+1)],[p2,p4])[0]

   #Comebine the two closer intermediate values to the actual interpolation value
   p7 = Linearinterpolation([b],[0.5+0.1*j,0.5+0.1*(j+1)],[p5,p6])[0]

   return p7

def opensatgals(textfile):
   """
   Skip the header, create a list of lists where in each sublist the coordinates of each halo is stored.
   """
   fh = open(textfile)
   for _ in range(3):
      next(fh)
   halo_index = -1
   for line in fh:
      numberofhaloes = int(line.rstrip('\n'))
      haloes = [[] for i in range(numberofhaloes)]
      break
   for line in fh:
      line = line.rstrip('\n')
      if line == '#':
         halo_index += 1
      else:
         haloes[halo_index].append(line)
   fh.close()
   
   haloes = [[[float(s) for s in haloes[i][j].split('   ')] for j in range(len(haloes[i]))] for i in range(len(haloes))]
   return haloes

if __name__ == '__main__':
   seed = 2
   print("The seed is: " + str(seed))

   print("Poisson function for (lambda,k) = (1,0) is: " + str(Poisson(1,0)))
   print("Poisson function for (lambda,k) = (5,10) is: " + str(Poisson(5,10)))
   print("Poisson function for (lambda,k) = (3,21) is: " + str(Poisson(3,21)))
   print("Poisson function for (lambda,k) = (2.6,40) is: " + str(Poisson(2.6,40)))

   RNG_list = RNG(1000)
   RNG_list2 = RNG(10**6)

   n_RNG_list = np.array(RNG_list[:-1])
   np1_RNG_list = np.array(RNG_list[1:])

   fig, axs = plt.subplots(1, 2, sharey=False, tight_layout=True)

   axs[0].scatter(n_RNG_list, np1_RNG_list, marker="o", color=(1,0,0), facecolors='none')
   axs[1].hist(RNG_list2, bins = 20, range = (0,1))

   xlabel = ['Combined RNG n', 'Random number generated by combined RNG']
   ylabel = ['Combined RNG n+1', 'Counts']

   i=0
   for ax in axs:
      ax.set(xlabel=xlabel[i], ylabel=ylabel[i])
      i+=1

   fig.savefig('./plots/RNG-test-results')

   a = (RNG(1)*1.4)+1.1
   b = (RNG(1)*1.5)+0.5
   c = (RNG(1)*2.5)+1.5
   
   integration = extmidpointromberg(densityprofileint, [0,5], 10**2, 4)
   A = (1/(4*np.pi))*(1/integration)
   
   print("a, b, c, A = " + str(a) + ", " + str(b) + ", " + str(c) + ", " + str(A))

   numbers = np.log10(np.array([10**-4, 10**-2, 10**-1, 1, 5]))
   densityvalues = np.log10(np.array([densityprofile(10**-4), densityprofile(10**-2), densityprofile(10**-1), densityprofile(1), densityprofile(5)]))
   interpolatedrange = np.linspace(-4,0.69897,100)

   linearvalues = Linearinterpolation(interpolatedrange,numbers,densityvalues)
   Nevillesvalues = Nevillesinterpolation(interpolatedrange,numbers,densityvalues)
   realvalues = np.log10(densityprofile(10**interpolatedrange))
   
   fig2, axs2 = plt.subplots()
   axs2.plot(interpolatedrange, Nevillesvalues, label='Nevilles interpolation', color = 'orange')
   axs2.plot(interpolatedrange, linearvalues, label='Linear interpolation', color = 'blue')
   axs2.plot(interpolatedrange, realvalues, label='real values', color = 'black')
   axs2.scatter(numbers,densityvalues,marker="o", label='Data points', color=(1,0,0))
   axs2.set(xlabel='log10(x)', ylabel='log10(Density profile)')
   axs2.legend()
   fig2.savefig('./plots/Log-Log_plot_interpolation')

   derivative_at_b = riddler(densityprofile,b,0.1,2,6)
   analyticaldrv_at_b = analyticaldrvdensityprofile(b)
   
   print("The analytical derivative at b is: %.15f" % analyticaldrv_at_b)

   print("The numerically solved derivative at b is: %.15f" % derivative_at_b)

   p_u1 = np.array(RNG(100))
   p_u2 = np.array(RNG(100))

   theta = np.arccos(1-2*p_u1)
   phi = 2*np.pi*p_u2

   x_accepted_densityprofile = []
   while len(x_accepted_densityprofile)<100:
      x = RNG(1)*5
      y = RNG(1)*1.33
      if y <= ndprofile(x):
         x_accepted_densityprofile.append(x)

   satellites100 = np.column_stack((x_accepted_densityprofile,phi,theta))

   print("(r,phi,theta) for 100 satellites are: ")
   print(satellites100)
   
   haloes = [[] for i in range(1000)]
   
   #1000 haloes with 100 satellites each.
   for i in range(1000):
      x_local_accepted_densityprofile = []
      while len(x_local_accepted_densityprofile)<100:
         x = RNG(1)*5
         y = RNG(1)*1.33
         if y <= ndprofile(x):
            x_local_accepted_densityprofile.append(x)
      
      haloes[i] = x_local_accepted_densityprofile

   flattened_haloes = [item for sublist in haloes for item in sublist]
   Quicksort(flattened_haloes)
   
   fig3, axs3 = plt.subplots()

   logbins = np.logspace(np.log10(10**-4),np.log10(5),20)
   weights = []

   for i in range(len(flattened_haloes)):
      j=0
      bin_found = False
      while bin_found == False:
         if logbins[j] <= flattened_haloes[i] < logbins[j+1]:
            bin_found = True
            weights.append(1/(1000*(logbins[j+1]-logbins[j])))
         else:
            j += 1

   axs3.hist(flattened_haloes,bins=logbins, log=True)
   axs3.plot(flattened_haloes, ndprofile(np.array(flattened_haloes),N_sat=100))
   axs3.set(xscale='log', xlabel='log10(x)', ylabel='log10(density)')
   fig3.savefig('./plots/Density_profile_Haloes_Log-Log2')

   """
   Solve the Equation N(x)-(y/2)=0 for x and where y is the maximum of N(x)
   """
 
   root1 = secant(rootfunction, [10**-4,10**-1], 10**-6, 10**6)
   root2 = secant(rootfunction, [10**-1,5], 10**-6, 10**6)

   roots = [root1,root2]

   print("The roots are:")
   print(roots)
   
   #Clarify what is meant exactly as the radial bin with the most number of galaxies?
   
   maxradialbin = [logbins[15], logbins[16]]

   haloesmaxbin = [[] for i in range(1000)]
   
   for i in range(len(haloes)):
      for j in range(len(haloes[i])):
         if maxradialbin[0] <= haloes[i][j] <= maxradialbin[1]:
            haloesmaxbin[i].append(haloes[i][j])

   flat_haloesmaxbin = [item for sublist in haloesmaxbin for item in sublist]
   index_16 = int(0.16*len(flat_haloesmaxbin)) - 1
   index_84 = int(0.84*len(flat_haloesmaxbin)) - 1
   Quicksort(flat_haloesmaxbin)
   a_16 = flat_haloesmaxbin[index_16]
   a_84 = flat_haloesmaxbin[index_84]

   #Don't quite understand what's going here, have to figure out what needs to be binned and what the
   #x-axis is supposed to be, since it is supposed to approximate a Poisson distribution.
   haloesmaxbin_counts = [len(haloesmaxbin[i]) for i in range(1000)]
   
   binshere = np.unique(haloesmaxbin_counts)
   
   kspace = np.array(range(1,np.max(binshere)+1))

   tra = []
   for i in range (1,np.max(binshere)+1):
      tra.append(Poisson(46.333,i))

   fig4, axs4 = plt.subplots()
   axs4.plot(kspace,1000*np.array(tra))
   axs4.hist(haloesmaxbin_counts,bins=binshere)
   axs4.set(xlabel='Number of galaxies in maximum radial bin', ylabel='Number of haloes')
   fig4.savefig('./plots/Counts_of_bins')

   arange = np.linspace(1.1,2.5,15)
   brange = np.linspace(0.5,2,16)
   crange = np.linspace(1.5,4,26)

   A3d = np.array([[[0 for k in range(len(crange))] for j in range(len(brange))] for i in range(len(arange))])
   A3d = A3d.astype('float64')

   for i in range(len(arange)):
      for j in range(len(brange)):
         for k in range(len(crange)):
            a, b, c = arange[i], brange[j], crange[k]
            localint = extmidpointromberg(densityprofileint, [0,5], 10**2, 4)
            A3d[i,j,k] += (1/(4*np.pi))*(1/localint)

   interpolationarray_k = np.zeros((len(arange),len(brange),len(crange)-1))
   interpolationarray_k.astype('float64')

   Linear3dinterpolator(A3d,1.15,0.55,1.55)
   
   haloes = opensatgals('Data/satgals_m14.txt')

   x14 = [[x[0] for x in haloes[i]] for i in range(len(haloes))]

   flattened_x14 = [item for sublist in x14 for item in sublist]

   fig5, axs5 = plt.subplots()

   logbins = np.logspace(np.log10(10**-4),np.log10(5),20)
   
   axs5.hist(flattened_x14,bins=20,weights=[(1./223.) for i in range(len(flattened_x14))])
   axs5.set(xlabel='x', ylabel='counts')
   fig5.savefig('./plots/Densityprofile_readin_gal')
