import math
# Variables
E1 = 5.700E+006  # Tensile Modulus (psi)
E2 = 1.240E+006  # Tensile Modulus (psi)
G12 = 5.400E+005  # Shear Modulus (psi)
v12 = 0.280  # Poisson's Ratio
CTE1 = 3.900E-006  # Thermal Expansion (in/in/F)
CTE2 = 1.170E-005  # Thermal Expansion (in/in/F)
CME1 = 0.000  # Moisture Expansion (in/in)
CME2 = 0.200  # Moisture Expansion (in/in)
Xt = 1.570E+005  # Tensile Strength (psi)
Xc = 9.000E+004  # Compressive Strength (psi)
Yt = 5.700E+003  # Tensile Strength (psi)
Yc = 1.860E+004  # Compressive Strength (psi)
S = 1.290E+004  # Shear Strength (psi)
g = 9.81  # Gravity (m/s^2)
dEglass = 158.6  # Density of E-Glass (lb/ft^3)


def calculateTank(tank):
    """
    Calculate the tank

    Input:
        tank = Tank object containing all the information from the form
    """
    # TODO: dont change the actual value
    p = tank['internal_pressure']
    tank['internal_pressure'] = float(tank['internal_pressure']) + \
        float(tank['liquid_height'])*float(tank['specific_gravity'])
    t = 0
    if tank['tensile_force'] and tank['outdoor']:
        t1 = tensileForceThickness(
            tank['operating_moment'], tank['diameter'], tank['tensile_force_value'])
        t2 = operatingCompressiveForceThickness(tank)
        t = max(t1, t2)
    elif tank['outdoor'] and not tank['tensile_force']:
        t = operatingCompressiveForceThickness(tank)
    elif tank['tensile_force'] and not tank['outdoor']:
        t = tensileForceThickness(
            tank['operating_moment'], tank['diameter'], tank['tensile_force_value'])

    t += idealThickness(tank['diameter'], tank['internal_pressure'])
    tank['internal_pressure'] = p
    tank['thickness'] = t + tank['corrosion_barrier_thickness'] + \
        tank['corrosion_liner_thickness']
    return tank


def idealThickness(D=0.0, Pi=0.0):
    """
    Ideal thickness formula
        used when none of the modifiers are selected

    Parameters:
        D = inside diameter
        Pi = internal pressure
        Eh = Hoop Tensile Modulus (one of the inputs)
    Formula:
        t = (PD)/(2*(0.001*Eh))
    Returns:
        t = thickness
    """
    # check if we should use the default hoop tensile modulus
    return (float(Pi)*float(D)*10)/(2*Xt)


def tensileForceThickness(Ma=0.0, D=0.0, Fat=0.0):
    """
    Thickness formula when accounting for tensile force

    Parameters:
        Ma = Bending moment from operating loads
        D = inside diameter
        Fat = Axial Tensile force 
        10 is design factor

    Formula:
        t = ((Ma*8.8507457916)/(PI()*((D/2)^2)*(Xt/10))) + ((Fat*0.2248089431)/(PI()*D*(Xt/10)))
    """
    return ((float(Ma))/(math.pi*((float(D)/2)**2)*(Xt/10))) + ((float(Fat))/(math.pi*float(D)*(Xt/10)))


def operatingCompressiveForceThickness(tank):
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
        load = mass of human load
        10 is design factor 1
        5 is design factor
        Ce = exposure factor GIVEN no unit
        Ct = Thermal factor GIVEN no unit
        Is = Importance factor GIVEN no unit
        Pg = ground snow load GIVEN lb/ft^2
        D = Tank Diameter GIVEN in
        qh = velocity pressure for all surfaces at height GIVEN 
        G = gust effect factor GIVEN
        Cp = External pressure coefficient GIVEN
        GCpi = Internal pressure coefficient GIVEN
        liveload = human Live load GIVEN lb
        Fa = Seismic Constraint GIVEN
        Ss = seismic constraint GIVEN
        deadload = deadload form objects GIVEN lb
        height = tank height in
    Formula:
        t1 = (((Ma) + Mb)/(PI()*((D/2)^2)*(Xt/10))) + (((Fac)+Fbc)/(PI()*D*(Xt/10))) + ((Pe*D)/(4*(Xt/10)));
        t2 = (((((Ma) + Mb)/(PI()*((D/2)^2))) + (((Fac)+Fbc)/(PI()*D)) + ((Pe*D)/4)) * ((5*(D/2))/(0.3*((E2*E1)^(1/2)))))^(1/2);
    """
    # get values
    nozzle = (2.0*math.pi*(float(tank['diameter'])/24.0)*(float(
        tank['nozzle_length'])/12.0)*(float(tank['nozzle_thickness'])/12.0))*dEglass
    Ma = float(tank['operating_moment'])
    D = float(tank['diameter'])
    Fac = float(tank['compressive_force'])
    Pe = float(tank['external_pressure'])
    height = float(tank['height'])
    deadLoad = float(tank['dead_load']) + nozzle
    liveLoad = float(tank['live_load'])
    Ce = float(tank['snow_Ce'])
    Ct = float(tank['snow_Ct'])
    Is = float(tank['snow_Is'])
    Pg = float(tank['snow_Pg'])
    qh = float(tank['wind_qh'])
    G = float(tank['wind_G'])
    Cp = float(tank['wind_Cp'])
    GCpi = float(tank['wind_GCpi'])
    Fa = float(tank['seismic_Fa'])
    Ss = float(tank['seismic_Ss'])

    # The compressive force due to wind/snow/seismic is given by:
    # Fbc = (0.7*(Ce)*(Ct)*(Is)*(Pg))*(PI()*((1.25*(D*0.0833333)/2)^2)) + (qh*(G*Cp - GCpi)*PI()*((1.25*(D*0.0833333))/2)^2) + (liveload) + 0.2*((2/3)*Fa*Ss)*deadload;
    Fbc = (0.7*(Ce)*(Ct)*(Is)*(Pg))*(math.pi*((1.25*(D*0.0833333)/2)**2)) + (qh*(G*Cp - GCpi)
                                                                             * math.pi*((1.25*(D*0.0833333))/2)**2) + (liveLoad) + 0.2*((2/3)*Fa*Ss)*deadLoad
    # Bending moment from wind snow or seismic loads
    Mb = Fbc * height
    t1 = (((Ma) + Mb)/(math.pi*((D/2)**2)*(Xt/10))) + \
        (((Fac)+Fbc)/(math.pi*D*(Xt/10))) + ((Pe*D)/(4*(Xt/10)))
    t2 = (((((Ma) + Mb)/(math.pi*((D/2)**2))) + (((Fac) +
                                                  Fbc)/(math.pi*D)) + ((Pe*D)/4)) * ((5*(D/2))/(0.3*((E2*E1)**(1/2)))))**(1/2)
    return max(t1, t2)
