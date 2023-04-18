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
        t2 = operatingCompressiveForceThickness(tank['operating_moment'], tank['wind_moment'], tank['diameter'],
                                                tank['operating_compressive_force'], tank['wind_compressive_force'], tank['external_pressure'])
        t = max(t1, t2)
    elif tank['outdoor'] and not tank['tensile_force']:
        t = operatingCompressiveForceThickness()
    elif tank['tensile_force'] and not tank['outdoor']:
        t = tensileForceThickness(tank['operating_moment'], tank['diameter'],
                                  tank['tensile_force_value'], tank['internal_pressure'])
    else:
        t = idealThickness()


def idealThickness():
    """
    Ideal thickness formula
    """
    return 0


def tensileForceThickness(Ma, D, Fat, Pi):
    """
    Thickness formula when accounting for tensile force

    Parameters:
        Ma = Bending moment from operating loads
        D = inside diameter
        Xt = Ultimate axial tensile strength
        Fat = Axial Tensile force 
        Pi = internal pressure (probably 15)
        10 is design factor

    Formula:
        t = (Ma/(PI()*((D/2)^2)*(Xt/10))) + (Fat/(PI()*D*(Xt/10))) + ((P*D)/(4*(Xt/10)));
    """
    return (Ma/(math.pi*((D/2)**2)*(Xt/10))) + (Fat/(math.pi*D*(Xt/10))) + ((Pi*D)/(4*(Xt/10)))


def operatingCompressiveForceThickness(Ma, Mb, D, Fac, Fbc, Pe):
    """
    Compressive force will come from the snow/wind/siesmic loads in the other inputs.
    If there is a compressive force (Enter value in Newtons), 
    use these thickness formulas and take the greater value

    Parameters:
        Ma = Bending moment from operating loads
        Mb = Bending moment from wind snow or seismic loads
        D = inside diameter
        Xt = Ultimate axial tensile strength
        Fac = Axial compressive force (operating load)
        Fbc = Axial compressive force (wind snow or seismic)
        Pe = external pressure (atmospheric i assume)
        E2 = Axial Flexural Modulus
        E1 = Hoop tensile modulus
        10 is design factor 1
        5 is design factor 
    Formula:
        t1 = ((Ma + Mb)/(PI()*((D/2)^2)*(Xt/10))) + ((Fac+Fbc)/(PI()*D*(Xt/10))) + ((Pe*D)/(4*(Xt/10)));
        t2 = ((((Ma + Mb)/(PI()*((D/2)^2))) + ((Fac+Fbc)/(PI()*D)) + ((Pe*D)/4)) * ((5*(D/2))/(0.3*((E2*E1)^(1/2)))))^(1/2);
    """
    t1 = ((Ma + Mb)/(math.pi*((D/2)**2)*(Xt/10))) + \
        ((Fac+Fbc)/(math.pi*D*(Xt/10))) + ((Pe*D)/(4*(Xt/10)))
    t2 = ((((Ma + Mb)/(math.pi*((D/2)**2))) + ((Fac+Fbc)/(math.pi*D)) +
          ((Pe*D)/4)) * ((5*(D/2))/(0.3*((E2*E1)**(1/2)))))**(1/2)
    return max(t1, t2)
