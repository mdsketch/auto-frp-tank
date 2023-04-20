import math
# Variables
E1 = 3.931e+010  # Tensile Modulus (Pa)
E2 = 8.552e+009  # Tensile Modulus (Pa)
G12 = 3.724e+009  # Shear Modulus (Pa)
v12 = 0.280  # Poisson's Ratio
CTE1 = 7.020e-006  # Thermal Expansion (m/m/C)
CTE2 = 2.106e-005  # Thermal Expansion (m/m/C)
CME1 = 0.000  # Moisture Expansion (m/m)
CME2 = 0.200  # Moisture Expansion (m/m)
Xt = 1.083e+009  # Tensile Strength (Pa)
Xc = -6.207e+008  # Compressive Strength (Pa)
Yt = 3.931e+007  # Tensile Strength (Pa)
Yc = -1.283e+008  # Compressive Strength (Pa)
S = 8.897e+007  # Shear Strength (Pa)
g = 9.81  # Gravity (m/s^2)


def calculateTank(tank):
    """
    Calculate the tank

    Input:
        tank = Tank object containing all the information from the form
    """
    t = 0
    if tank['tensile_force'] and tank['outdoor']:
        t1 = tensileForceThickness(tank['operating_moment'], tank['diameter'],
                                   tank['tensile_force_value'], tank['internal_pressure'])
        t2 = operatingCompressiveForceThickness(tank['operating_moment'], tank['compressive_force'], tank['diameter'], tank['external_pressure'],
                                                tank['live_load'], tank['dead_load'], tank['snow_pressure'], tank['wind_speed'], tank['height'])
        t = max(t1, t2)
    elif tank['outdoor'] and not tank['tensile_force']:
        t = operatingCompressiveForceThickness(tank['operating_moment'], tank['compressive_force'], tank['diameter'], tank['external_pressure'],
                                               tank['live_load'], tank['dead_load'], tank['snow_pressure'], tank['wind_speed'], tank['height'])
    elif tank['tensile_force'] and not tank['outdoor']:
        t = tensileForceThickness(tank['operating_moment'], tank['diameter'],
                                  tank['tensile_force_value'], tank['internal_pressure'])
    else:
        t = idealThickness(
            tank['diameter'], tank['internal_pressure'], tank['hoop_tensile_modulus'])
    print(t)
    return t


def idealThickness(D=0.0, Pi=0.0, Eh=0.0):
    """
    Ideal thickness formula
        used when none of the modifiers are selected

    Parameters:
        D = inside diameter
        Pi = internal pressure
        Eh = Hoop Tensile Modulus (one of the inputs)
    Formula:
        t = (PD)/(2*(0.001*Eh))
    """
    return (Pi*D)/(2*(0.001*Eh))


def tensileForceThickness(Ma=0.0, D=0.0, Fat=0.0, Pi=0.0):
    """
    Thickness formula when accounting for tensile force

    Parameters:
        Ma = Bending moment from operating loads
        D = inside diameter
        Fat = Axial Tensile force 
        Pi = internal pressure (probably 15)
        10 is design factor

    Formula:
        t = (Ma/(PI()*((D/2)^2)*(Xt/10))) + (Fat/(PI()*D*(Xt/10))) + ((P*D)/(4*(Xt/10)));
    """
    return (Ma/(math.pi*((D/2)**2)*(Xt/10))) + (Fat/(math.pi*D*(Xt/10))) + ((Pi*D)/(4*(Xt/10)))


def operatingCompressiveForceThickness(Ma=0.0, Fac=0.0, D=0.0, Pe=0.0, liveLoad=0.0, deadLoad=0.0, msnow=0.0, vwind=0.0, height=0.0):
    """
    Compressive force will come from the snow/wind/siesmic loads in the other inputs.
    If there is a compressive force (Enter value in Newtons), 
    use these thickness formulas and take the greater value

    Parameters:
        Ma = Bending moment from operating loads
        D = inside diameter
        Fac = Axial compressive force (operating load)
        Pe = external pressure (atmospheric i assume)
        msnow = mass of snow
        vwind = velocity of wind
        height = tank height
        mpeople = mass of human load
        10 is design factor 1
        5 is design factor 
    Formula:
        t1 = ((Ma + Mb)/(PI()*((D/2)^2)*(Xt/10))) + ((Fac+Fbc)/(PI()*D*(Xt/10))) + ((Pe*D)/(4*(Xt/10)));
        t2 = ((((Ma + Mb)/(PI()*((D/2)^2))) + ((Fac+Fbc)/(PI()*D)) + ((Pe*D)/4)) * ((5*(D/2))/(0.3*((E2*E1)^(1/2)))))^(1/2);
    """
    # The compressive force due to wind/snow/seismic is given by:
    # Fbc = (msnow*9.81) + (0.5*1.225*(vwind^2))*(2*PI()*radius*height) + (mpeople*9.81);
    Fbc = (msnow*g) + (0.5*1.225*(vwind**2))*(math.pi*D*height) + (liveLoad*g)
    # Bending moment from wind snow or seismic loads
    Mb = Fbc * height
    t1 = ((Ma + Mb)/(math.pi*((D/2)**2)*(Xt/10))) + \
        ((Fac+Fbc)/(math.pi*D*(Xt/10))) + ((Pe*D)/(4*(Xt/10)))
    t2 = ((((Ma + Mb)/(math.pi*((D/2)**2))) + ((Fac+Fbc)/(math.pi*D)) +
          ((Pe*D)/4)) * ((5*(D/2))/(0.3*((E2*E1)**(1/2)))))**(1/2)
    return max(t1, t2)
