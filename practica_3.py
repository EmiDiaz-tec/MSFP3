# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import control as ctrl
import matplotlib.pyplot as plt

# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5 #tiempo obtenido
N= round(tend/dt)+1
t= np.linspace(t0,tend,N)
u =np.zeros(N); u[round(1/dt):round(2/dt)]=1


# Funcion de transferencia para Control
a,R,Cs,Cp= 0.25, 100, 10E-6,100E-6
num= [Cs*R,1-a]
den = [R*(Cp + Cs),1]
sys_control = ctrl.tf(num, den)
print(f"Funcion de transferencia Control:{sys_control}\n")

# Funcion de transferencia para Control
a,R,Cs,Cp= 0.25, 10000, 10E-6,100E-6
num= [Cs*R,1-a]
den = [R*(Cp + Cs),1]
sys_caso = ctrl.tf(num, den)
print(f"Funcion de transferencia Caso:{sys_caso}\n")


# Componentes del controlador
kP, kI=  0.3258, 2442.000353
numPID = [kP,kI]
denPID = [1,0]
PID = ctrl.tf(numPID, denPID)
print(f"Funcion de transferencia del controlador: {PID} \n")


# Sistema de control en lazo cerrado
sysPID=ctrl.feedback(ctrl.series(PID,sys_caso),1,sign =-1)
print(f"Funcion de transferencia en lazo cerrado: {sysPID} \n")

#Colores
clr1 = np.array([80,3,192])/255
clr2 = np.array([171,3,169])/255
clr3 = np.array([255,213,30])/255
clr4 = np.array([0, 102, 204]) / 255


# Respuestas: Simulaciones numéricas
Fsx = ctrl.forced_response(sys_control,t , u).outputs
Fsy = ctrl.forced_response(sys_caso,t , u).outputs  
PIDu = ctrl.forced_response(sysPID,t , Fsx).outputs

# Configuración de la figura única
fg = plt.figure(1)
fg.set_size_inches(w, h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.plot(t, u, '-', color=clr1, linewidth=1.5, label='F(t)')
plt.plot(t, Fsx, '-.', color=clr2, linewidth=1.8, label='FsX(t): Control')
plt.plot(t, Fsy, ':', color=clr3, linewidth=2.0, label='FsY(t): Caso')
plt.plot(t, PIDu, '--', color=clr4, linewidth=2.0, label='PID(t): Tratamiento')

# Configuración de ejes y rejilla
plt.xlim(0, 10)
plt.xticks(np.arange(0, 11, 1))
plt.ylim(-0.1, 1.2)
plt.yticks(np.arange(-0.1, 1.3, 0.1))

plt.xlabel('t [s]')
plt.ylabel('F(t) [V]')
plt.title('Respuesta Control, Caso y Tratamiento')
plt.grid(True, linestyle=':', alpha=0.6)

# Leyenda inferior centrada
plt.legend(bbox_to_anchor=(0.5, -0.25), loc='center', ncol=4, frameon=False)

plt.tight_layout()
plt.show()

# Guardar figura en formato PDF
fg.savefig('respuesta_practica2_python.pdf', bbox_inches='tight')