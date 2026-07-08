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

Version 4.0 as of 8 of July 2026
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

# To run paste code in terminal use:
# python3 load_calculations_ANNOTATED.py --Rocket_info Discovery_part_info.dat --Rocket_COP Discovery_Centres_of_Pressure.DAT --Rocket_CL Discovery_Lift_Coefficient_Curve_Slopes.DAT --Open_Rocket Open_rocket_info.dat --Rocket_CD Discovery_Cd.dat

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

    # Max q data 
    open_rocket_df = pd.read_csv(args.Open_Rocket, sep=',', header=None, skiprows=1)
    
    rho_inf = open_rocket_df.iloc[0,0] # density [kg m^-3]
    velocity_v_inf = open_rocket_df.iloc[0,1] # velocity [m s^-1]
    T_inf = open_rocket_df.iloc[0,3] # temperature [K]

    angle_of_attack_alpha = 0.0872665  # [rad]

    # ------------------ NEW PHYSICS FIX ------------------
    # Calculate Mach Number to interpolate AeroLAB data
    speed_of_sound = np.sqrt(1.4 * 287 * T_inf)  # [m/s] approx. Adjust this based on your altitude's temperature
    mach_number = velocity_v_inf / speed_of_sound
    
    # Interpolate Lift coefficient curve slopes [rad^-1] based on Mach number
    nose_body_cl_alpha = np.interp(mach_number, aerolab_cl_alpha_df.iloc[:,0], aerolab_cl_alpha_df.iloc[:,2])
    wing_cl_alpha = np.interp(mach_number, aerolab_cl_alpha_df.iloc[:,0], aerolab_cl_alpha_df.iloc[:,3])
    body_wing_cl_alpha = np.interp(mach_number, aerolab_cl_alpha_df.iloc[:,0], aerolab_cl_alpha_df.iloc[:,4])

    # Interpolate Centres of pressure [m] based on Mach number
    nose_body_x_cp = np.interp(mach_number, aerolab_x_cp_df.iloc[:,0], aerolab_x_cp_df.iloc[:,2]) / 100
    wing_x_cp = np.interp(mach_number, aerolab_x_cp_df.iloc[:,0], aerolab_x_cp_df.iloc[:,3]) / 100
    body_wing_x_cp = np.interp(mach_number, aerolab_x_cp_df.iloc[:,0], aerolab_x_cp_df.iloc[:,4]) / 100

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

    # Interpolate Drag coefficient based on Mach number
    rocket_cd = np.interp(mach_number, aerolab_cd_df.iloc[:,0], aerolab_cd_df.iloc[:,1])

    # Drag [N]
    ### Calculates the drag force through the classical drag equation (Using the maximum frontal reference area)
    rocket_drag = 0.5 * rho_inf * (velocity_v_inf ** 2) * s * rocket_cd
    print("Rocket's total drag: ", rocket_drag)
    
    # Masses [kg]
    ### Extracts the rocket masses of the nosecone, wing and body/wing of the rocket to get total rocket mass
    rocket_parts_mass_m = rocket_parts_df["mass_m"]

    rocket_mass_m = sum(rocket_parts_mass_m)

    # Centres of mass [m]
    ### Extracting the centre of mass (CoM) of the nosecone, wing and body/wing of the rocket by and
    #### using it to calculate the centre of mass of the rocket by calculating sum(mx*xCM,x)/ sum(mx)
    rocket_parts_x_cm = rocket_parts_df["x_cm"]/100
    rocket_x_cm = sum(rocket_parts_mass_m * rocket_parts_x_cm) / rocket_mass_m

    # Moments of inertia [kg m^2]
    # ------------------ NEW PHYSICS FIX ------------------
    # Approximate local moment of inertia for each part assuming a solid cylinder: I_cm = (1/12) * m * L^2
    # This prevents the script from underestimating I by treating huge parts as point-masses.
    rocket_parts_length_m = rocket_info_df["Length"] / 100
    rocket_parts_i_local = (1/12) * rocket_parts_mass_m * (rocket_parts_length_m ** 2)
    
    # Parallel Axis Theorem: I_total = I_local + m * (x_cp - rocket_x_cm)^2
    rocket_parts_i = rocket_parts_i_local + rocket_parts_mass_m * (rocket_parts_x_cm - rocket_x_cm) ** 2
    rocket_i = sum(rocket_parts_i)
    # -----------------------------------------------------

    # Moments [N m]
    ### Calculates the moments of the nosecone, wing and body/wing of the rocket by calculating 
    ### Mx = Lx(xCP,x - rocket_x_cm) and then summing it up to get total moment
    nose_body_moment_m = nose_body_lift_l * (nose_body_x_cp - rocket_x_cm)
    wing_moment_m = wing_lift_l * (wing_x_cp - rocket_x_cm)
    body_wing_moment_m = body_wing_lift_l * (body_wing_x_cp - rocket_x_cm)

    rocket_moment_m = nose_body_moment_m + wing_moment_m + body_wing_moment_m

    # Angular acceleration [rad s^-2]
    ### Calculates angular acceleration using a_ang = M_TOT / I_TOT
    angular_acceleration_alpha = rocket_moment_m / rocket_i

    #print("Rocket's angular acceleration: ", angular_acceleration_alpha)

    # Accelerations [m s^-2]
    # ------------------ NEW PHYSICS FIX ------------------
    # Lateral (transverse) acceleration is driven solely by lift (ignoring minor lateral gravity components)
    rocket_lateral_acc = rocket_lift_l / rocket_mass_m

    # Axial (longitudinal) acceleration is driven by thrust (0 here), drag, and gravity
    rocket_axial_acc = (-rocket_drag - rocket_mass_m * 9.81) / rocket_mass_m

    # The lateral acceleration at each component's CoM includes the rigid-body rotational contribution
    rocket_parts_lateral_a = rocket_lateral_acc + (angular_acceleration_alpha * (rocket_parts_x_cm - rocket_x_cm))

    # Point loads [N]
    # Shear diagrams are ONLY driven by lateral/transverse forces. Weight is excluded here.
    rocket_parts_inertial_lateral_p = -(rocket_parts_mass_m * rocket_parts_lateral_a)
    rocket_parts_p = rocket_parts_inertial_lateral_p # Transverse point loads

    # Intertial torque [N m]
    rocket_parts_inertial_torque = rocket_parts_i_local * angular_acceleration_alpha

    # Summed Mass [kg]
    rocket_summed_mass = np.add.accumulate(rocket_parts_mass_m)
    
    # Drag on Individual Components [N] and Summed Drag [N]
    rocket_parts_drag = rocket_drag * (rocket_parts_length_m / length_l)
    rocket_summed_drag = np.add.accumulate(rocket_parts_drag)

    # Compressive Loads [N]
    # Compressive loads are ONLY driven by axial forces (Axial inertial resistance + Gravity + Drag)
    rocket_parts_c = -(rocket_summed_mass * (rocket_axial_acc + 9.81)) - rocket_summed_drag
    # -----------------------------------------------------
 
# ------------------ STRUCTURAL JOINTS DICTIONARY ------------------
    structural_joints = {
        0.4510: "Nose/Rec Bay Joint",
        1.0100: "Rec Bay/UEB Joint",
        1.3400: "UEB/Fuel Tank Joint",
        2.5800: "Fuel Tank/LEB Joint",
        2.8770: "LEB/Ox Tank Joint",
        3.5170: "Ox Tank/Injector Joint",
        4.0564: "Injector/Fin Can Joint"
    }
    joint_xs = list(structural_joints.keys())
    joint_labels = list(structural_joints.values())
    # ------------------------------------------------------------------

# Load diagram (Transverse / Lateral Loads)
    # This plots the discrete lateral forces (lift components vs lateral inertia)
    loads_d = {
        "x": np.array(
            rocket_parts_x_cm.tolist() + [nose_body_x_cp, wing_x_cp,
                                          body_wing_x_cp] + [0, length_l]),
        "p": np.array(
            rocket_parts_p.tolist() + [nose_body_lift_l, wing_lift_l,
                                       body_wing_lift_l] + [0, 0]),
        "m_concentrated": np.array(
            rocket_parts_inertial_torque.tolist() + [0, 0, 0] + [0, 0]),
        "section": rocket_parts_df["Rocket_part"].tolist()
                    + ["Nose Lift", "Wing Lift", "Body/Wing Lift", "Start", "End"],
    }
    loads_df_raw = pd.DataFrame(data=loads_d).sort_values(by=["x"])

    joint_load_df = pd.DataFrame({"x": joint_xs, "p": 0.0, "m_concentrated": 0.0, "section": joint_labels})
    loads_df = pd.concat([loads_df_raw, joint_load_df]).sort_values(by="x", kind='stable').reset_index(drop=True)

    loads_x = loads_df["x"]  # [m]
    loads_p = loads_df["p"]  # [N]
    loads_m_conc = loads_df["m_concentrated"]  # [N m]
    section_labels = loads_df["section"]  # Section labels for parts

    fig1 = go.Figure()
    fig1.add_trace(
        go.Bar(x=loads_x, y=loads_p, text=section_labels, textposition="outside")
    ) 
    fig1.update_layout(
        xaxis_range=[0, length_l],
        xaxis_title="Position, x [m]",
        yaxis_title="Transverse Load, P [N]",
        title="Transverse Load Diagram",
    )
    fig1.update_traces(marker=dict(line=dict(width=10, color="blue")))
    fig1.show()

    # Shear diagram
    # Produces a shear diagram plotting the cumulative sum of the lateral loads
    shears_d = {
        "x": np.repeat(np.copy(loads_x), 2)[1:-1],
        "shear_v": np.repeat(np.add.accumulate(np.copy(loads_p)), 2)[:-2],
        "section": np.repeat(np.array(loads_df["section"].tolist()), 2)[1:-1],
    }
    shears_df = pd.DataFrame(data=shears_d)

    shears_x = shears_df["x"]  # [m]
    shears_shear_v = shears_df["shear_v"]  # [N]
    shears_labels = shears_df["section"]  # Section labels

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=shears_x, y=shears_shear_v, mode='lines+markers', line=dict(color='red'), text=shears_labels, hovertemplate='<b>%{text}</b><br>x: %{x:.2f} m<br>Shear: %{y:.1f} N<extra></extra>'))
    fig2.update_layout(
        xaxis_range=[0, length_l],
        xaxis_title="Position, x [m]",
        yaxis_title="Transverse Shear, V [N]",
        title="Transverse Shear Diagram",
    )
    fig2.show()

    # Axial Forces diagram
    # Produces a compressive forces diagram based strictly on longitudinal drag and mass * axial acceleration
    compressive_d = {
        "x": np.array(rocket_parts_x_cm.tolist()),
        "compressive_v": np.array(rocket_parts_c.tolist()),
        "section": rocket_parts_df["Rocket_part"].tolist(),
    }
    compressive_df_raw = pd.DataFrame(data=compressive_d).sort_values(by=["x"])

    def get_axial(x_target):
        mask = compressive_df_raw["x"] <= x_target
        if mask.any(): return compressive_df_raw.loc[mask, "compressive_v"].iloc[-1]
        return 0.0

    joint_axials = [get_axial(x) for x in joint_xs]
    joint_axial_df = pd.DataFrame({"x": joint_xs, "compressive_v": joint_axials, "section": joint_labels})
    compressive_df = pd.concat([compressive_df_raw, joint_axial_df]).sort_values(by="x", kind='stable').reset_index(drop=True)

    compressive_x = compressive_df["x"]  # [m]
    compressive_compress_v = compressive_df["compressive_v"]  # [N]
    compressive_labels = compressive_df["section"]  # Section labels

    fig3 = go.Figure()
    # Using 'hv' (horizontal-vertical) shape to show discrete stepped loading across components
    fig3.add_trace(go.Scatter(x=compressive_x, y=compressive_compress_v, mode='lines+markers', line=dict(color='green', shape='hv'), text=compressive_labels, hovertemplate='<b>%{text}</b><br>x: %{x:.2f} m<br>Axial Force: %{y:.1f} N<extra></extra>'))
    fig3.update_layout(
        xaxis_range=[0, length_l],
        xaxis_title="Position, x [m]",
        yaxis_title="Axial Compressive Force, T [N]",
        title="Axial Force Diagram",
    )
    fig3.show()

    # Moment diagram
    # Produces a bending moment diagram by integrating the transverse shear diagram over x
    dx = np.diff(loads_x, prepend=loads_x.iloc[0])
    shear_v = np.cumsum(loads_p)
    shifted_shear = np.insert(shear_v[:-1].to_numpy(), 0, 0)
    moment_m = np.cumsum(shifted_shear * dx) + np.cumsum(loads_m_conc)  

    moments_d = {
        "x": loads_x,
        "moment_m": moment_m,
        "section": loads_df["section"],
    }
    moments_df = pd.DataFrame(data=moments_d)

    moments_x = moments_df["x"]  # [m]
    moments_moment_m = moments_df["moment_m"]  # [N m]
    moments_labels = moments_df["section"]  # Section labels

    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=moments_x, y=moments_moment_m, mode='lines+markers', line=dict(color='purple'), text=moments_labels, hovertemplate='<b>%{text}</b><br>x: %{x:.2f} m<br>Moment: %{y:.1f} N m<extra></extra>'))
    fig4.update_layout(
        xaxis_range=[0, length_l],
        xaxis_title="Position, x [m]",
        yaxis_title="Bending Moment, M [N m]",
        title="Bending Moment Diagram",
    )
    fig4.show()

    return True

if __name__ == '__main__':
    main()
