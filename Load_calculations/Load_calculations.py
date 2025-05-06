#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 00:00:00 2021
@author: Fred Chun

Version 1.0 
@editor: Nat Espinosa on 23 of May 2023

Version 2.0 as of 8 of November 2024
@editor: Alexander Boldis

Version 3.0 as of 13 of January 2025
@editor: Nadim Hatoum
"""

#Import argparse, numpy, pandas, and plotly libraries
import argparse
from ast import arg
import numpy as np
import pandas as pd
from plotly import graph_objs as go
# import plotly.io as pio

# pio.renderers.default = "pdf"


def main():

    # See details at
    # http://www.aspirespace.org.uk/downloads/Rocket%20vehicle%20loads%20and%20airframe%20design.pdf

    # Rocket's documentation
    ### Sets up arguments to input the "Rocket_info", "Rocket_COP", "Rocket_CL", "Rocket_CD" 
    ### and "Open_Rocket"  files  (first four from AeroLAB and last from Open_Rocket

    parser = argparse.ArgumentParser()
    parser.add_argument('--Rocket_info', type=str, help='input desired rockets main information file', required=True)
    parser.add_argument('--Rocket_COP', type=str, help='input desired rockets COP file', required=True)
    parser.add_argument('--Rocket_CL', type=str, help='input desired rockets lift coefficient file', required=True)
    parser.add_argument('--Rocket_CD', type=str, help='input desired rockets drag coefficient file', required=True)
    parser.add_argument('--Open_Rocket', type=str, help='input desired rockets OpenRocket information file', required=True)
    args = parser.parse_args()

    ### Sets a data frame with the following values as the headers: 
    ### "Length", "Reference Area", "Rocket_part", "mass_m", "x_cm". Next two lines converts string values to numeric values
    rocket_info_df = pd.read_csv(args.Rocket_info, sep=",", header=None, skiprows=1, names=["Length", "Reference Area", "Rocket_part", "mass_m", "x_cm"])
    rocket_info_df["Length"] = pd.to_numeric(rocket_info_df["Length"], errors='coerce')
    rocket_info_df["Reference Area"] = pd.to_numeric(rocket_info_df["Reference Area"], errors='coerce')  

    # Length [m] Note: please double check that the information is in [cm]
    ### Obtains the first length of the rocket and sets the reference area as a circle of this diameter
    length_l = rocket_info_df.iloc[0, 0]/100

    # Reference area
    s = np.pi * ((rocket_info_df.iloc[0, 1]/100/2)**2)

    # Rocket Parts
    ### Extracts each rocket part's name, and their respective mass and centre of mass
    rocket_parts_df = rocket_info_df.iloc[:, [2, 3, 4]]

    # AeroLab data
    ### Extracts the centre of pressure, coefficient of lift slope, and coefficient of drag from the AeroLAB files
    aerolab_x_cp_df = pd.read_csv(args.Rocket_COP, sep="\s+", header=None, skiprows=1)
    aerolab_cl_alpha_df = pd.read_csv(args.Rocket_CL, sep="\s+", header=None, skiprows=1)
    aerolab_cd_df = pd.read_csv(args.Rocket_CD, sep="\s+", header=None, skiprows=1)

    # Max q data       --> manually change <--
    ### Extracts density, velocity of rocket, and velocity of wind from OpenRocket file and calculates angle of attack (alpha)
    ### based on it using arctan(v_wind/U_inf) to obtain an angle in radians    
    open_rocket_df = pd.read_csv(args.Open_Rocket, sep=',', header=None, skiprows=1)
    
    rho_inf = open_rocket_df.iloc[0,0] # density [kg m^-3]
    velocity_v_inf = open_rocket_df.iloc[0,1] # velocity [m s^-1]
    velocity_v_wind_gust = open_rocket_df.iloc[0,2] # wind gust velocity [m s^-1]  

    angle_of_attack_alpha = np.arctan(velocity_v_wind_gust / velocity_v_inf)  # [rad]
    
    # Lift coefficient curve slopes [rad^-1]
    ### Extracts the lift coefficient curve slopes of the nosecone, wing, and body/wing of rocket
    nose_body_cl_alpha = aerolab_cl_alpha_df.iloc[:,2].max()
    wing_cl_alpha = aerolab_cl_alpha_df.iloc[:,3].max()
    body_wing_cl_alpha = aerolab_cl_alpha_df.iloc[:,4].max()

    # Lift coefficients
    ### Calculates the lift coefficients of the nosecone, wing, and body/wing of the rocket by multiplying the previous values by alpha
    nose_body_cl = nose_body_cl_alpha * angle_of_attack_alpha
    wing_cl = wing_cl_alpha * angle_of_attack_alpha
    body_wing_cl = body_wing_cl_alpha * angle_of_attack_alpha

    # Lifts [N]
    ### Calculates the lift of the nosecone, wing and body/wing of the rocket by calculating 
    ### Lx = 0.5 rho U^2 CL,x and then summing them up for the total lift generated
    nose_body_lift_l = 0.5 * rho_inf * (velocity_v_inf ** 2) * s * nose_body_cl
    wing_lift_l = 0.5 * rho_inf * (velocity_v_inf ** 2) * s * wing_cl
    body_wing_lift_l = 0.5 * rho_inf * (velocity_v_inf ** 2) * s * body_wing_cl

    rocket_lift_l = nose_body_lift_l + wing_lift_l + body_wing_lift_l

    # Drag coefficient
    ### Extracts the maximum drag coefficient of the rocket
    rocket_cd = aerolab_cd_df.iloc[:,1].max()

    # Drag [N]
    ### Calculates the drag coefficient of the rocket by multiplying the previous value by alpha
    rocket_drag = 0.5 * rho_inf * (velocity_v_inf ** 2) * s * rocket_cd

    # Centres of pressure [m]
    ### Converts the centre of pressure and nosecone, wing and body/wing of the rocket to metres from centimetres and summing them up
    nose_body_x_cp = aerolab_x_cp_df.iloc[-1, 2]/ 100
    wing_x_cp = aerolab_x_cp_df.iloc[-1, 3] / 100
    body_wing_x_cp = aerolab_x_cp_df.iloc[-1, 4] / 100

    # Masses [kg]
    ### Extracts the rocket masses of the nosecone, wing and body/wing of the rocket to get total rocket mass
    rocket_parts_mass_m = rocket_parts_df["mass_m"]

    rocket_mass_m = sum(rocket_parts_mass_m)

    # Centres of mass [m]
    ### Extracting the centre of mass (CoM) of the nosecone, wing and body/wing of the rocket by and
    #### using it to calculate the centre of mass of the rocket by calculating sum(mx*xCM,x)/ sum(mx)
    rocket_parts_x_cm = rocket_parts_df["x_cm"]/100

    rocket_x_cm = sum(rocket_parts_mass_m * rocket_parts_x_cm) / sum(
        rocket_parts_mass_m)

    # Moments of inertia [kg m^2]
    ### Calculates the moment of inertia of the nosecone, wing and body/wing of the rocket by calculating 
    ### Ix = mx(xCP,x - xCM,x)2 and then summing it up to get total moment of inertia
    rocket_parts_i = rocket_parts_mass_m * (
            rocket_parts_x_cm - rocket_x_cm) ** 2

    rocket_i = sum(rocket_parts_i)

    # Moments [N m]
    ### Calculates the moments of the nosecone, wing and body/wing of the rocket by calculating 
    ### Mx = Lx(xCP,x - xCM,x) and then summing it up to get total moment
    nose_body_moment_m = nose_body_lift_l * (nose_body_x_cp - rocket_x_cm)
    wing_moment_m = wing_lift_l * (wing_x_cp - rocket_x_cm)
    body_wing_moment_m = body_wing_lift_l * (body_wing_x_cp - rocket_x_cm)

    rocket_moment_m = nose_body_moment_m + wing_moment_m + body_wing_moment_m

    # Angular acceleration [rad s^-2]
    ### Calculates angular acceleration using a_ang = M_TOT / I_TOT
    angular_acceleration_alpha = rocket_moment_m / rocket_i

    # Accelerations [m s^-2]
    ### Calculates the total acceleration of the rocket using a_x = L_x / m_x + a_ang (xCP,x - xCM,x)
    rocket_parts_a = (rocket_lift_l / rocket_mass_m) + (
            angular_acceleration_alpha * (rocket_parts_x_cm - rocket_x_cm))

    # Point loads [N]
    ### Calculates the point loads of the rocket using F_x = - m_xa_x
    rocket_parts_p = -(rocket_parts_mass_m * rocket_parts_a)

    # Summed Mass [kg]
    ### Calculates the mass of every component of the rocket as well as the components above them 
    rocket_summed_mass = np.add.accumulate(rocket_parts_mass_m)

    # Compressive Loads [N]
    ### Calculates the compressive loads of the rocket using Fc_x = -m_x(a_x + g) - D
    rocket_parts_c = -(rocket_summed_mass * (rocket_parts_a + 9.81)) - rocket_drag

    # Load diagram
    ### Produces a load diagram plotting the values from Line 113 vs x_cp and displays it
    loads_d = {
        "x": np.array(
            rocket_parts_x_cm.tolist() + [nose_body_x_cp, wing_x_cp,
                                          body_wing_x_cp] + [0, length_l]),
        "p": np.array(
            rocket_parts_p.tolist() + [nose_body_lift_l, wing_lift_l,
                                       body_wing_lift_l] + [0, 0]),
        "section": rocket_parts_df["Rocket_part"].tolist()
                    + ["Nose", "Wing", "Body/Wing", "Start", "End"],
    }
    loads_df = pd.DataFrame(data=loads_d).sort_values(by=["x"])

    loads_x = loads_df["x"]  # [m]
    loads_p = loads_df["p"]  # [N]
    section_labels = loads_df["section"]  # Section labels for parts

    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=loads_x, y=loads_p, text=section_labels, textposition="outside",)
    ) 
    fig.update_layout(
        xaxis_range=[0, length_l],
        xaxis_title="Position, x [m]",
        yaxis_title="Load, P [N]",
        title="Load Diagram",
    )
    fig.update_traces(marker=dict(line=dict(width=10, color="blue")))
    fig.show()

    # Shear diagram
    ### Produces a shear diagram plotting the cumulative sum of the loads (i.e. sheer stresses) vs x_cp and displays it
    shears_d = {
        "x": np.repeat(np.copy(loads_x), 2)[1:-1],
        "shear_v": np.repeat(np.add.accumulate(np.copy(loads_p)), 2)[:-2],
    }
    shears_df = pd.DataFrame(data=shears_d)

    shears_x = shears_df["x"]  # [m]
    shears_shear_v = shears_df["shear_v"]  # [N]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=shears_x, y=shears_shear_v))
    fig.update_layout(
        xaxis_range=[0, length_l],
        xaxis_title="Position, x [m]",
        yaxis_title="Shear, V [N]",
        title="Shear Diagram",
    )
    fig.show()

    # Axial Forces diagram
    ### Produces a compressive forces diagram plotting the compressive forces vs x_cp and displays it
    compressive_d = {
        "x": np.array(rocket_parts_x_cm.tolist()),
        "compressive_v": np.array(rocket_parts_c.tolist()),
    }
    compressive_df = pd.DataFrame(data=compressive_d)

    compressive_x = compressive_df["x"]  # [m]
    compressive_compress_v = compressive_df["compressive_v"]  # [N]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=compressive_x, y=compressive_compress_v))
    fig.update_layout(
        xaxis_range=[0, length_l],
        xaxis_title="Position, x [m]",
        yaxis_title="Axial Force, T [N]",
        title="Axial Force Diagram",
    )
    fig.show()

    # Moment diagram
    ### Produces a moment diagram plotting the loads times the x_cp (i.e. shear stresses) vs x_cp and displays it
    moments_d = {
        "x": np.copy(loads_x),
        "moment_m": np.concatenate((np.zeros(1), np.add.accumulate(
            np.concatenate(
                (np.diff(np.copy(loads_x)), np.zeros(1))) * np.add.accumulate(
                np.copy(loads_p)))))[:-1],
    }
    moments_df = pd.DataFrame(data=moments_d)

    moments_x = moments_df["x"]  # [m]
    moments_moment_m = moments_df["moment_m"]  # [N m]


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=moments_x, y=moments_moment_m))
    fig.update_layout(
        xaxis_range=[0, length_l],
        xaxis_title="Position, x [m]",
        yaxis_title="Moment, M [N m]",
        title="Moment Diagram",
    )
    fig.show()

    return True

if __name__ == '__main__':
    main()
