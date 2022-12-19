# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 13:13:17 2022

@author: SYSTEM
"""

import math
def ISA(altitude):
    #Standard Atmosphere
    h0 = 0
    p0 = 101325
    T0 = 288.15
    rho0 = 1.225

    R = 287
    g = 9.80665

    #Troposphere
    h0 = 0
    a0 = -6.5E-3

    #Tropopause
    h1 = 11000
    a1 = 0

    #Stratosphere1
    h2 = 20000
    a2 = 1E-3

    #Stratosphere2
    h3 = 32000
    a3 = 2.8E-3

    #Stratopause
    h4 = 47000
    a4 = 0

    #Mesosphere1
    h5 = 51000
    a5 = -2.8E-3

    #Mesosphere2
    h6 = 71000
    a6 = -2.0E-3

    #Mesopause
    h7 = 84852
    a7 = 0

    #Calculations
    hlist   = []
    hlist.append(h0)
    Tlist   = []
    Tlist.append(T0)
    plist   = []
    plist.append(p0)
    rholist = []
    rholist.append(rho0)

    #Functions
    def temperature(Told,hold,hnew,a):
        Tnew = Told + a*(hnew-hold)
        Tlist.append(Tnew)
        return Tnew
        
            
    def pressure(Told,Tnew,a,pold,hold,hnew):
        if a != 0:
            pnew = pold*(Tnew/Told)**(-g/(a*R))
            plist.append(pnew)
            return pnew
        else:
            pnew = pold*math.e**((-g/(R*Tnew))*(hnew-hold))
            plist.append(pnew)
            return pnew
        
    def density(p,T):
        rhonew = p/(R*T)
        rholist.append(rhonew)
        return rhonew 

    i = 0
    while i == 0:
        #Troposphere
        if altitude > h1:
            T1 = temperature(T0,h0,h1,a0)
            p1 = pressure(T0,T1,a0,p0,h0,h1)
            rho1 = density(p1,T1)
            hlist.append(h1)
        else:
            T1 = temperature(T0,h0,altitude,a0)
            p1 = pressure(T0,T1,a0,p0,h0,altitude)
            rho1 = density(p1,T1)
            hlist.append(altitude)
            i = 1
            break
        #Tropopause
        if altitude > h2:
            T2 = temperature(T1,h1,h2,a1)
            p2 = pressure(T1,T2,a1,p1,h1,h2)
            rho2 = density(p2,T2)
            hlist.append(h2)
        else:
            T2 = temperature(T1,h1,altitude,a1)
            p2 = pressure(T1,T2,a1,p1,h1,altitude)
            rho2 = density(p2,T2)
            hlist.append(altitude)
            i = 1
            break
        #Stratosphere1
        if altitude > h3:
            T3 = temperature(T2,h2,h3,a2)
            p3 = pressure(T2,T3,a2,p2,h2,h3)
            rho3 = density(p3,T3)
            hlist.append(h3)
        else:
            T3 = temperature(T2,h2,altitude,a2)
            p3 = pressure(T2,T3,a2,p2,h2,altitude)
            rho3 = density(p3,T3)
            hlist.append(altitude)
            i = 1
            break    
        #Stratosphere2
        if altitude > h4:
            T4 = temperature(T3,h3,h4,a3)
            p4 = pressure(T3,T4,a3,p3,h3,h4)
            rho4 = density(p4,T4)
            hlist.append(h4)
        else:
            T4 = temperature(T3,h3,altitude,a3)
            p4 = pressure(T3,T4,a3,p3,h3,altitude)
            rho4 = density(p4,T4)
            hlist.append(altitude)
            i = 1
            break      
        #Stratopause
        if altitude > h5:
            T5 = temperature(T4,h4,h5,a4)
            p5 = pressure(T4,T5,a4,p4,h4,h5)
            rho5 = density(p5,T5)
            hlist.append(h5)
        else:
            T5 = temperature(T4,h4,altitude,a4)
            p5 = pressure(T4,T5,a4,p4,h4,altitude)
            rho5 = density(p5,T5)
            hlist.append(altitude)
            i = 1
            break      
        #Mesosphere1
        if altitude > h6:
            T6 = temperature(T5,h5,h6,a5)
            p6 = pressure(T5,T6,a5,p5,h5,h6)
            rho6 = density(p6,T6)
            hlist.append(h6)
        else:
            T6 = temperature(T5,h5,altitude,a5)
            p6 = pressure(T5,T6,a5,p5,h5,altitude)
            rho6 = density(p6,T6)
            hlist.append(altitude)
            i = 1
            break      
        #Mesosphere2
        if altitude > h7:
            T7 = temperature(T6,h6,h7,a6)
            p7 = pressure(T6,T7,a6,p6,h6,h7)
            rho7 = density(p7,T7)
            hlist.append(h7)
        else:
            T7 = temperature(T6,h6,altitude,a6)
            p7 = pressure(T6,T7,a6,p6,h6,altitude)
            rho7 = density(p7,T7)
            hlist.append(altitude)
            i = 1
            break      
        #Mesopause
        T8 = temperature(T7,h7,altitude,a7)
        p8 = pressure(T7,T8,a7,p7,h7,altitude)
        rho8 = density(p8,T8)
        hlist.append(altitude)
        i = 1
        break 
    T = Tlist[-1]
    rho = rholist[-1]
    c = (1.4*R*T)**(1/2)
    return T, rho, c
    